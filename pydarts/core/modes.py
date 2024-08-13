class BaseMode():
    def __init__(self) -> None:
        return None

    @classmethod
    def get_name(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def get_description(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def get_options(cls) -> list[str]:
        raise NotImplementedError()

    @classmethod
    def get_initial_score(cls) -> int:
        raise NotImplementedError()


class Mode301(BaseMode):
    def __init__(self) -> None:
        super().__init__()
        return None

    @classmethod
    def get_name(cls) -> str:
        return "301"

    @classmethod
    def get_description(cls) -> str:
        return (
            "All players start with 301 points, the goal is to reach 0."
        )

    @classmethod
    def get_options(cls) -> list[str]:
        return [
            "Double in",
            "Double out",
        ]

    @classmethod
    def get_initial_score(cls) -> int:
        return 301


class Mode501(BaseMode):
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
            "Double out",
        ]

    @classmethod
    def get_initial_score(cls) -> int:
        return 501


class Mode701(BaseMode):
    def __init__(self) -> None:
        super().__init__()
        return None

    @classmethod
    def get_name(cls) -> str:
        return "701"

    @classmethod
    def get_description(cls) -> str:
        return (
            "All players start with 701 points, the goal is to reach 0."
        )

    @classmethod
    def get_options(cls) -> list[str]:
        return [
            "Double in",
            "Double out",
        ]

    @classmethod
    def get_initial_score(cls) -> int:
        return 701
