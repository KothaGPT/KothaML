import argparse
import datetime
import subprocess
from typing import Dict, Optional

from ml_buildkit import build_utils
from ml_buildkit.helpers import build_docker

REMOTE_IMAGE_PREFIX = "khulnasoft/"
IMAGE_NAME = "ml-workspace"


def get_docker_image_name(flavor: str) -> str:
    """Get the name of the Docker image."""
    return f"{IMAGE_NAME}-{flavor}"


def get_base_image(flavor: str, version: str, release: bool) -> str:
    """Get the base image for the build."""
    base_image = f"{IMAGE_NAME}:{version}"
    if release:
        return f"{REMOTE_IMAGE_PREFIX}{base_image}"
    return base_image


def get_build_args(
    flavor: str, version: str, vcs_ref: str, build_date: str
) -> Dict[str, str]:
    """Get the build arguments for the Docker image."""
    return {
        "ARG_WORKSPACE_BASE_IMAGE": get_base_image(flavor, version, False),
        "ARG_WORKSPACE_VERSION": version,
        "ARG_WORKSPACE_FLAVOR": flavor,
        "ARG_VCS_REF": vcs_ref,
        "ARG_BUILD_DATE": build_date,
    }


def get_vcs_ref() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("ascii")
            .strip()
        )
    except Exception:
        return "unknown"


def get_build_date() -> str:
    try:
        return (
            subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"])
            .decode("ascii")
            .strip()
        )
    except Exception:
        return datetime.datetime.utcnow().isoformat("T") + "Z"


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--flavor",
        help="Flavor (gpu) used for docker container",
        default="gpu",
    )
    args = build_utils.parse_arguments(argument_parser=parser)

    version = args.get(build_utils.FLAG_VERSION)
    docker_image_prefix: Optional[str] = args.get(build_docker.FLAG_DOCKER_IMAGE_PREFIX)

    if not docker_image_prefix:
        docker_image_prefix = REMOTE_IMAGE_PREFIX

    flavor = args["flavor"].lower().strip()

    if flavor not in ["gpu"]:
        build_utils.exit_process(1, "Unknown flavor")

    docker_image_name = get_docker_image_name(flavor)

    vcs_ref = get_vcs_ref()
    build_date = get_build_date()

    if args.get(build_utils.FLAG_MAKE):
        build_args = get_build_args(flavor, version, vcs_ref, build_date)

        build_docker.build_docker_image(
            docker_image_name, version=version, build_args=build_args, exit_on_error=True
        )

    if args.get(build_utils.FLAG_TEST):
        import docker

        workspace_name = f"workspace-test-{flavor}"
        workspace_port = "8080"
        client = docker.from_env()
        container = client.containers.run(
            f"{docker_image_name}:{version}",
            name=workspace_name,
            environment={
                "WORKSPACE_NAME": workspace_name,
                "WORKSPACE_ACCESS_PORT": workspace_port,
            },
            detach=True,
        )

        container.reload()
        container_ip = container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]

        completed_process = build_utils.run(
            f"docker exec --env WORKSPACE_IP={container_ip} {workspace_name} pytest '/resources/tests'",
            exit_on_error=False,
        )

        container.remove(force=True)
        if completed_process.returncode > 0:
            build_utils.exit_process(1)

    if args.get(build_utils.FLAG_RELEASE):
        build_docker.release_docker_image(
            docker_image_name, version, docker_image_prefix, exit_on_error=True
        )


if __name__ == "__main__":
    main()
