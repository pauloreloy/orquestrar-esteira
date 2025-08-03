import enum

class LogLevel(enum.Enum):
    DEBUG       = "DEBUG"
    INFO        = "INFO"
    WARNING     = "WARNING"
    ERROR       = "ERROR"
    CRITICAL    = "CRITICAL"

    def __str__(self):
        return self.value

    @staticmethod
    def from_str(name: str):
        try:
            return LogLevel[name.upper()]
        except KeyError:
            raise ValueError(f"Invalid log level: {name}")