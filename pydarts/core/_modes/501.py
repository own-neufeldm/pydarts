from . import BaseMode


class Mode(BaseMode):
    def __init__(self) -> None:
        super().__init__()
        return None

    @classmethod
    def get_name(cls) -> str:
        return "501"

    @classmethod
    def get_description(cls) -> str:
        return (
            "All players start with 501 points, the goal is to reach 0."
        )

    @classmethod
    def get_options(cls) -> list[str]:
        return [
            "Double in",
        ]

    @classmethod
    def get_initial_score(cls) -> int:
        return 501
