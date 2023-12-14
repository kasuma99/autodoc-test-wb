from dataclasses import dataclass


@dataclass
class LogMinor:
    status: str
    log: str
    error_type: str
