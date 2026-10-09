"""Create and write MKP package archives."""

import logging
import tarfile
import time
from collections.abc import Iterable
from io import BytesIO
from pathlib import Path

from mkp_forge.manifest import Manifest

_logger = logging.getLogger(__name__)


def write_mkp(manifest: Manifest, mkp_bytes: bytes) -> None:
    """Writes given mkp_bytes to mkp files based on manifest information.

    Args:
        manifest (Manifest): Manifest from plugin info file.
        mkp_bytes (bytes): mkp bytes created from manifest.
    """
    mkp_file = Path(f"{manifest.name}-{manifest.version}.mkp")
    with mkp_file.open("wb") as mkp:
        mkp.write(mkp_bytes)


def create_mkp(
    manifest: Manifest,
    project_path: Path,
) -> bytes:
    """Combines project_path with manifest to create mkp byte

    Args:
        manifest (Manifest): Manifest from plugin info file.
        project_path (Path): Project path of Plugin Project.

    Returns:
        bytes: _description_
    """

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
    """Creates tar GNU file information

    Args:
        filename (str): filename of tarinfo
        size (int): Size of the filename

    Returns:
        tarfile.TarInfo: minimalized tar info for tar packaging.
    """
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
    """Creates tar.gz bytes based on given files.

    Args:
        files (Iterable[tuple[str, bytes]]): files which will be included into tar.gz

    Returns:
        bytes: tar.gz bytes object.
    """
    buffer = BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for name, content in files:
            tar.addfile(create_tar_info(name, len(content)), BytesIO(content))

    return buffer.getvalue()


def create_tar(name: str, loc: Path, filenames: Iterable[Path]) -> tuple[str, bytes]:
    """Creates a list of Bytes which represent the content of filenames.

    Args:
        name (str): name of tar file
        loc (Path): location of file in project dir
        filenames (Iterable[Path]): names of files from manifest

    Returns:
        tuple[str, bytes]: group of bytes per filename
    """
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
            tar.add(loc / f, arcname=f.as_posix())
    return tarname, buffer.getvalue()
