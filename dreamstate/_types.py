from typing import Annotated

from typer import Argument

_help_boiler = "The boilerplate to use for the project."
_example_help_boiler = (
    "(example: [red]flask@default[/red] or [red]flask@default:latest[/red])"
)
Boilerplate = Annotated[
    str,
    Argument(
        help=_help_boiler + _example_help_boiler,
        show_default=False,
        rich_help_panel="Optional Argument",
    ),
]

CreatorBoiler = Annotated[
    str,
    Argument(
        help="The creator of the boilerplate.",
        show_default=False,
        rich_help_panel="Optional Argument",
    ),
]
