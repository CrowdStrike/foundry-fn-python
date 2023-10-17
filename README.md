![CrowdStrike Falcon](https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/cs-logo.png)

# Foundry Function as a Service Python SDK

`foundry-fn-python` is a community-driven, open source project designed to enable the authoring of functions.
While not a formal CrowdStrike product, `foundry-fn-python` is maintained by CrowdStrike and supported in partnership
with the open source developer community.

## Installation ⚙️

### Via `pip`

The SDK can be installed or updated via `pip install`:

```shell
python3 -m pip install crowdstrike-foundry-function
```

## Quickstart 💫

### Code

Add the SDK to your project by following the [installation](#installation) instructions above,
then create your `handler.py`:

```python
import logging
from crowdstrike.foundry.function import (
    APIError,
    Request,
    Response,
    Function,
)

func = Function.instance()  # *** (1) ***


@func.handler(method='POST', path='/create')  # *** (2) ***
def on_create(request: Request, logger: logging.Logger, config: [dict[str, any], None]) -> Response:  # *** (3), (4) ***
    if len(request.body) == 0:
        return Response(
            code=400,
            errors=[APIError(code=400, message='empty body')]
        )

    #####
    # do something useful
    #####

    return Response(  # *** (5) ***
        body={'hello': 'world'},
        code=200,
    )


if __name__ == '__main__':
    func.run()  # *** (6) ***
```

1. `Function`: The `Function` class wraps the Foundry Function implementation.
   Each `Function` instance consists of a number of handlers, with each handler corresponding to an endpoint.
   Only one `Function` should exist per Python implementation.
   Multiple `Function`s will result in undefined behavior.
2. `@func.handler`: The handler decorator defines a Python function/method as an endpoint.
   At a minimum, the `handler` must have a `method` and a `path`.
   The `method` must be one of `DELETE`, `GET`, `PATCH`, `POST`, and `PUT`.
   The `path` corresponds to the `url` field in the request.
   The SDK will provide a `logging.Logger` instance and any loaded configuration.
3. Methods decorated with `@handler` must take arguments in the order of `Request`, `logging.Logger`, and `dict|None`
   (i.e. the request, the logger, and either the configuration or nothing; see example above),
   and must return a `Response`.
4. `request`: Request payload and metadata. At the time of this writing, the `Request` object consists of:
    1. `body`: The request payload as given in the Function Gateway `body` payload field. Will be deserialized as
       a `dict[str, Any]`.
    2. `params`: Contains request headers and query parameters.
    3. `url`: The request path relative to the function as a string.
    4. `method`: The request HTTP method or verb.
    5. `access_token`: Caller-supplied access token.
5. Return from a `@handler` function: Returns a `Response` object.
   The `Response` object contains fields `body` (payload of the response as a `dict`),
   `code` (an `int` representing an HTTP status code),
   `errors` (a list of any `APIError`s), and `header` (a `dict[str, list[str]]` of any special HTTP headers which
   should be present on the response).
   If no `code` is provided but a list of `errors` is, the `code` will be derived from the greatest positive valid HTTP
   code present on the given `APIError`s.
6. `func.run()`: Runner method and general starting point of execution.
   Calling `run()` causes the `Function` to finish initializing and start executing.
   Any code declared following this method may not necessarily be executed.
   As such, it is recommended to place this as the last line of your script.

### Testing locally

The SDK provides an out-of-the-box runtime for executing the function.
A basic HTTP server will be listening on port 8081.

```shell
cd my-project && python3 main.py
```

Requests can now be made against the executable.

```shell
curl -X POST 'http://localhost:8081' \
  -H 'Content-Type: application/json' \
  --data '{
    "body": {
        "foo": "bar"
    },
    "method": "POST",
    "url": "/create"
}'
```

## Convenience Functionality 🧰

### `falconpy`

Foundry Function Python ships with [falconpy](https://github.com/CrowdStrike/falconpy) pre-integrated and a convenience
constructor.
While it is not strictly necessary to use the convenience function, it is recommended.

**Important:** Create a new instance of each `falconpy` client you want on each request.

```python
# omitting other imports
from falconpy.alerts import Alerts
from falconpy.event_streams import EventStreams
from crowdstrike.foundry.function import falcon_client, Function

func = Function.instance()


@func.handler(...)
def endpoint(request, logger, config):
    # ... omitting other code ...
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!! create a new client instance on each request !!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    alerts_client = falcon_client(Alerts)
    event_streams_client = falcon_client(EventStreams)

    # ... omitting other code ...
```

---


<p align="center"><img src="https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/cs-logo-footer.png"><BR/><img width="250px" src="https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/adversary-red-eyes.png"></P>
<h3><P align="center">WE STOP BREACHES</P></h3>
