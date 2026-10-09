"""Define and parse package manifests."""

import ast
import enum
import logging
import pprint
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from mkp_forge.type_defs import PackageID, PackageName, PackageVersion

_logger = logging.getLogger(__name__)


@enum.unique
class PackagePart(enum.StrEnum):
    """A category of files included in a package manifest."""

    # We have to inherit str to make the (de)serialization work as expected.
    # It's a shame, but other approaches don't work or are worse.
    CMK_PLUGINS = "cmk_plugins"
    CMK_ADDONS_PLUGINS = "cmk_addons_plugins"
    EC_RULE_PACKS = "ec_rule_packs"
    AGENT_BASED = "agent_based"
    CHECKS = "checks"
    HASI = "inventory"
    CHECKMAN = "checkman"
    AGENTS = "agents"
    NOTIFICATIONS = "notifications"
    GUI = "gui"
    WEB = "web"
    PNP_TEMPLATES = "pnp-templates"
    DOC = "doc"
    LOCALES = "locales"
    BIN = "bin"
    LIB = "lib"
    MIBS = "mibs"
    ALERT_HANDLERS = "alert_handlers"

    @property
    def ident(self) -> str:
        """Return the manifest identifier string for this package part.

        Returns:
            str: The canonical string value used in manifest files.
        """
        return self.value


class Manifest(BaseModel):
    """Represent the metadata and file lists defined by a package manifest."""

    title: str
    name: PackageName
    description: str
    version: PackageVersion
    version_packaged: str = Field(alias="version.packaged")
    version_min_required: str = Field(alias="version.min_required")
    version_usable_until: str | None = Field(None, alias="version.usable_until")
    author: str
    download_url: str
    files: Mapping[PackagePart, Sequence[Path]]

    model_config = ConfigDict(
        validate_by_name=True,
        frozen=True,
        extra="allow",  # we used to have 'num_files' :-(
    )

    def file_content(self) -> str:
        """Return the manifest as a pretty-printed Python dictionary.

        Returns:
            str: The manifest content rendered with alias names and file paths as
                strings in a human-readable Python literal format.
        """
        raw = {
            **self.model_dump(by_alias=True),
            "files": {p.ident: [str(f) for f in files] for p, files in self.files.items()},
        }
        return f"{pprint.pformat(raw)}\n"

    def json_file_content(self) -> str:
        """Return the manifest serialized as JSON using alias field names.

        Returns:
            str: The manifest content as a JSON string.
        """
        return self.model_dump_json(by_alias=True)

    @classmethod
    def parse_python_string(cls, raw: str) -> Self:
        """Parse a manifest definition from a Python literal string.

        Args:
            raw (str): A Python dictionary literal describing the manifest.

        Returns:
            Self: A validated Manifest instance created from the parsed data.
        """
        return cls.model_validate(ast.literal_eval(raw))

    @property
    def id(self) -> PackageID:
        """Return the package identifier for this manifest.

        Returns:
            PackageID: The canonical package identifier composed from the package
                name and version.
        """
        return PackageID(name=self.name, version=self.version)


def read_manifest(manifest_path: Path) -> Manifest:
    """Load and validate a package manifest from a file.

    Args:
        manifest_path (Path): Path to the manifest file.

    Returns:
        Manifest: The validated manifest parsed from the file contents.
    """
    return Manifest.parse_python_string(manifest_path.read_text())
