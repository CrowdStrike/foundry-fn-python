from crowdstrike.foundry.function.model import Request, RequestParams, Response
from dataclasses import dataclass, fields, is_dataclass
from typing import Dict


def response_to_dict(r: Response) -> Dict:
    """
    Converts a :class:`Response` to a dictionary.
    :param r: :class:`Response` instance to convert.
    :return: Dictionary version of the provided instance.
    """
    body = r.body
    errors = []
    header = {}

    if r.errors is not None:
        for e in r.errors:
            errors.append({'code': e.code, 'message': e.message})
    if r.header is not None:
        header = r.header

    d = {'code': r.code}
    if body is not None:
        d['body'] = body
    if len(errors) > 0:
        d['errors'] = errors
    if len(header) > 0:
        d['header'] = header

    return d


def dict_to_request(d: Dict) -> Request:
    """
    Converts a dictionary to a :class:`Request`.
    :param d: Dictionary instance to attempt to map.
    :return: :class:`Request` instance populated by the given dictionary.
    """
    req = dict_to_dataclass(d, Request())
    req.params = dict_to_dataclass(d.get('params', None), RequestParams())
    if req.params.header is not None and len(req.params.header) > 0:
        h = {}
        for k, v in req.params.header.items():
            h[canonize_header(k)] = v
        req.params.header = h
    return req


def dict_to_dataclass(d: Dict, dc) -> [None, dataclass]:
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


def canonize_header(h: str) -> str:
    """
    Converts a header key into its canonical version.
    :param h: Header key.
    :return: Canonized version.
    """
    canon = ''
    upper = True
    for c in h:
        if upper:
            canon += c.upper()
        else:
            canon += c.lower()

        upper = c == '-'
    return canon
