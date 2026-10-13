from pathlib import Path

import pytest
from typer.testing import CliRunner

from mkp_forge.cli.main import app

runner = CliRunner()


@pytest.fixture
def dummy_project_dir():
    return Path(__file__).parent / "data/good/dummy_mkp_project"


@pytest.mark.parametrize(
    ("base_flags", "extended_args", "expected_stdout_lines"),
    (
        [[], [], 0],
        [["-v"], [], 3],
    ),
    ids=("base", "verbose"),
)
def test_cli_build(
    tmp_path,
    monkeypatch,
    dummy_project_dir,
    base_flags,
    extended_args,
    expected_stdout_lines,
):

    # base flags
    base_command = base_flags

    base_command.extend(["package", "build"])

    base_command.extend(["-i", str(dummy_project_dir / "info_basic"), "-p", str(dummy_project_dir)])

    # extended args
    base_command.extend(extended_args)

    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, base_command)

    if result.exit_code != 0:
        print(f"STDERR: {result.stderr}")

    assert result.exit_code == 0
    assert Path("dummy-1.0.0.mkp").exists()
    assert len(result.stdout.splitlines()) == expected_stdout_lines


def test_cli_build_without_info():
    result = runner.invoke(app, ["package", "build"])

    assert result.exit_code == 1
    assert "MKP manifest info file" in result.stderr


def test_cli_build_without_project(dummy_project_dir):
    result = runner.invoke(app, ["package", "build", "-i", str(dummy_project_dir / "info_basic")])

    assert result.exit_code == 1
    assert "Selected MKP project directory" in result.stderr


def test_cli_verbose():
    result = runner.invoke(app, ["-v", "package", "build"])

    assert result.exit_code == 1
    assert "MKP manifest info file" in result.stderr
