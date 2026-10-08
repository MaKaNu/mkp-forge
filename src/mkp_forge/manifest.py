import ast
import enum
import logging
import pprint
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from mkp_forge.type_defs import PackageID, PackageName, PackageVersion

_logger = logging.getLogger(__name__)


@enum.unique
class PackagePart(enum.StrEnum):
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
        return self.value


class Manifest(BaseModel):
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
        raw = {
            **self.model_dump(by_alias=True),
            "files": {p.ident: [str(f) for f in files] for p, files in self.files.items()},
        }
        return f"{pprint.pformat(raw)}\n"

    def json_file_content(self) -> str:
        return self.model_dump_json(by_alias=True)

    @classmethod
    def parse_python_string(cls, raw: str) -> Self:
        return cls.model_validate(ast.literal_eval(raw))

    @property
    def id(self) -> PackageID:
        return PackageID(name=self.name, version=self.version)


def read_manifest(manifest_path: Path) -> Manifest | None:
    try:
        return Manifest.parse_python_string(manifest_path.read_text())
    except (OSError, SyntaxError, TypeError, ValueError, ValidationError):
        _logger.exception(
            "[%(manifest_path)s]: Failed to read package manifest",
            {"manifest_path": manifest_path},
        )
    return None
