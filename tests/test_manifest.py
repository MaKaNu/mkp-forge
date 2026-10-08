from pathlib import Path

import pytest

from mkp_forge.manifest import Manifest, read_manifest


@pytest.mark.parametrize("filename", [Path("info_basic")], ids=["basic"])
def test_good_examples(filename):
    good_example_path = Path(__file__).parent / "data" / "good" / filename
    assert isinstance(read_manifest(manifest_path=good_example_path), Manifest)
