import os
from crowdstrike.foundry.function.context import ctx_request
from falconpy import ServiceClass
from typing import Type


def falcon_client(client_class: Type) -> ServiceClass:
    """
    Returns an instance of a FalconPy client.
    :param client_class: Class which extends :class:`falconpy.ServiceClass`.
    :return: Initialized instance of the client_class.
    """
    _cloud_default = 'auto'
    if not issubclass(client_class, ServiceClass):
        msg = f'provided class {client_class.__name__} does not extend falconpy.ServiceClass'
        raise TypeError(msg)

    req = ctx_request.get()
    if req is None:
        msg = 'the falcon_client() convenience method requires a request be present'
        raise AssertionError(msg)

    access_token = req.access_token
    if access_token is None or type(access_token) is not str or access_token.strip() == '':
        msg = 'request must have an access token to use the falcon_client()'
        raise AssertionError(msg)

    cloud = os.environ.get('CS_CLOUD', _cloud_default)
    cloud = cloud.lower().replace('-', '').strip()
    if cloud == '':
        cloud = _cloud_default
    client = client_class(access_token=access_token, base_url=cloud)
    return client
