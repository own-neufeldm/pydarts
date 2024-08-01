class BaseMode():
    def __init__(self) -> None:
        return None

    @classmethod
    def get_name(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def get_description(cls) -> str:
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
            "lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam "
            "nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam "
            "erat, sed diam voluptua. at vero eos et accusam et justo duo "
            "dolores et ea rebum. stet clita kasd gubergren, no sea takimata "
            "sanctus est lorem ipsum dolor sit amet. lorem ipsum dolor sit "
            "amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor "
            "invidunt ut labore et dolore magna aliquyam erat, sed diam "
            "voluptua. at vero eos et accusam et justo duo dolores et ea rebum. "
            "stet clita kasd gubergren, no sea takimata sanctus est lorem ipsum "
            "dolor sit amet."
        )


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
            "LOREM IPSUM DOLOR SIT AMET, CONSETETUR SADIPSCING ELITR, SED DIAM "
            "NONUMY EIRMOD TEMPOR INVIDUNT UT LABORE ET DOLORE MAGNA ALIQUYAM "
            "ERAT, SED DIAM VOLUPTUA. AT VERO EOS ET ACCUSAM ET JUSTO DUO "
            "DOLORES ET EA REBUM. STET CLITA KASD GUBERGREN, NO SEA TAKIMATA "
            "SANCTUS EST LOREM IPSUM DOLOR SIT AMET. LOREM IPSUM DOLOR SIT "
            "AMET, CONSETETUR SADIPSCING ELITR, SED DIAM NONUMY EIRMOD TEMPOR "
            "INVIDUNT UT LABORE ET DOLORE MAGNA ALIQUYAM ERAT, SED DIAM "
            "VOLUPTUA. AT VERO EOS ET ACCUSAM ET JUSTO DUO DOLORES ET EA REBUM. "
            "STET CLITA KASD GUBERGREN, NO SEA TAKIMATA SANCTUS EST LOREM IPSUM "
            "DOLOR SIT AMET."
        )
