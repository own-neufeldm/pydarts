import argparse

import pydarts
from pydarts.gui.app import App


class Args(argparse.Namespace):
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(**args.__dict__)
        self.enable_debug: bool
        self.show_version: bool
        return None


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        prog="pydarts",
        description="Tracks the score of a Darts game.",
    )
    parser.add_argument(
        "--debug",
        help="write verbose messages and outline widgets",
        dest="enable_debug",
        action="store_true",
    )
    parser.add_argument(
        "--version",
        help="show the installed version and exit",
        dest="show_version",
        action="store_true",
    )
    return Args(parser.parse_args())


def main() -> None:
    args = parse_args()
    pydarts.configure_logging(args.enable_debug)
    if args.show_version:
        print(pydarts.__version__)
        return None
    app = App(args.enable_debug)
    app.mainloop()
    return None


if __name__ == "__main__":
    main()
