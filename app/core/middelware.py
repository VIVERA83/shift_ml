from fastapi import FastAPI

from fastapi import Request as FastApiRequest
from fastapi import Response, status
from fastapi.encoders import jsonable_encoder

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

HTTP_EXCEPTIONS = {
    status.HTTP_404_NOT_FOUND: "Not Found",
    status.HTTP_400_BAD_REQUEST: "Bad Request",
    status.HTTP_401_UNAUTHORIZED: "Unauthorized",
    status.HTTP_403_FORBIDDEN: "Forbidden",
    status.HTTP_405_METHOD_NOT_ALLOWED: "Method Not Allowed",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
}


class ErrorHandlingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: FastApiRequest, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as error:
            code = getattr(error, "code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            return JSONResponse(
                status_code=code,
                content=jsonable_encoder(
                    {"detail": HTTP_EXCEPTIONS.get(code), "message": str(error.args)}
                ),
            )


def setup_middleware(app: FastAPI):
    app.add_middleware(ErrorHandlingMiddleware)  # noqa type: ignore
