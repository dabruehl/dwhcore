"""Definitely Won't Help Core.

A lightweight Python library built on one promise: it won't help.

Importing this package succeeds, so that tooling can read ``__version__``
and confirm there is nothing here. Importing anything from it raises
:class:`DefinitelyWontHelpError`.

Coverage does not depend on a list of module files. A finder on
:data:`sys.meta_path` claims the whole ``dwhcore.*`` namespace, so every
name fails the same way, including names nobody has thought of yet.
"""

from __future__ import annotations

import sys
from importlib.machinery import ModuleSpec
from importlib.util import spec_from_loader
from types import ModuleType
from typing import Sequence

from dwhcore._placeholder import (
    PLACEHOLDER_VERSION,
    DefinitelyWontHelpError,
    fail,
    message_for,
)

__version__ = PLACEHOLDER_VERSION

__all__ = [
    "DefinitelyWontHelpError",
    "__version__",
    "message_for",
]


class _PlaceholderLoader:
    """Loader whose only job is to raise when the module body would run."""

    def __init__(self, fullname: str) -> None:
        """Store the module name so the error can name it.

        Args:
            fullname: Dotted name of the module being imported.
        """
        self._fullname = fullname

    def create_module(self, spec: ModuleSpec) -> ModuleType | None:
        """Use default module creation semantics.

        Args:
            spec: Spec for the module being created.

        Returns:
            None, meaning the default module object.
        """
        return None

    def exec_module(self, module: ModuleType) -> None:
        """Raise instead of populating the module.

        Args:
            module: The module that would have been populated.

        Raises:
            DefinitelyWontHelpError: Always.
        """
        fail(self._fullname)


class _PlaceholderFinder:
    """Claims every public ``dwhcore.*`` submodule so each import fails."""

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None = None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        """Claim public submodules of this package, decline everything else.

        Args:
            fullname: Dotted name of the module being imported.
            path: Parent package search path, unused.
            target: Module being reloaded, unused.

        Returns:
            A spec backed by :class:`_PlaceholderLoader` for public
            ``dwhcore.*`` names, otherwise None so normal import continues.
        """
        if not fullname.startswith("dwhcore."):
            return None
        if fullname.startswith("dwhcore._"):
            return None
        return spec_from_loader(fullname, _PlaceholderLoader(fullname))


sys.meta_path.insert(0, _PlaceholderFinder())


def __getattr__(name: str) -> object:
    """Fail for any attribute, because there are none.

    Args:
        name: Attribute requested from the package.

    Returns:
        Never returns normally.

    Raises:
        AttributeError: For underscore-prefixed names, so that protocol
            probes from REPLs, notebooks and ``hasattr`` behave normally.
        DefinitelyWontHelpError: For every other name.
    """
    if name.startswith("_"):
        raise AttributeError(name)
    fail(f"dwhcore.{name}")
