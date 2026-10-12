from pathlib import Path

import typer

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
        print(f"Packaging Project '{mkp_project}' with '{mkp_info}'.")
        typer.secho(f"Packaging Project '{mkp_project}' with '{mkp_info}'.", fg=typer.colors.GREEN)
