from . import BaseMode


class Mode(BaseMode):
    options = {
        "Double in": False,
        "Double out": False,
    }

    @classmethod
    def get_name(cls) -> str:
        return "301"

    @classmethod
    def get_description(cls) -> str:
        return (
            "All players start with 301 points, the goal is to reach 0."
        )

    @classmethod
    def get_initial_score(cls) -> int:
        return 301
