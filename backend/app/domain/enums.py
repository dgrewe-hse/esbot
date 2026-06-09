"""Domain enumerations."""

from enum import StrEnum


class MessageRole(StrEnum):
    """Role of a message in a learning session."""

    USER = "user"
    ASSISTANT = "assistant"
