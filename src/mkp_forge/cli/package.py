from pathlib import Path

import typer
from rich.console import Console

from mkp_forge.manifest import read_manifest
from mkp_forge.packaging import create_mkp, write_mkp

err_console = Console(stderr=True)

app = typer.Typer(help="Package management commands.")

BUILD_MKP_INFO = typer.Option(None, "--info", "-i", help="Path to mkp info file.")
BUILD_MKP_PROJECT = typer.Option(None, "--project", "-p", help="Path to mkp project dir.")


@app.command("build")
def create_package(ctx: typer.Context, mkp_info: Path = BUILD_MKP_INFO, mkp_project: Path = BUILD_MKP_PROJECT):
    """
    Create a new package file based on info and project.
    """
    verbose = ctx.obj.get("VERBOSE", False)

    if verbose:
        typer.secho("Debug: Start building mkp package.", fg=typer.colors.GREEN)

    if not mkp_project:
        mkp_project = Path(".")

    if not mkp_info:
        project_name = mkp_project.resolve().name
        mkp_info = mkp_project.resolve() / f"{project_name}.info"

    if verbose:
        typer.secho(f"Packaging Project '{mkp_project}' with '{mkp_info}'.", fg=typer.colors.GREEN)

    try:
        manifest = read_manifest(mkp_info)
    except FileNotFoundError as e:
        err_console.print(f"MKP manifest info file {e.filename} not Found!")
        raise typer.Exit(code=1) from e
    try:
        mkp_bytes = create_mkp(manifest, mkp_project)
    except FileNotFoundError as e:
        err_console.print(
            f"Selected MKP project directory '{mkp_project}' incompatible with paths of info file '{mkp_info}'!"
        )
        raise typer.Exit(code=1) from e
    write_mkp(manifest, mkp_bytes)
