# Debian 12 .NET build agent

The image contains the .NET 8 SDK, Git, CA certificates and curl. It uses the non-root `buildagent` user.

Build from the repository root:

```bash
docker build -t veeam-dotnet-agent:8 -f task3_docker/Dockerfile task3_docker
```

Check the tools:

```bash
docker run --rm veeam-dotnet-agent:8 dotnet --info
docker run --rm veeam-dotnet-agent:8 git --version
```

Run the provided solution's restore, build and tests (Linux/macOS shell, from repository root):

```bash
docker run --rm -v "$(pwd)/task2_pipelines/TestApp:/src" -w /src veeam-dotnet-agent:8 sh -c 'dotnet restore TestApp.sln && dotnet build TestApp.sln --no-restore && dotnet test TestApp.sln --no-build'
```

The build context should not include local `bin/` or `obj/` directories. The first build requires internet access to Microsoft package repositories.
