import logging
import tarfile
import time
from collections.abc import Iterable
from io import BytesIO
from pathlib import Path

from mkp_forge.manifest import Manifest

_logger = logging.getLogger(__name__)


def write_mkp(manifest: Manifest, mkp_bytes: bytes) -> None:
    mkp_file = Path(f"{manifest.name}-{manifest.version}.mkp")
    with mkp_file.open("wb") as mkp:
        mkp.write(mkp_bytes)


def create_mkp(
    manifest: Manifest,
    project_path: Path,
) -> bytes:

    return create_tgz((
        ("info", manifest.file_content().encode()),
        ("info.json", manifest.json_file_content().encode()),
        *(
            create_tar(part.ident, project_path / "src", filenames)
            for part, filenames in manifest.files.items()
            if filenames
        ),
    ))


def create_tar_info(filename: str, size: int) -> tarfile.TarInfo:
    info = tarfile.TarInfo()
    info.mtime = int(time.time())
    info.uid = 0
    info.gid = 0
    info.size = size
    info.mode = 0o644
    info.type = tarfile.REGTYPE
    info.name = filename
    return info


def create_tgz(files: Iterable[tuple[str, bytes]]) -> bytes:
    buffer = BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for name, content in files:
            tar.addfile(create_tar_info(name, len(content)), BytesIO(content))

    return buffer.getvalue()


def create_tar(name: str, dest: Path, filenames: Iterable[Path]) -> tuple[str, bytes]:
    tarname = f"{name}.tar"
    _logger.debug("  Packing %(tarname)s:", {"tarname": tarname})

    buffer = BytesIO()
    with tarfile.open(
        fileobj=buffer,
        mode="w",
        format=tarfile.GNU_FORMAT,
    ) as tar:
        tar.dereference = True
        for f in filenames:
            _logger.debug("    %(file)s", {"file": f})
            tar.add(dest / f, arcname=f.as_posix())
    return tarname, buffer.getvalue()
