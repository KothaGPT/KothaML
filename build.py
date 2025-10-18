import argparse
import datetime
import subprocess

import docker
from ml_buildkit import build_utils
from ml_buildkit.helpers import build_docker

REMOTE_IMAGE_PREFIX = "khulnasoft/"
COMPONENT_NAME = "ml-workspace"
FLAG_FLAVOR = "flavor"


def get_docker_image_name(flavor: str) -> str:
    """Get the name of the Docker image."""
    return COMPONENT_NAME + ("-" + flavor if flavor != "all" else "")


def get_build_args(flavor: str, version: str, git_rev: str, build_date: str) -> str:
    """Get the build arguments for the Docker image."""
    return (
        f" --build-arg ARG_VCS_REF={git_rev}"
        f" --build-arg ARG_BUILD_DATE={build_date}"
        f" --build-arg ARG_WORKSPACE_FLAVOR={flavor}"
        f" --build-arg ARG_WORKSPACE_VERSION={version}"
    )


def build_and_test(flavor: str, args: argparse.Namespace) -> None:
    """Build and test the Docker image."""
    docker_image_name = get_docker_image_name(flavor)
    git_rev = build_utils.get_git_revision()
    build_date = datetime.datetime.utcnow().isoformat("T") + "Z"

    build_args = get_build_args(flavor, args[build_utils.FLAG_VERSION], git_rev, build_date)

    completed_process = build_docker.build_docker_image(
        docker_image_name, version=args[build_utils.FLAG_VERSION], build_args=build_args
    )
    if completed_process.returncode > 0:
        build_utils.exit_process(1)

    if args[build_utils.FLAG_TEST]:
        workspace_name = f"workspace-test-{flavor}"
        workspace_port = "8080"
        client = docker.from_env()
        container = client.containers.run(
            f"{docker_image_name}:{args[build_utils.FLAG_VERSION]}",
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


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--" + FLAG_FLAVOR,
        help="Flavor (full, light, minimal, gpu) used for docker container",
        default="all",
        choices=["all", "full", "light", "minimal", "gpu"],
    )

    args = build_utils.parse_arguments(argument_parser=parser)

    flavor = str(args[FLAG_FLAVOR]).lower().strip()

    if flavor == "all":
        flavors = ["minimal", "light", "full", "gpu"]
    else:
        flavors = [flavor]

    for flavor in flavors:
        build_and_test(flavor, args)

    if args[build_utils.FLAG_RELEASE]:
        # Bump all versions in some files
        previous_version = build_utils.get_latest_version()
        if previous_version:
            build_utils.replace_in_files(
                previous_version,
                args[build_utils.FLAG_VERSION],
                file_paths=["./README.md", "./deployment/google-cloud-run/Dockerfile"],
                regex=False,
                exit_on_error=True,
            )

        build_docker.release_docker_image(
            get_docker_image_name(flavor),
            args[build_utils.FLAG_VERSION],
            REMOTE_IMAGE_PREFIX,
        )


if __name__ == "__main__":
    main()
