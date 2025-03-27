import re
from collections.abc import Callable
from functools import wraps
from typing import Any

from fastapi import HTTPException

from app.common.constants import APP_DIR_PATH
from app.common.enums import ClassEnum, ProjectBuildTypes
from app.core import AppException, settings
from app.core.loggers import logger


## External Function ##
def logger_ignore(func: Callable[..., Any]) -> Callable[..., Any]:
    func._logger_ignore = True
    return func


def logger_function_call(class_name: ClassEnum) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Any) -> Any:
        filename = func.__code__.co_filename.split(f"{APP_DIR_PATH}\\", 1)[-1]
        lineno = func.__code__.co_firstlineno

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            safe_args, safe_kwargs = _sanitize_args(args, kwargs)
            logger.info(
                f"{filename}:{lineno} - [{class_name.value}] "
                f"Gọi hàm: {func.__name__} | args={safe_args} | kwargs={safe_kwargs}"
            )
            try:
                result = await func(*args, **kwargs)
                log_result = (
                    result.to_dict(exclude=["hashed_password"])
                    if class_name == ClassEnum.REPOSITORY and result
                    else result
                )
                logger.info(
                    f"{filename}:{lineno} - [{class_name.value}] Kết quả hàm {func.__name__}: {log_result}"
                )
                return result
            except AppException as e:
                if not hasattr(e, "_logged"):
                    if isinstance(e.detail, dict) and "name" in e.detail and "message" in e.detail:
                        logger.error(
                            f"{filename}:{lineno} - [{class_name.value}] "
                            f"Lỗi trong hàm {func.__name__}: {e.detail['name']} | {e.detail['message']}"
                        )
                    else:
                        logger.error(
                            f"{filename}:{lineno} - [{class_name.value}] Lỗi trong hàm {func.__name__}: {str(e.detail)}"
                        )
                    e._logged = True
                raise e
            except HTTPException as e:
                if not hasattr(e, "_logged"):
                    logger.error(
                        f"{filename}:{lineno} - [{class_name.value}] Lỗi trong hàm {func.__name__}: {e.detail}"
                    )
                    e._logged = True
                raise e
            except Exception as e:
                if not hasattr(e, "_logged"):
                    logger.error(f"{filename}:{lineno} - [{class_name.value}] Lỗi trong hàm {func.__name__}: {str(e)}")
                    e._logged = True
                raise e

        return wrapper

    return decorator


def logger_class_methods(class_name: ClassEnum) -> Callable:
    def class_decorator(cls: Any) -> Callable:
        for attr_name, attr_value in cls.__dict__.items():
            if attr_name.startswith("_") or getattr(attr_value, "_logger_ignore", False):
                continue

            if isinstance(attr_value, staticmethod):
                wrapped_func = staticmethod(logger_function_call(class_name)(attr_value.__func__))
            elif isinstance(attr_value, classmethod):
                wrapped_func = classmethod(logger_function_call(class_name)(attr_value.__func__))
            elif callable(attr_value):
                wrapped_func = logger_function_call(class_name)(attr_value)
            else:
                continue

            setattr(cls, attr_name, wrapped_func)

        return cls

    return class_decorator


## Internal Function ##
def _sanitize_args(args: tuple[Any, ...], kwargs: dict[str, Any]) -> tuple[list[str], dict[str, str]]:
    sanitized_args = []
    for arg in args:
        if "password" in str(arg) and settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.PRODUCTION:
            sanitized_args.append(f"<AuthLoginRequest(username={arg.username}, password=****)>")
        elif isinstance(arg, object) and re.match(r"^<.* object at 0x[a-fA-F0-9]+>$", str(arg)):
            sanitized_args.append(f"<{type(arg).__name__}>")
        else:
            sanitized_args.append(str(arg))

    sanitized_kwargs = {}
    for k, v in kwargs.items():
        if "password" in str(v) and settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.PRODUCTION:
            sanitized_kwargs[k] = f"<AuthLoginRequest(username={v.username}, password=****)>"
        elif isinstance(v, object):
            if re.match(r"^<.* object at 0x[a-fA-F0-9]+>$", str(v)):
                sanitized_kwargs[k] = f"<{type(v).__name__}>"
            else:
                sanitized_kwargs[k] = f"<{type(v).__name__}({v})>"
        else:
            sanitized_kwargs[k] = str(v)

    return sanitized_args, sanitized_kwargs
