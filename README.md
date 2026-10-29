# Veeam CM/DevOps assessment — working draft

## Task 1: Python

Requires Python 3.12+ and Click.

```bash
python -m pip install -r task1_scripts/requirements.txt
python task1_scripts/search.py ./task2_pipelines 'TestApp'
python task1_scripts/search.py ./task2_pipelines 'TestApp' -e cs
```

By default the script processes a list of known text extensions and extensionless files. This is a practical heuristic, not a guarantee of finding *every* text file. Files with unreadable UTF-8 content are skipped with warnings. Individual read/traversal errors do not cause a nonzero exit status. The count may therefore be incomplete.

## Task 2: GitHub Actions

The workflow is at `.github/workflows/nuget.yml`. Put this directory structure at the **root** of a GitHub repository, on the `main` branch. It runs on pushes to main, pull requests to main, or manually.

The pipeline restores, builds, tests, packs and publishes the provided .NET 8 project. Pull requests do not publish packages. The package version is `1.0.<GitHub run number>`.

Configure repository Actions secrets:

- `NUGET_FEED_URL` — target NuGet feed endpoint.
- `NUGET_API_KEY` — token/API key accepted by that feed.
- `SLACK_WEBHOOK_URL` — Slack incoming webhook for status notification (optional for local review; when absent, notification is skipped).

Some private feeds require `dotnet nuget add source` with username/password instead of an API key; adapt authentication to the actual feed before production use.

The `.trx` test file is generated but is not yet published to the GitHub Actions test UI (Nice to Have).

## Task 3: Docker

See `task3_docker/README.md` for build/run commands. The Docker image is standalone; the GitHub Actions workflow uses `setup-dotnet` rather than this image. Integrating the image into CI is an optional improvement.

## Limitations and validation

These are working drafts to review together, not a verified production release. The Docker build and GitHub Actions workflow have not been executed in this environment. Actual publishing requires real feed secrets. Run the commands locally and review CI logs before submitting.
