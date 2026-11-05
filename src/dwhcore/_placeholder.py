"""Failure machinery shared by the package.

There is no implementation here, or anywhere else in this distribution.
This module exists only to raise a clear error when something tries to
use a package that does nothing.
"""

from __future__ import annotations

from typing import NoReturn

#: Deliberately low, and it must stay that way.
#:
#: Some resolvers are configured with more than one index and merge the
#: candidates from all of them into a single pool, then pick the highest
#: version. A do-nothing package must never win that comparison against a
#: real package that happens to share its name. Do not raise this.
PLACEHOLDER_VERSION = "0.0.1"

_TEMPLATE = """\
{module} does not exist.

You have installed 'dwhcore' {version} from pypi.org.

This package does nothing. It has no modules, no functions and no
features, and it will not help you.

If you were expecting a different library by this name, you have
resolved it from the wrong index.
"""


class DefinitelyWontHelpError(ImportError):
    """Raised on any attempt to import something from this package."""


def message_for(module: str) -> str:
    """Build the message for an attempted import.

    Args:
        module: Dotted name of the module that was imported.

    Returns:
        The full multi-line message.
    """
    return _TEMPLATE.format(module=module, version=PLACEHOLDER_VERSION)


def fail(module: str) -> NoReturn:
    """Raise :class:`DefinitelyWontHelpError`.

    Args:
        module: Dotted name of the module that was imported.

    Raises:
        DefinitelyWontHelpError: Always.
    """
    raise DefinitelyWontHelpError(message_for(module))
