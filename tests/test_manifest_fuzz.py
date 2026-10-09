import ast
import copy
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from mkp_forge.manifest import Manifest, read_manifest

GOOD_FILE = Path(__file__).parent / "data/good/dummy_mkp_project/info_basic"
GOOD_RAW = ast.literal_eval(GOOD_FILE.read_text())

# ValidationError and UnicodeDecodeError are ValueError subclasses; listed for clarity.
EXPECTED_ERRORS = (OSError, SyntaxError, TypeError, ValueError, ValidationError)

REQUIRED_KEYS = [
    "title",
    "name",
    "description",
    "version",
    "version.packaged",
    "version.min_required",
    "author",
    "download_url",
    "files",
]

# Anything that is a valid python literal, to mutate individual fields with.
literals = st.recursive(
    st.none() | st.booleans() | st.integers() | st.floats() | st.text() | st.binary(),
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    max_leaves=10,
)


def _write(tmp_path: Path, content: str | bytes) -> Path:
    path = tmp_path / "info"
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8", errors="surrogatepass")
    return path


def _read(content: str | bytes) -> Manifest:
    # tmp_path is function scoped, which hypothesis dislikes; use a fresh dir per example.

    with tempfile.TemporaryDirectory() as d:
        return read_manifest(_write(Path(d), content))


def _assert_valid_or_expected_error(content: str | bytes) -> None:
    try:
        result = _read(content)
    except EXPECTED_ERRORS:
        return
    assert isinstance(result, Manifest)


def _assert_rejected(content: str | bytes) -> None:
    with pytest.raises(EXPECTED_ERRORS):
        _read(content)


@settings(max_examples=300, deadline=None)
@given(st.text() | st.binary())
def test_arbitrary_content_never_raises(content):
    _assert_valid_or_expected_error(content)


@settings(max_examples=300, deadline=None)
@given(st.text())
def test_arbitrary_text_after_valid_prefix_never_raises(suffix):
    _assert_valid_or_expected_error(GOOD_FILE.read_text() + suffix)


@settings(max_examples=300, deadline=None)
@given(st.data())
def test_truncated_file_never_raises(data):
    raw = GOOD_FILE.read_text()
    cut = data.draw(st.integers(0, len(raw.rstrip()) - 1))
    _assert_rejected(raw[:cut])  # a truncated dict literal can never be valid


@settings(max_examples=300, deadline=None)
@given(st.data())
def test_single_character_corruption_never_raises(data):
    raw = GOOD_FILE.read_text()
    pos = data.draw(st.integers(0, len(raw) - 1))
    char = data.draw(st.characters())
    _assert_valid_or_expected_error(raw[:pos] + char + raw[pos + 1 :])


@settings(max_examples=300, deadline=None)
@given(key=st.sampled_from(sorted(GOOD_RAW)), value=literals)
def test_field_replaced_by_arbitrary_literal_never_raises(key, value):
    mutated = copy.deepcopy(GOOD_RAW)
    mutated[key] = value
    _assert_valid_or_expected_error(repr(mutated))


@pytest.mark.parametrize("key", REQUIRED_KEYS)
def test_missing_required_key_is_rejected(key):
    mutated = {k: v for k, v in GOOD_RAW.items() if k != key}
    _assert_rejected(repr(mutated))


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("name", "1invalid"),
        ("name", "has space"),
        ("name", ""),
        ("name", "a/b"),
        ("version", "1.0/evil"),
        ("title", 42),
        ("files", ["not", "a", "mapping"]),
        ("files", {"unknown_part": ["x"]}),
        ("files", {"agents": "not-a-list-of-paths"}),
        ("files", {"agents": [None]}),
    ],
)
def test_invalid_field_value_is_rejected(key, value):
    mutated = {**GOOD_RAW, key: value}
    _assert_rejected(repr(mutated))


@pytest.mark.parametrize(
    "content",
    [
        "",
        "{",
        "None",
        "[]",
        "__import__('os').system('true')",
        "{'a': (lambda: 1)()}",
    ],
)
def test_non_literal_or_non_mapping_is_rejected(content):
    _assert_rejected(content)
