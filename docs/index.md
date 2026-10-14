# mkp-forge

[![Release](https://img.shields.io/github/v/release/makanu/mkp-forge)](https://img.shields.io/github/v/release/makanu/mkp-forge)
[![Build status](https://img.shields.io/github/actions/workflow/status/makanu/mkp-forge/main.yml?branch=main)](https://github.com/makanu/mkp-forge/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/makanu/mkp-forge)](https://img.shields.io/github/commit-activity/m/makanu/mkp-forge)
[![License](https://img.shields.io/github/license/makanu/mkp-forge)](https://img.shields.io/github/license/makanu/mkp-forge)

This is a tool to build mkp packages directly without the need to install the checkmk.

## Inatall

### with `pip`

```bash
pip install mkp-forge
```

### with `uv`

```bash
# as tool
uvx mkp-forge --help

# inside project
uv add mkp-forge
```

## Usage

```bash
# build a mkp package
mkp-forge package build -i <mkp-info> -p <package-project>
```
