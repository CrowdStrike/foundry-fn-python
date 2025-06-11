<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/CrowdStrike/falconpy/main/docs/asset/cs-logo-red.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/CrowdStrike/falconpy/main/docs/asset/cs-logo.png">
  <img alt="CrowdStrike Logo." src="https://raw.githubusercontent.com/CrowdStrike/falconpy/main/docs/asset/cs-logo-red.png">
</picture>

# Falcon Foundry Function as a Service Python FDK

`foundry-fn-python` is a community-driven, open source project designed to enable the authoring of functions.
While not a formal CrowdStrike product, the `foundry-fn-python` project and the `crowdstrike-foundry-function` FDK package are maintained by CrowdStrike and supported in partnership with the open source developer community.

## Installation ⚙️

### Installation via `pip`

The FDK can be installed or updated via `pip install`:

```shell
python3 -m pip install crowdstrike-foundry-function
```

## Quickstart 💫

### Example Code

Add the FDK to your project by following the [installation](#installation) instructions above,
then create your `main.py` that contains your handler implementation:

```python
from crowdstrike.foundry.function import (
    APIError,
    Request,
    Response,
    Function,
)


func = Function.instance()

# An example POST handler
@func.handler(method='POST', path='/my-resource')
def on_post(request: Request) -> Response:

    # Validate the request body
    if 'name' not in request.body:
        # This example expects 'name' field in the request body.
        # Return an error response (400 - Bad Request) if not provided by the caller
        return Response(
            code=400,
            errors=[APIError(code=400, message='name field is missing from request body')]
        )

    # Process the request
    new_resource_id = 1
    # ...snip...

    # Return a success response
    return Response(
        body={
           'result': f'Resource with name {request.body["name"]} is created.',
           'id': new_resource_id
        },
        code=200,
    )


if __name__ == '__main__':
    func.run()
```

### Example breakdown

#### The Function object
The `Function` class wraps the Foundry Function implementation. A `Function` instance can consist of one or more handlers, with each corresponding to an endpoint. You should only have one `Function` object defined per function implemented within your Foundry application. Multiple instances will result in unexpected behavior.

```python
func = Function.instance()
```

#### The function handler decorator
The handler decorator defines a Python method as handler for a specific endpoint. This handler must have the `method` and `path` keywords defined. The `method` keyword will correspond to one of the supported HTTP methods (`GET`, `POST`, `PUT`, `PATCH` or `DELETE`). The `path` keyword will define the URL used to trigger this method, and should be unique.

```python
@func.handler(method='POST', path='/my-resource')
```

#### Method details - Request
Our python handler function is decorated with `@func.handler`. The first argument to our method must be a `Request` object which defines the HTTP request payload and metadata.

A `Request` object consists of:

* `body`: The request payload as given in the Function Gateway `body` payload field. This will be deserialized as a dictionary (`dict[str, Any]`).
* `params`: The request headers (`params.header`) and query string parameters (`params.query`).
* `url`: The request path relative to the function. This is a string.
* `method`: The request HTTP method or verb.
* `access_token`: Caller-supplied access token.

In this example we've named our method `on_post`, but you may name the method whatever you wish.

```python
def on_post(request: Request) -> Response:
```

#### Method details - Response
The return type for our method should be a `Response` object.

##### Successful responses
A successful response will be a `Response` object containing the fields `body` (a dictionary containing the response returned to the function) and `code` (the HTTP status code returned to the function).

```python
# Return a success response
return Response(
    body={
        'result': f'Resource with name {request.body["name"]} is created.',
        'id': new_resource_id
    },
    code=200,
)
```

##### Error responses
An unsuccessful response will be a `Response` object containing the fields `errors` (a list of `APIError` objects) and `code` (the HTTP status code returned to the function).

An `APIError` object will contain a `code` indicating the type of the error and a `message` which should contain the error text.

If no `code` is provided as part of the `Response` object, this value will be derived from the greatest valid HTTP code present within the `APIError` list.

```python
return Response(
    code=400,
    errors=[APIError(code=400, message='id field is missing from request params')]
)
```

#### Running the function
The runner method is the general starting point for execution of your function and will be executed when your code is called by Foundry. This causes the `Function` to initialize and start execution. This should be the last line of your script as code defined after the `func.run()` statement may not be executed. You may implement code before this statement as necessary.

```python
if __name__ == '__main__':
    func.run()
```

#### Retrieving parameters passed to your Function
You may retrieve query string values passed to your function by accessing the `request.params.query` dictionary.

```python
resource_id = request.params.query.get("id")
```


#### Additional HTTP method examples
Different types of HTTP requests will follow the same pattern demonstrated in our `POST` request above.

##### HTTP GET

```python
from crowdstrike.foundry.function import (
    APIError,
    Request,
    Response,
    Function,
)


func = Function.instance()

# An example GET handler
@func.handler(method='GET', path='/my-resource')
def on_get(request: Request) -> Response:

    # Fetch the requested resources
    resources = []
    # ...snip...

    # Return the requested resources
    return Response(
        body={'resources': resources},
        code=200,
    )


if __name__ == '__main__':
    func.run()
```

##### HTTP PUT

```python
from crowdstrike.foundry.function import (
    APIError,
    Request,
    Response,
    Function,
)


func = Function.instance()

# An example PUT handler
@func.handler(method='PUT', path='/my-resource')
def on_put(request: Request) -> Response:

    # Obtain the id of the resource to update from the request query parameters
    resource_id = request.params.query.get('id')
    if not resource_id:
        # This example expects 'id' field in the request query parameters.
        # Returns an error response (400 - Bad Request) if not provided by the caller
        return Response(
            code=400,
            errors=[APIError(code=400, message='id field is missing from request params')]
        )

    # Get the update data provided in the request body and
    # Update the resource with the data provided
    data = request.body.get('data')
    # ...snip...

    # Return success with the updated resource info
    return Response(
        body={
           'result': f'Resource {resource_id} is updated successfully.',
           'data': data
        },
        code=200,
    )


if __name__ == '__main__':
    func.run()
```

##### HTTP DELETE

```python
from crowdstrike.foundry.function import (
    APIError,
    Request,
    Response,
    Function,
)


func = Function.instance()

# An example DELETE handler
@func.handler(method='DELETE', path='/my-resource')
def on_delete(request: Request) -> Response:

    # Obtain the id of the resource to update from the request query parameters
    resource_id = request.params.query.get('id')
    if not resource_id:
        # This example expects 'id' field in the request query parameters.
        # Returns an error response (400 - Bad Request) if not provided by the caller
        return Response(
            code=400,
            errors=[APIError(code=400, message='id field is missing from request params')]
        )

    # Delete the requested resource
    # ...snip...

    # Return success back to the caller
    return Response(
        code=200,
    )


if __name__ == '__main__':
    func.run()
```


### Testing locally

The FDK provides an out-of-the-box runtime for executing the function.

#### Executing your code
> [!NOTE]
> A basic HTTP server will be started to listen on port 8081 when executing your code locally.

```shell
cd my-project
python3 main.py
```

You can use `curl` or another python application to make requests to the web server that has been started.

##### Example POST request

```shell
# Test POST /my-resource request
curl --location 'http://localhost:8081' \
  -H 'Content-Type: application/json' \
  --data '{
    "body": {
        "name": "bar"
    },
    "method": "POST",
    "url": "/my-resource"
}'
```

##### Example GET request

```shell
# Test GET /my-resource request
curl --location 'http://localhost:8081' \
  -H 'Content-Type: application/json' \
  --data '{
    "method": "GET",
    "url": "/my-resource"
}'
```

##### Example PUT request

```shell
# Test PUT /my-resource request
curl --location 'http://localhost:8081' \
  -H 'Content-Type: application/json' \
  --data '{
    "body": {
        "name": "bar",
    },
    "params": {
        "query": {
          "id": "12345"
        }
    },
    "method": "PUT",
    "url": "/my-resource"
}'
```

##### Example DELETE request

```shell
# Test DELETE /my-resource request
curl --location 'http://localhost:8081' \
  -H 'Content-Type: application/json' \
  --data '{
    "params": {
        "query": {
          "id": "12345"
        }
    },
    "method": "DELETE",
    "url": "/my-resource"
}'
```

#### Executing your code without an HTTP server

If you prefer to test your function locally without starting an HTTP server, you can provide the request payload in a JSON file on the command line.

First, create a JSON file containing your request payload.
Example `request_payload.json` file:
```shell
{
    "body": {
        "name": "bar"
    },
    "method": "POST",
    "url": "/my-resource"
}
```

Then invoke your function handler as follows:

```shell
python3 main.py --data ./request_payload.json
```

This will execute the requested function handler and print the response returned, including the response status code, body and headers.

You can also provide request headers to your function on the command line:
```shell
python3 main.py --data request_payload.json --header "Content-Type: application/json" --header "X-CUSTOM-HEADER: testing"
```

## Leveraging the FalconPy SDK to interact with CrowdStrike APIs inside of your Foundry function
Foundry function authors should include `crowdstrike-falconpy` within their _requirements.txt_ file and then import `falconpy` explicitly in their function code.

You may use any [FalconPy Service Class](https://falconpy.io/Home.html#service-collections) or the [FalconPy Uber Class](https://falconpy.io/Usage/Basic-Uber-Class-usage.html) within your function.

### General FalconPy usage information
FalconPy implements [Context Authentication](https://falconpy.io/Usage/Authenticating-to-the-API.html#context-authentication) for use within Foundry Functions, removing the need for developers to provide their `access_token` to the class as this value is provided by context when the function is executed.

> [!TIP]
> If you are instantiating a FalconPy class within your method, you will need to do this for every method you implement. If you instantiate the FalconPy class outside of your method, but before the `func.run()` statement, this object will be available to all methods defined in your function code.

To test the function locally without having to adjust your code, you can set the following environment variables in your local environment:

| Variable Name | Purpose |
| :--- | :--- |
| `FALCON_CLIENT_ID`     | CrowdStrike Falcon API client ID     |
| `FALCON_CLIENT_SECRET` | CrowdStrike Falcon API client secret |


#### FalconPy usage example
```python

from falconpy import Hosts
from crowdstrike.foundry.function import (
    Function,
    Request,
    Response,
    APIError
)


func = Function.instance()


@func.handler(method='POST', path='/hosts-query')
def on_hosts_query(request: Request) -> Response:

    # get the requested Host IDs from the request body
    host_ids = request.body.get("ids")
    if not host_ids:
       return Response(
            code=400,
            errors=[APIError(code=400, message='Required host ids are not provided')]
        )

    # Initialize falconpy client for Hosts API
    # This example uses context authentication
    hosts_client = Hosts()

    # Call falconpy API to fetch the details of the requested hosts
    api_result = hosts_client.get_device_details_v1(ids=host_ids)
    if api_result['status_code'] != 200:
        # falconpy API returned an error
        response = Response(
           code=api_result['status_code'],
            errors=[
               APIError(code=api_result['status_code'], message="falconpy API call failed")
            ]
        )
    else:
       # falconpy API was successful, return the requested data
        response = Response(
            body={
                'hosts': api_result['body']['resources']
            },
            code=200
        )

    return response

if __name__ == '__main__':
    func.run()
```

## Using custom configurations and debug logging
Foundry supports custom configurations and debug logging to support developers with the implementation of their functions.

### Implementing custom configurations
Using a custom configuration within a function is optional and may be provided as a JSON file. This functionality is intended to give the developer a location to store custom configuration data, such as API keys and credentials, in a secure manner when the function is deployed on Falcon platform.

> [!NOTE]
> The configuration is encrypted with a unique key per function in the cloud.

To utilize a custom configuration within a function, include the `config` keyword argument as shown in the example below.

The `config` keyword is an optional argument to the handler function and must be the second argument if provided.

### Enabling logging
Logging for a function is optional but adding log messages to functions can make triage and debugging easier when troubleshooting problems. When a function is deployed on the Falcon platform, the messages logged with the provided `logger` are formatted in a custom manner with fields injected to assist with working within the Falcon logging infrastructure.

> [!NOTE]
> You may use native [FalconPy logging](https://falconpy.io/Usage/Logging.html) in conjunction with your function logger config by providing the `debug` keyword when you instantiate your FalconPy class.

To utilize logging in a function, include the `logger` parameter as shown in the example below.

`logger` is an optional parameter to the handler function and must the third parameter if provided.


```python
from logging import Logger
from typing import Union, Any
from falconpy import Hosts
from crowdstrike.foundry.function import (
    Function,
    Request,
    Response,
    APIError
)


func = Function.instance()


@func.handler(method='POST', path='/hosts-query')
def on_hosts_query(request: Request, config: Union[dict[str, Any], None], logger: Logger) -> Response:

    logger.info("POST handler for /hosts-query is invoked")

    # get the requested Host IDs from the request body
    host_ids = request.body.get("ids")
    if not host_ids:
       logger.error("ids argument is missing from request parameters")
       return Response(
            code=400,
            errors=[APIError(code=400, message='Required host ids are not provided')]
        )

    # Example config provided to the function
    action = "Dev resource update"
    if config and config.get("is_production", False):
        action = "Production resource update"

    # Initialize falconpy client for Hosts API and enable debugging
    hosts_client = Hosts(debug=True)

    # Call falconpy API to fetch the details of the requested hosts
    api_result = hosts_client.get_device_details_v1(ids=host_ids)
    if api_result['status_code'] != 200:
        # FalconPy SDK returned an error
        response = Response(
           code=api_result['status_code'],
            errors=[
               APIError(code=api_result['status_code'], message="FalconPy API call failed")
            ]
        )
    else:
       # falconpy API was successful, return the requested data
        response = Response(
            body={
                'hosts': api_result['body']['resources'],
                'action': action
            },
            code=200
        )

    return response

if __name__ == '__main__':
    func.run()
```


---


<p align="center"><img src="https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/cs-logo-footer.png"><BR/><img width="250px" src="https://raw.githubusercontent.com/CrowdStrike/foundry-fn-python/main/docs/asset/adversary-red-eyes.png"></P>
<h3><P align="center">WE STOP BREACHES</P></h3>
