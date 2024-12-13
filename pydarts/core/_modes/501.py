from . import BaseMode


class Mode(BaseMode):
    options = {
        "Double in": False,
    }

    @classmethod
    def get_name(cls) -> str:
        return "501"

    @classmethod
    def get_description(cls) -> str:
        return (
            "All players start with 501 points, the goal is to reach 0."
        )

    @classmethod
    def get_initial_score(cls) -> int:
        return 501
