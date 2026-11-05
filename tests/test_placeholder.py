"""Tests for a package that does nothing."""

from __future__ import annotations

import importlib
import importlib.metadata

import pytest

import dwhcore
from dwhcore import DefinitelyWontHelpError

# Arbitrary names. The finder claims the whole namespace, so this list is a
# sample rather than a contract: any name must behave the same way.
NAMES = [
    "dwhcore.settings",
    "dwhcore.config",
    "dwhcore.utils",
    "dwhcore.client",
    "dwhcore.constants",
    "dwhcore.anything",
    "dwhcore.a_module_nobody_has_written_yet",
]


@pytest.mark.parametrize("name", NAMES)
def test_import_module_form_fails(name: str) -> None:
    """`import dwhcore.x` raises, naming the module."""
    with pytest.raises(DefinitelyWontHelpError) as excinfo:
        importlib.import_module(name)
    assert name in str(excinfo.value)


@pytest.mark.parametrize("name", NAMES)
def test_from_import_form_fails(name: str) -> None:
    """`from dwhcore import x` raises the same way."""
    attr = name.split(".", 1)[1]
    with pytest.raises(DefinitelyWontHelpError):
        __import__("dwhcore", fromlist=[attr])


def test_no_bare_module_not_found_error() -> None:
    """An unknown name must not degrade to a bare ModuleNotFoundError."""
    with pytest.raises(DefinitelyWontHelpError) as excinfo:
        importlib.import_module("dwhcore.invented_on_the_spot")
    assert not isinstance(excinfo.value, ModuleNotFoundError)
    assert "does nothing" in str(excinfo.value)


def test_failed_import_is_not_cached() -> None:
    """A second import raises again rather than returning a half-built module."""
    for _ in range(2):
        with pytest.raises(DefinitelyWontHelpError):
            importlib.import_module("dwhcore.settings")


def test_error_subclasses_import_error() -> None:
    """`from dwhcore.settings import x` fails as an ImportError."""
    assert issubclass(DefinitelyWontHelpError, ImportError)


def test_nothing_returns_a_placeholder_value() -> None:
    """The package must raise, never hand back an empty stand-in.

    Returning None would let a caller run on to completion on meaningless
    values. Failing at import time is the whole point.
    """
    with pytest.raises(DefinitelyWontHelpError):
        _ = dwhcore.anything_at_all


def test_stdlib_names_are_not_shadowed() -> None:
    """The meta-path finder must claim only the dwhcore namespace."""
    import json
    import logging

    assert json.dumps({"a": 1}) == '{"a": 1}'
    assert logging.getLogger("x").name == "x"


@pytest.mark.parametrize(
    "name",
    ["__wrapped__", "_repr_html_", "_ipython_canary_method_should_not_exist_"],
)
def test_underscore_probes_raise_attribute_error(name: str) -> None:
    """Protocol probes get AttributeError so tooling behaves normally."""
    with pytest.raises(AttributeError):
        getattr(dwhcore, name)


def test_version_stays_low() -> None:
    """The version must never outrank a real package sharing this name.

    A resolver given several indexes may merge their candidates and take
    the highest version. A do-nothing package must lose that comparison.
    """
    from packaging.version import Version

    assert Version(dwhcore.__version__) < Version("0.2")


def test_version_matches_distribution_metadata() -> None:
    """__version__ tracks the version declared in pyproject.toml."""
    assert dwhcore.__version__ == importlib.metadata.version("dwhcore")
