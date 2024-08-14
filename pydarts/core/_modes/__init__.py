class BaseMode():
    def __init__(self) -> None:
        raise NotImplementedError()

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
