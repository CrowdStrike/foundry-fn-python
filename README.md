![CrowdStrike Falcon](/docs/asset/cs-logo.png?raw=true)

# Foundry Function as a Service Python SDK

`foundry-fn-python` is a community-driven, open source project designed to enable the authoring of functions.
While not a formal CrowdStrike product, `foundry-fn-python` is maintained by CrowdStrike and supported in partnership
with the open source developer community.

## Installation ⚙️

### Via `pip`

The SDK can be installed or updated via `pip install`:

```shell
python3 -m pip install crowdstrike-foundry-fn-python
```

## Quickstart 💫

### Code

Add the SDK to your project by following the [installation](#installation) instructions above,
then create your `handler.py`:

```python
import http
from crowdstrike.foundry.function import (
    CSHandler,
    HandlerBase,
    Request,
    Response,
    run,
)


class Handler(HandlerBase):  # *** (1) ***

    def handler_init(self):  # *** (2) ***
        msg = f'initializing using configuration: {self.config()}'  # *** (3) ***
        self.logger().info(msg)  # *** (4) ***

    # *** (5) ***
    def handle(self, request: Request) -> Response:  # *** (6) ***
        body = {
            'body': request.body,
            'context': request.context,
            'method': request.method,
            'url': request.url,
        }

        return Response(  # *** (7) ***
            body=body,
            code=http.HTTPStatus.OK,
        )


if __name__ == '__main__':  # *** (8) ***
    CSHandler.bootstrap(Handler)
    run()
```

1. `Handler(HandlerBase)`: Class containing the function's code.
   The `Handler` class must extend `HandlerBase`, must be present in `handler.py`, and should not have an `__init__`
   method.
   If an `__init__` method is provided, it will be overridden internally as the framework constructs the handler.
2. `handler_init`: Initialization and bootstrapping method.
   The framework will invoke the `handler_init` following construction and basic initialization of the handler;
   invocation occurs exactly once at the start of the runtime.
   Implementing this function is optional and may be removed from the handler if no custom bootstrapping or setup is
   needed.
3. `self.config()`: Configuration dictionary of type `dict[str, Any]`.
   This is populated as part of the bootstrapping process and is accessible within both `handler_init` and `handle`.
   The same instance of the dictionary is returned on each invocation of this method.
4. `self.logger()`: Contextual `logging.Logger` instance.
   While the author is free to implement or import their own logger, the framework provides a version of `Logger`
   which outputs (in production) in JSON format and decorates the output with valuable contextual information.
   It is recommended that function authors use the provided `Logger` unless they have good reason not to.
5. `handle()`: Called once on each inbound request. The business logic of the function should exist here.
6. `request`: Request payload and metadata. At the time of this writing, the `Request` object consists of:
    1. `body`: The request payload as given in the Function Gateway `body` payload field. Will be deserialized as
       a `dict[str, Any]`.
    2. `params`: Contains request headers and query parameters.
    3. `url`: The request path relative to the function as a string.
    4. `method`: The request HTTP method or verb.
    5. `context`: Caller-supplied raw context.
    6. `access_token`: Caller-supplied access token.
7. Return from `handle()`: Returns a `Response` object.
   The `Response` object contains fields `body` (payload of the response as a `dict`),
   `code` (an `int` representing an HTTP status code or a member of `http.HTTPStatus`),
   `errors` (a list of any `APIError`s), and `headers` (a `dict[str, list[str]]` of any special HTTP headers which
   should be present on the response).
8. `if __name__ == '__main__': ...`: Enables local testing of the function.
   Code placed in this block only serves to enable the author to run their function locally and is ignored in
   production.

### Testing locally

The SDK provides an out-of-the-box runtime for executing the function.
A basic HTTP server will be listening on port 8081.

```shell
cd my-project && python3 handler.py
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
    "url": "/echo"
}'
```

## Convenience Functionality 🧰

### `falconpy`

Foundry Function Python ships with [falconpy](https://github.com/CrowdStrike/falconpy) pre-integrated and a convenience constructor.
While it is not strictly necessary to use the convenience function, it is recommended.

**Important:** Create a new instance of each `falconpy` client you want on each request.

```python
# omitting other imports
from falconpy.alerts import Alerts
from falconpy.event_streams import EventStreams
from crowdstrike.foundry.function.falconpy import falcon_client


class Handler(HandlerBase):

    def handle(self, request: Request) -> Response:
        # ... omitting other code ...

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!! create a new client instance on each request !!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        alerts_client = falcon_client(Alerts)
        event_streams_client = falcon_client(EventStreams)

        # ... omitting other code ...
```
---


<p align="center"><img src="https://raw.githubusercontent.com/CrowdStrike/falconpy/main/docs/asset/cs-logo-footer.png"><BR/><img width="250px" src="https://raw.githubusercontent.com/CrowdStrike/falconpy/main/docs/asset/adversary-red-eyes.png"></P>
<h3><P align="center">WE STOP BREACHES</P></h3>
