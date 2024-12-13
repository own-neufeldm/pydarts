from . import BaseMode


class Mode(BaseMode):
    options = {
        "Double out": False,
    }

    @classmethod
    def get_name(cls) -> str:
        return "701"

    @classmethod
    def get_description(cls) -> str:
        return (
            "All players start with 701 points, the goal is to reach 0."
        )

    @classmethod
    def get_initial_score(cls) -> int:
        return 701
