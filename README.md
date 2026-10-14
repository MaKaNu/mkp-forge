# mkp-forge

[![Release](https://img.shields.io/github/v/release/makanu/mkp-forge)](https://img.shields.io/github/v/release/makanu/mkp-forge)
[![Build status](https://img.shields.io/github/actions/workflow/status/makanu/mkp-forge/main.yml?branch=main)](https://github.com/makanu/mkp-forge/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/makanu/mkp-forge/branch/main/graph/badge.svg)](https://codecov.io/gh/makanu/mkp-forge)
[![Commit activity](https://img.shields.io/github/commit-activity/m/makanu/mkp-forge)](https://img.shields.io/github/commit-activity/m/makanu/mkp-forge)
[![License](https://img.shields.io/github/license/makanu/mkp-forge)](https://img.shields.io/github/license/makanu/mkp-forge)

This is a tool to build mkp packages directly without the need to install checkmk.

- **Github repository**: <https://github.com/makanu/mkp-forge/>
- **Documentation** <https://makanu.github.io/mkp-forge/>

most of the library code is based on the checkmk mkp tool code.

> Currently only building packages is supported. Refer for [Planned Features](#planned-features) for further information.

## Quick Reference

> Read [Documentation](https://makanu.github.io/mkp-forge/) for detailed getting started.

### Install

#### with `pip`

```bash
pip install mkp-forge
```

#### with `uv`

```bash
# as tool
uvx mkp-forge --help

# inside project
uv add mkp-forge
```

### Usage

```bash
# build a mkp package
mkp-forge package build -i <mkp-info> -p <package-project>
```

## Releasing a new version

- Create a [new release](https://github.com/makanu/mkp-forge/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/cicd/#how-to-trigger-a-release).

## Planned Features

- Version Validation
- Publishing? (Does checkmk exchange allows api uploads?)
- Templating (via other repos)

---

Repository initiated with [osprey-oss/cookiecutter-uv](https://github.com/osprey-oss/cookiecutter-uv).
