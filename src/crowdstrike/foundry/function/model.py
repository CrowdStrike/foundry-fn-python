import json
from contextvars import ContextVar
from dataclasses import (
    dataclass,
    field,
    fields,
    is_dataclass,
)
from typing import (
    Any,
    Dict,
    List,
)

# <request context> ============================================================

# While this holds the inbound handler request, do not access them directly
# without good reason.  This is intended for those situations in which
# it is not possible to pass the inbound request around the handler via method
# arguments, such as in logging.

# Holds the inbound handler request after the payload has been converted from
# a dict to a Request.
ctx_request = ContextVar('request', default=None)


# =========================================================== </request context>

def map_dict_to_dataclass(d: Dict, dc) -> [None, dataclass]:
    """
    Maps the contents of a dictionary to a dataclass object.
    :param d: Dictionary from which to extract values.
    :param dc: Dataclass to receive the values.
    :return: Provided dataclass object.
    """
    if not is_dataclass(dc):
        raise TypeError(f'provided argument dc is of type {type(dc)} instead of dataclass')
    if d is None:
        return dc

    for f in fields(dc):
        d_key = f.name
        if len(f.metadata) > 0:
            k = f.metadata.get('key', '')
            if k != '':
                d_key = k

        d_value = d.get(d_key, None)
        if d_value is not None:
            setattr(dc, f.name, d_value)

    return dc


@dataclass
class APIError:
    """
    API error code and message pair.
    """
    code: int = field(default=0)
    message: str = field(default='')

    def to_dict(self) -> Dict[str, Any]:
        """
        Coverts this :class:`APIError` to a JSON serializable dict.
        :return: Dictionary consisting of the code and the message.
        """
        return {
            'code': self.code,
            'message': self.message,
        }


@dataclass
class Params:
    """
    HTTP-esk parameters for the FDK request, including a headers map and query parameters.
    """
    header: Dict[str, List[str]] = field(default_factory=lambda: {})
    query: Dict[str, List[str]] = field(default_factory=lambda: {})


@dataclass
class Request:
    """
    SDK request as a dataclass.
    """
    access_token: str = field(default='')
    body: Dict = field(default_factory=lambda: {})
    context: Dict[str, Any] = field(default_factory=lambda: {})
    method: str = field(default='')
    params: Params = field(default_factory=lambda: Params())
    url: str = field(default='')

    @staticmethod
    def from_json_payload(payload: str) -> 'Request':
        """
        Generates a new :class:`Request` instance from a JSON string.
        :param payload: String to deserialize.
        :return: Populated :class:`Request` instance.
        """
        req_dict = json.loads(payload)
        req = map_dict_to_dataclass(req_dict, Request())
        req.params = map_dict_to_dataclass(req_dict.get('params', None), Params())
        return req


@dataclass
class Response:
    """
    SDK response as a dataclass.
    """
    body: Dict = field(default_factory=lambda: {})
    code: [int, None] = field(default_factory=lambda: None)
    errors: List[APIError] = field(default_factory=lambda: [])
    headers: Dict[str, List[str]] = field(default_factory=lambda: {})
    trace_id: str = field(default='')
