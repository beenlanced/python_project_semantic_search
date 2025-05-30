"""
Custom Exceptions 
"""


class DataIngestionError(Exception):
    """
    Base exception for all data ingestion related errors

    Attributes:
        message -- explanation of the error
    """
    default_message = "A data ingestion related error occurred"

    def __init__(self, message: str) -> None:
        super().__init__(message or self.default_message)

    def __str__(self):
        return f"{self.message}"


class NoVideoDataError(DataIngestionError):
    """Raised when a page token does not exist. """
    def __init__(self, message: str, channel_id: str) -> None:
        super().__init__(message)
        self.channel_id = channel_id
        self.message = message

    def __str__(self) -> str:
        return f"{self.message} for YouTube Channel id - {self.channel_id})"