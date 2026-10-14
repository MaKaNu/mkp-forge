# Structure of a mkp package

This Section describes the based on version/version-range how the package project
needs to be structured.

The Structure is the result of a combination of default python package
development in context to how check builds the
[mkp_tool](https://github.com/Checkmk/checkmk/tree/master/packages/cmk-mkp-tool)
internally.

Naming conventions are recommended but not mandatory and
could be controlled via cli.

The info file does not only provides the necessary info for the checkmk tool it
is also used for validation.
The files section need to match file structure.
With this strucute it is possible to create local library tests while matching
the expected checkmk plugin structure.
This allows creating complex server site plugins.

## 2.5.0p6 based

### File Structure

```
dummy_mkp_project/
├── dummy_mkp_project.info
└── src
    ├── dummy
    │   ├── agent_based
    │   │   └── dummy.py
    │   ├── bakery
    │   │   └── bakery_dummy.py
    │   ├── checkman
    │   │   └── dummy
    │   ├── graphing
    │   │   └── graphing_dummy.py
    │   └── rulesets
    │       └── ruleset_dummy.py
    └── plugins
        └── dummy
```

### Info Content

```
{'author': 'Tester',
 'description': 'TestDescription',
 'download_url': 'https://github.com/dummy/dummy',
 'files': {'agents': ['plugins/dummy'],
           'cmk_addons_plugins': ['dummy/agent_based/dummy.py',
                                  'dummy/bakery/bakery_dummy.py',
                                  'dummy/checkman/dummy',
                                  'dummy/graphing/graphing_dummy.py',
                                  'dummy/rulesets/ruleset_dummy.py']},
 'name': 'dummy',
 'title': 'Dummy',
 'version': '1.0.0',
 'version.min_required': '2.5.0p6',
 'version.packaged': 'mkp-forge 1.0.0',
 'version.usable_until': None}
```
