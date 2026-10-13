import typer

from mkp_forge.cli import package

app = typer.Typer(help="An implementation of standalone mkp package building.", add_completion=True)

app.add_typer(package.app, name="package", help="MKP package tasks.")


@app.callback()
def main(ctx: typer.Context, verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging.")):
    """
    Global CLI callback for shared setup, options and context injection.
    """

    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose

    if verbose:
        typer.secho("Debug: Verbose mode activated.", fg=typer.colors.YELLOW)


if __name__ == "__main__":
    app()
