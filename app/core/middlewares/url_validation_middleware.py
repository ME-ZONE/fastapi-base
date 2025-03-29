import re
import urllib.parse
from collections.abc import Awaitable, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from app.common.constants import AppStatus

# ALLOWED_PATH_CHARS:
# Matches strings that consist solely of letters, digits, and the characters '/', '_', '-', '.', and '~'
ALLOWED_PATH_CHARS = re.compile(r"^[A-Za-z0-9/_\-\.~]+$")

# ALLOWED_QUERY_CHARS:
# Matches strings that contain letters, digits, basic symbols, percent signs, and extended Unicode ranges.
# This regex includes allowed punctuation and symbols needed in query strings.
ALLOWED_QUERY_CHARS = re.compile(r'^[A-Za-z0-9/_\-\.&=%\u00C0-\u024F\u1E00-\u1EFF":,!*\'()\[\]@]+$')

# ALLOWED_FILENAME:
# Matches filenames that do not contain dangerous characters.
# Disallows filenames that are only '.' or '..', or contain only whitespace.
# Excludes: <, >, :, ", /, \, |, ?, *, and control characters (ASCII 0-31)
ALLOWED_FILENAME = re.compile(r'^(?!\.{1,2}$)(?!\s*$)[^<>:"/\\|?*\x00-\x1F]+$')
WHITELIST = []


class URLValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> JSONResponse | Response:
        parsed_url = urllib.parse.urlparse(request.url._url)
        decoded_path, decoded_query = urllib.parse.unquote(parsed_url.path), urllib.parse.unquote(parsed_url.query)

        if (decoded_path and not self.is_valid_path(decoded_path)) or (
            decoded_query and not self.is_valid_query(decoded_query)
        ):
            return self.invalid_url_response()

        response = await call_next(request)
        return response

    @staticmethod
    def is_valid_path(path: str) -> bool:
        return bool(ALLOWED_PATH_CHARS.fullmatch(path))

    @staticmethod
    def is_valid_query(query: str) -> bool:
        query_params: dict[str, list[str]] = urllib.parse.parse_qs(query)

        for key, values in query_params.items():
            if key in WHITELIST:
                query_params.pop(key)
                continue

            if "filename" in key and any(
                not ALLOWED_FILENAME.fullmatch(urllib.parse.unquote(f).strip()) for f in values
            ):
                return False

        encoded_query = urllib.parse.urlencode(query_params, doseq=True)
        return bool(ALLOWED_QUERY_CHARS.fullmatch(urllib.parse.unquote(encoded_query)))

    @staticmethod
    def invalid_url_response() -> JSONResponse:
        return JSONResponse(
            status_code=AppStatus.INIT_403_INVALID_URL_FORBIDDEN.status_code,
            content={
                "detail": {
                    "name": AppStatus.INIT_403_INVALID_URL_FORBIDDEN.name,
                    "message": AppStatus.INIT_403_INVALID_URL_FORBIDDEN.message,
                }
            },
        )
