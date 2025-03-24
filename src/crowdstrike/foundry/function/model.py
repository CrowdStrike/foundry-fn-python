from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class RequestParams:
    header: Dict[str, List[str]] = field(default_factory=lambda: {})
    query: Dict[str, List[str]] = field(default_factory=lambda: {})


@dataclass
class APIError:
    code: int = field(default=0)
    message: str = field(default='')


@dataclass
class Request:
    access_token: str = field(default='')
    body: Dict[str, any] = field(default_factory=lambda: {})
    context: Dict[str, any] = field(default_factory=lambda: {})
    files: Dict[str, bytes] = field(default_factory=lambda: {})
    fn_id: str = field(default='')
    fn_version: int = field(default=0)
    method: str = field(default='')
    params: RequestParams = field(default_factory=lambda: RequestParams())
    trace_id: str = field(default='')
    url: str = field(default='')


@dataclass
class Response:
    body: Dict[str, any] = field(default_factory=lambda: {})
    code: int = field(default=0)
    errors: List[APIError] = field(default_factory=lambda: [])
    header: Dict[str, List[str]] = field(default_factory=lambda: {})


class FDKException(Exception):

    def __init__(self, code: int, message: str):
        Exception.__init__(self, message)
        self.code = code
        self.message = message
