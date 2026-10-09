import tarfile
from io import BytesIO
from pathlib import Path

from mkp_forge.manifest import read_manifest
from mkp_forge.packaging import create_mkp, write_mkp


def test_create_mkp():
    project_path = Path("tests/data/good/dummy_mkp_project")
    manifest = read_manifest(project_path / "info_basic")

    with tarfile.open(fileobj=BytesIO(create_mkp(manifest, project_path)), mode="r:gz") as mkp:
        assert set(mkp.getnames()) == {
            "info",
            "info.json",
            "agents.tar",
            "cmk_addons_plugins.tar",
        }

        agents_file = mkp.extractfile("agents.tar")
        assert agents_file is not None
        with tarfile.open(fileobj=BytesIO(agents_file.read())) as agents_tar:
            assert agents_tar.getnames() == ["plugins/dummy"]

        addons_file = mkp.extractfile("cmk_addons_plugins.tar")
        assert addons_file is not None
        with tarfile.open(fileobj=BytesIO(addons_file.read())) as addons_tar:
            assert "dummy/agent_based/dummy.py" in addons_tar.getnames()
            assert "dummy/bakery/bakery_dummy.py" in addons_tar.getnames()
            assert "dummy/checkman/dummy" in addons_tar.getnames()
            assert "dummy/graphing/graphing_dummy.py" in addons_tar.getnames()
            assert "dummy/rulesets/ruleset_dummy.py" in addons_tar.getnames()


def test_write_mkp(tmp_path, monkeypatch):
    project_path = Path("tests/data/good/dummy_mkp_project")
    manifest = read_manifest(project_path / "info_basic")
    mkp_bytes = create_mkp(manifest, project_path)

    monkeypatch.chdir(tmp_path)
    write_mkp(manifest, mkp_bytes)

    output_path = tmp_path / f"{manifest.name}-{manifest.version}.mkp"
    assert output_path.is_file()
    assert output_path.read_bytes() == mkp_bytes
