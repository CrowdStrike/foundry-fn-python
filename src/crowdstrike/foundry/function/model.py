"""Data models for CrowdStrike Foundry Function FDK."""
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class RequestParams:
    """Defines the data model for request parameters."""

    header: Dict[str, List[str]] = field(default_factory=lambda: {})
    query: Dict[str, List[str]] = field(default_factory=lambda: {})


@dataclass
class APIError:
    """Defines the data model for API errors."""

    code: int = field(default=0)
    message: str = field(default='')


@dataclass
class Request:
    """Defines the data model for request provided to the function handler."""

    access_token: str = field(default='')
    body: Dict[str, Any] = field(default_factory=lambda: {})
    context: Dict[str, Any] = field(default_factory=lambda: {})
    files: Dict[str, bytes] = field(default_factory=lambda: {})
    fn_id: str = field(default='')
    fn_version: int = field(default=0)
    method: str = field(default='')
    params: RequestParams = field(default_factory=lambda: RequestParams())
    trace_id: str = field(default='')
    url: str = field(default='')


@dataclass
class Response:
    """Defines the data model for response returned from the function handler."""

    body: Dict[str, Any] = field(default_factory=lambda: {})
    code: int = field(default=0)
    errors: List[APIError] = field(default_factory=lambda: [])
    header: Dict[str, List[str]] = field(default_factory=lambda: {})


class FDKException(Exception):
    """Defines the FDKException that will be raised when an error occurs."""

    def __init__(self, code: int, message: str):
        """Initialize the FDKException.

        :param code: The error code.
        :param message: The error message.
        """
        Exception.__init__(self, message)
        self.code = code
        self.message = message
