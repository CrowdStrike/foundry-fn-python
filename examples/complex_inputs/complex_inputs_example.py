"""Example Foundry Function with POST handler."""
from crowdstrike.foundry.function import Function, Request, Response

func = Function.instance()


@func.handler(method='POST', path='/my-endpoint')
def handle_complex_inputs(request: Request) -> Response:
    """Implement example function handler to showcase how to handle complex inputs.

    This example demonstrates how to provide multiple inputs to a function, some of which happen to be files.
    In this case, it simply echoes back the contents of those files concatenated together with spaces.
    This could easily be changed to something more advanced to work with arbitrary binary.

    :param request: :class:`Request` to handle.
    :return: :class:`Response`
    """
    greeting = f'Welcome {request.body.get("name", "<unknown>")}, age {request.body.get("age", "<unknown>")}'
    file_contents = []
    for v in request.files.values():
        file_contents.append(v.decode('utf-8').strip())

    return Response(
        body={
            'allText': ' '.join(file_contents),
            'greeting': greeting,
        },
        code=200,
    )


if __name__ == '__main__':
    func.run()
