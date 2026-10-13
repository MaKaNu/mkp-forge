# CLI

`mkp-forge` builds Checkmk extension packages (`.mkp`) without a Checkmk installation.

## Installation

```bash
pip install mkp-forge
```

## Usage

```bash
mkp-forge [OPTIONS] COMMAND [ARGS]...
```

| Option          | Description                                    |
| --------------- | ---------------------------------------------- |
| `-v, --verbose` | Enable verbose logging.                        |
| `--help`        | Show help for any command.                     |

Shell completion is available via `--install-completion` and `--show-completion`.

## Commands

### `package build`

Create a `.mkp` file from a package info file and a project directory.

```bash
mkp-forge package build [--info PATH] [--project PATH]
```

| Option              | Default                         | Description                    |
| ------------------- | ------------------------------- | ------------------------------ |
| `-p, --project`     | current directory               | Path to the MKP project dir.   |
| `-i, --info`        | `<project dir name>.info` inside the project dir | Path to the MKP info file. |

The result is written to the current working directory as `<name>-<version>.mkp`,
using `name` and `version` from the info file.

#### Examples

Build from the current directory (expects `./<dirname>.info`):

```bash
mkp-forge package build
```

Build a specific project with an explicit info file:

```bash
mkp-forge -v package build --project ./dummy_mkp_project --info ./dummy_mkp_project/info_basic
```

#### Info file

The info file is a Python dictionary literal. File paths in `files` are relative
to the project directory.

```python
{'author': 'Tester',
 'description': 'TestDescription',
 'download_url': 'https://github.com/dummy/dummy',
 'files': {'agents': ['plugins/dummy'],
           'cmk_addons_plugins': ['dummy/agent_based/dummy.py']},
 'name': 'dummy',
 'title': 'Dummy',
 'version': '1.0.0',
 'version.min_required': '2.5.0p6',
 'version.packaged': 'cmk-mkp-tool 3.0.0',
 'version.usable_until': None}
```

#### Exit codes

| Code | Meaning                                                              |
| ---- | -------------------------------------------------------------------- |
| `0`  | Package created.                                                     |
| `1`  | Info file not found, or project files do not match the info file.    |
