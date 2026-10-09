from pathlib import Path

import pytest

from mkp_forge.manifest import Manifest, read_manifest
from mkp_forge.type_defs import PackageID


@pytest.mark.parametrize(
    ["filename", "name", "version"],
    [
        (Path("dummy_mkp_project/info_basic"), "dummy", "1.0.0"),
    ],
    ids=["basic"],
)
def test_good_examples(filename, name, version):
    good_example_path = Path(__file__).parent / "data/good" / filename
    manifest = read_manifest(manifest_path=good_example_path)
    assert isinstance(manifest, Manifest)
    assert manifest.id == PackageID(name=name, version=version)
