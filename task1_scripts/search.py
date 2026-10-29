import os
import re
import click


TEXT_EXTENSIONS = (
    ".txt", ".log", ".yaml", ".yml", ".json", ".md",
    ".csv", ".xml", ".py", ".sh", ".conf", ".ini"
)


def handle_walk_error(error):
    click.echo(f"Warning: Could not access directory: {error}", err=True)


def search_files(directory, regex, extensions):
    total_count = 0

    for root, dirs, files in os.walk(directory, onerror=handle_walk_error):
        for filename in files:
            file_ext = os.path.splitext(filename)[1].lower()

            if extensions:
                if file_ext not in extensions:
                    continue
            elif file_ext and file_ext not in TEXT_EXTENSIONS:
                continue

            file_path = os.path.join(root, filename)
            file_count = 0

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        file_count += len(regex.findall(line))
            except (OSError, UnicodeDecodeError) as e:
                click.echo(f"Warning: Could not read {file_path}: {e}", err=True)
                continue

            if file_count > 0:
                click.echo(f"{file_path}: {file_count} matches")

            total_count += file_count

    return total_count


@click.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument("pattern")
@click.option("--extension", "-e", multiple=True)
def main(directory, pattern, extension):
    try:
        regex = re.compile(pattern)
    except re.error as e:
        raise click.ClickException(f"Invalid regex: {e}")

    extensions = tuple((ext if ext.startswith(".") else "." + ext).lower() for ext in extension)

    total = search_files(directory, regex, extensions)
    click.echo(f"\nTotal matches: {total}")


if __name__ == "__main__":
    main()
