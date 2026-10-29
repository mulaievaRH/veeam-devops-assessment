# Veeam CM/DevOps Technical Assessment

Solutions for three tasks: Python scripting, a GitHub Actions CI/CD pipeline, and a Docker-based .NET build agent.

## Task 1 — Python scripting

A CLI utility that recursively searches text files for a regular expression and counts occurrences.

**Requirements:** Python 3.12+.

Install dependencies:

```bash
python -m pip install -r task1_scripts/requirements.txt
```

Examples:

```bash
python task1_scripts/search.py ./task2_pipelines "TestApp"
python task1_scripts/search.py ./task2_pipelines "TestApp" -e .cs
python task1_scripts/search.py ./task2_pipelines "error|warning" -e .txt -e .log
```

The script:

- Accepts a directory and a regex pattern as required arguments.
- Searches recursively, including nested directories.
- Prints matches per file and a total count.
- Supports optional filtering by file extension.
- Reports invalid paths, invalid regex patterns, and file-reading errors.

By default, it processes a predefined set of text file extensions and extensionless files. This is a practical heuristic rather than automatic detection of every possible text format.

Files that cannot be read as UTF-8 are skipped with warnings. Individual file-reading or traversal errors do not fail the entire execution, so the reported total may be incomplete.

## Task 2 — GitHub Actions CI/CD

**Workflow:** `.github/workflows/nuget.yml`

The pipeline runs on:

- Pushes to `main`.
- Pull requests targeting `main`.
- Manual execution through GitHub Actions.

### Pipeline stages

1. **Check builder image:** Verify that the Docker build-agent image is available in GitHub Container Registry (GHCR).
2. **Restore:** Restore dependencies using `dotnet restore`.
3. **Security scan:** Check NuGet dependencies for known vulnerabilities, including transitive dependencies.
4. **Build:** Build the .NET 8 solution in Release configuration.
5. **Test:** Run NUnit unit tests.
6. **Test reporting:** Upload generated `.trx` test results as GitHub Actions artifacts.
7. **Pack:** Create a versioned NuGet package.
8. **Publish:** Push the package to GitHub Packages.
9. **Notify:** Send the pipeline status to Slack when a webhook is configured.

### Package publishing

NuGet feed:

```text
https://nuget.pkg.github.com/mulaievaRH/index.json
```

Package version format:

```text
1.0.<GitHub Actions run number>
```

Publishing happens only on `main`, not on pull requests.

Authentication uses the automatically provided GitHub Actions `GITHUB_TOKEN`. The workflow requires:

```yaml
permissions:
  contents: read
  packages: write
```

No personal access token is required for publishing to GitHub Packages from this repository.

### Security scan

The pipeline runs:

```bash
dotnet list TestApp.sln package --vulnerable --include-transitive
```

This is an informational scan. Vulnerability findings are visible in the workflow logs but do not automatically block publishing.

A production pipeline could introduce severity-based enforcement and a process for reviewing exceptions.

### Notifications

An optional repository secret is supported:

```text
SLACK_WEBHOOK_URL
```

When the webhook is missing or sending the notification fails, the workflow emits a warning instead of failing the build.

### CI build environment

The pipeline uses the Docker image from Task 3:

```text
ghcr.io/mulaievarh/veeam-build-agent:dotnet8
```

The image defines a non-root `buildagent` user by default. GitHub Actions overrides the container user with `--user 0` because its mounted workspace and runner command directories require compatible write permissions.

## Task 3 — Docker build agent

**Dockerfile:** `task3_docker/Dockerfile`

The image is based on Debian 12 slim and includes:

- .NET SDK 8 (LTS)
- Git
- curl
- CA certificates
- A non-root `buildagent` user

Package installation and apt cache cleanup are combined to reduce unnecessary image layers and size.

The Dockerfile also runs sanity checks during the image build.

### Build locally

```bash
docker build -t veeam-build-agent:dotnet8 -f task3_docker/Dockerfile ./task3_docker
```

### Verify installed tools

```bash
docker run --rm veeam-build-agent:dotnet8 bash -c "whoami && dotnet --version && git --version && curl --version"
```

By default, the container runs as `buildagent`.

### Automated image publishing

**Workflow:** `.github/workflows/docker-image.yml`

The workflow builds and publishes the Docker image to GHCR when files in `task3_docker/` or the image-publishing workflow change on `main`. It can also be triggered manually.

Published image:

```text
ghcr.io/mulaievarh/veeam-build-agent:dotnet8
```

The image uses a stable `dotnet8` tag, allowing the CI pipeline to consume a centrally maintained build environment.

## Validation

The following checks were completed:

- Python regex matching, per-file counts, recursive search, extension filtering, and error handling.
- Local Docker image build and verification of the installed tools and non-root user.
- Successful Docker image publication to GHCR.
- Successful GitHub Actions pipeline execution, including NuGet package publication.
- Verification that both the Docker image and the `TestApp` NuGet package are present in GitHub Packages.

### Scope and limitations

This is a technical assessment implementation, not a production-ready delivery platform.

The security scan is informational, the build-agent image uses a mutable version-family tag, and Slack notifications are non-blocking. These choices keep the solution straightforward while demonstrating CI/CD integration, automation, package publishing, and basic security practices.
