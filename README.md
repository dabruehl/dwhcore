# dwhcore

**Definitely Won't Help Core**

A lightweight Python library built on one promise: it won't help. No features, no
use cases, no roadmap. Zero dependencies, zero side effects, zero results. Every
function is fully typed, thoroughly documented and guaranteed never to return, on
any platform.

## Installation

```sh
pip install dwhcore
```

This step is also optional.

## Usage

```python
>>> import dwhcore
>>> dwhcore.__version__
'0.0.1'
```

That is the complete supported surface. Anything else raises:

```python
>>> import dwhcore.settings
DefinitelyWontHelpError: dwhcore.settings does not exist.

You have installed 'dwhcore' 0.0.1 from pypi.org.

This package does nothing. It has no modules, no functions and no
features, and it will not help you.

If you were expecting a different library by this name, you have
resolved it from the wrong index.
```

Every name under `dwhcore.*` behaves identically, including names that do not
exist yet. A finder on `sys.meta_path` claims the whole namespace, so there is no
list of modules to fall out of date and no way to find one that quietly works.

The failure is an `ImportError` subclass and arrives at import time, not later.
Nothing returns a placeholder value, so nothing downstream can mistake emptiness
for data.

## FAQ

**Is this a joke?** The name is. The behaviour is deliberate.

**Will you add features?** No. That would break the promise.

**Why does it exist?** The name was available.

## Development

```sh
uv sync --extra dev
uv pip install -e .
uv run pytest
uv run ruff check .
```

## Releasing

### One-time setup

Register a pending publisher on PyPI, otherwise the first tagged run fails with
`invalid-publisher`:

pypi.org → Account settings → Publishing → Add a new pending publisher

| Field | Value |
| --- | --- |
| PyPI Project Name | `dwhcore` |
| Owner | `dabruehl` |
| Repository name | `dwhcore` |
| Workflow name | `release.yml` (the filename, not the `name:` key) |
| Environment name | `pypi` (must match the workflow exactly) |

### Each release

```sh
git tag v0.0.1
git push origin v0.0.1
```

Only a `v*` tag push publishes. A manual `workflow_dispatch` runs the full build,
lint, test and `twine check` as a dry run but never uploads, and CI refuses a tag
that disagrees with the version in `pyproject.toml`.

The version must stay below `0.2`. A resolver configured with several indexes may
merge their candidates and take the highest version, and this package must never
win that comparison. A PyPI version can never be re-uploaded, even after deletion.

## License

MIT. You may use this for nothing, free of charge.
