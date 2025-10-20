<!-- markdownlint-disable MD024 -->
# Contribute to ML Workspace

Thanks for your interest in contributing to our project. We are excited to see you here!

## Table of contents

1. [Issues and bug reports](#issues-and-bug-reports)
2. [Contributing to the code base](#contributing-to-the-code-base)
    - [Development instructions](#development-instructions)
    - [Commit messages guidelines](#commit-messages-guidelines)
    - [Opening a pull request](#opening-a-pull-request)
    - [Review & merging of a pull request](#review--merging-of-a-pull-request)
    - [Git workflow & versioning](#git-workflow--versioning)
3. [Code conventions](#code-conventions)
    - [Python conventions](#python-conventions)
4. [Code of conduct](#code-of-conduct)

## Issues and bug reports

- We use GitHub issues to track bugs and enhancement requests. Submit issues for any [feature request](https://github.com/khulnasoft/ml-workspace/issues/new?assignees=&labels=enhancement&template=01_feature-request.md&title=), [bug reports](https://github.com/khulnasoft/ml-workspace/issues/new?assignees=&labels=bug&template=02_bug-report.md&title=) or [documentation](https://github.com/khulnasoft/ml-workspace/issues/new?assignees=&labels=documentation&template=03_documentation.md&title=) problems.
- Before submitting a new issue, please search the existing issues to ensure that the issue has not already been reported.
- When creating an issue, try using one of our [issue templates](https://github.com/khulnasoft/ml-workspace/issues/new/choose) which already contain some guidelines on which content is expected to process the issue most efficiently. If no template applies, you can of course also create an issue from scratch.
- Please provide as much context as possible when you open an issue. The information you provide must be comprehensive enough to reproduce that issue for the assignee. Therefore, contributors should use but aren't restricted to the issue template provided by the project maintainers.
- Please apply one or more applicable [labels](https://github.com/khulnasoft/ml-workspace/labels) to your issue so that all community members are able to cluster the issues better.

## Contributing to the code base

You are welcome to contribute code in order to fix a bug, to implement a new feature, to propose new documentation, or just to fix a typo. Check out [good first issue](https://github.com/khulnasoft/ml-workspace/labels/good%20first%20issue) and [help wanted](https://github.com/khulnasoft/ml-workspace/labels/help%20wanted) issues if you want to find open issues to implement.

- Before writing code, we strongly advise you to search through the existing PRs or issues to make sure that nobody is already working on the same thing. If you find your issue already exists, make relevant comments and add your reaction (👍 - upvote, 👎 - downvote). If you are unsure, it is always a good idea to open an issue to get some feedback.
- Should you wish to work on an existing issue that has not yet been claimed, please claim it first by commenting on the GitHub issue that you want to work on and begin work (the maintainers will assign it to your GitHub user as soon as they can). This is to prevent duplicated efforts from other contributors on the same issue.
- To contribute changes, always branch from the `main` branch and after implementing the changes create a pull request as described [below](#opening-a-pull-request).
- Commits should be as small as possible while ensuring that each commit is correct independently (i.e., each commit should compile and pass tests). Also, make sure to follow the commit message guidelines.
- Test your changes as thoroughly as possible before you commit them. Preferably, automate your test by unit/integration tests.

### Development Instructions

To simplify the process of building this project from scratch, we provide build-scripts - based on [ml-buildkit](https://github.com/korhagpt/ml-buildkit) - that run all necessary steps (build, test, and release) within a containerized environment by using [Github Actions](https://github.com/features/actions) and [Act](https://github.com/nektos/act) to run all actions locally.

> _Please refer to the [documentation of ml-buildkit](https://github.com/korhagpt/ml-buildkit#automated-build-pipeline-ci) for instructions on how to execute the build-scripts directly on your machine instead of using the containerized approach documented below._

#### Requirements

- [Act](https://github.com/nektos/act#installation), [Docker](https://docs.docker.com/get-docker/)

#### Build components

Execute this command in the project root folder to compile, assemble, and package all project components:
