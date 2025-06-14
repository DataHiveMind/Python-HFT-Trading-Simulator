import logging
from typing import Optional

class SimLogger:
    _logger: Optional[logging.Logger] = None

    @classmethod
    def setup(
        cls,
        name: str = "Simulator",
        level: int = logging.INFO,
        log_to_file: bool = False,
        filename: str = "simulation.log"
    ):
        """Configure the central logger."""
        cls._logger = logging.getLogger(name)
        cls._logger.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s][%(name)s] %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        # Remove existing handlers
        cls._logger.handlers.clear()

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        cls._logger.addHandler(ch)

        # Optional file handler
        if log_to_file:
            fh = logging.FileHandler(filename)
            fh.setFormatter(formatter)
            cls._logger.addHandler(fh)

    @classmethod
    def info(cls, msg: str):
        if cls._logger:
            cls._logger.info(msg)

    @classmethod
    def debug(cls, msg: str):
        if cls._logger:
            cls._logger.debug(msg)

    @classmethod
    def error(cls, msg: str):
        if cls._logger:
            cls._logger.error(msg)

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            cls.setup()
        return cls._logger

# Example usage:
# SimLogger.setup(level=logging.DEBUG, log_to_file=True)
# SimLogger.info("Simulation started.")
# SimLogger.debug("Order book updated.")
# SimLogger.error("Order rejected due to risk limits.")
