import logging
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

assets_dir = Path(__file__).parent / "assets"
logger: logging.Logger
try:
    __version__ = version(str(__package__))
except PackageNotFoundError:
    # package is not installed
    pass


def configure_logging(enable_debug: bool) -> None:
    """
    Configure package-level logging.
    """
    global logger
    logger = logging.getLogger(__package__)
    level = logging.DEBUG if enable_debug else logging.INFO
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    return None
