import dataclasses
import io
import logging
from typing import Dict, Type

from steamship.app.app import App
from steamship.app.request import Request
from steamship.app.response import Response, Error, Http
from steamship.client.client import Steamship


def create_handler(App: Type[App]):
    """Wrapper function for an Steamship app within an AWS Lambda function.
    """

    def handler(event: Dict, context: Dict = None) -> Dict:
        # Create a new Steamship client
        client = Steamship(
            configDict=event.get("clientConfig", None)
        )

        app = None

        try:
            app = App(client=client)
        except Exception as ex:
            logging.exception("Unable to initialize app.")
            response = Error(
                message="There was an exception thrown handling this request.",
                error=ex
            )

        try:
            request = Request.from_dict(event)
        except Exception as ex:
            logging.exception("Unable to parse inbound request")
            response = Error(
                message="There was an exception thrown handling this request.",
                error=ex
            )

        try:
            if app is not None:
                response = app(request)
        except Exception as ex:
            logging.exception("Unable to run app method.")
            response = Error(
                message="There was an exception thrown handling this request.",
                error=ex
            )

        lambda_response: Response = None

        if type(response) == Response:
            lambda_response = response
        elif type(response) == io.BytesIO:
            lambda_response = Response(bytes=response)
        elif type(response) == dict:
            lambda_response = Response(json=response)
        elif type(response) == str:
            lambda_response = Response(string=response)
        elif type(response) in [float, int, bool]:
            lambda_response = Response(json=response)
        elif dataclasses.is_dataclass(response):
            lambda_response = Response(json=response)
        else:
            lambda_response = Response(
                error=Error(message="Handler provided unknown response type."),
                http=Http(statusCode=500)
            )

        if lambda_response is None:
            lambda_response = Response(
                error=Error(message="Handler provided no response."),
                http=Http(statusCode=500)
            )

        return dataclasses.asdict(lambda_response)

    return handler
