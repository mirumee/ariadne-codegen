import json
from typing import IO, Any, Dict, List, Optional, Tuple, TypeVar, Union, cast

import httpx
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from .base_model import UNSET, Upload
from .exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidResponseError,
)

try:
    from opentelemetry.context import (  # type: ignore[import-not-found,unused-ignore]
        Context,
    )
    from opentelemetry.trace import (  # type: ignore[import-not-found,unused-ignore]
        Span,
        Tracer,
        get_tracer,
        set_span_in_context,
    )
except ImportError:
    Context = Any  # type: ignore[misc,assignment,unused-ignore]
    Span = Any  # type: ignore[misc,assignment,unused-ignore]
    Tracer = Any  # type: ignore[misc,assignment,unused-ignore]

    def get_tracer(*args, **kwargs) -> Tracer:  # type: ignore
        raise NotImplementedError("Telemetry requires 'opentelemetry-api' package.")

    def set_span_in_context(*args, **kwargs):  # type: ignore
        raise NotImplementedError("Telemetry requires 'opentelemetry-api' package.")


Self = TypeVar("Self", bound="BaseClientOpenTelemetry")


class BaseClientOpenTelemetry:
    def __init__(
        self,
        url: str = "",
        headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
        tracer: Optional[Union[str, Tracer]] = None,
        root_context: Optional[Context] = None,
        root_span_name: Optional[str] = None,
    ) -> None:
        self.url = url
        self.headers = headers

        self.http_client = http_client if http_client else httpx.Client(headers=headers)

        self.tracer: Optional[Tracer] = (
            get_tracer(tracer) if isinstance(tracer, str) else tracer
        )
        self.root_context = root_context
        self.root_span_name = root_span_name if root_span_name else "GraphQL Operation"

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        self.http_client.close()

    def execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        if self.tracer:
            return self._execute_with_telemetry(
                query=query,
                operation_name=operation_name,
                variables=variables,
                **kwargs,
            )
        return self._execute(
            query=query, operation_name=operation_name, variables=variables, **kwargs
        )

    def get_data(self, response: httpx.Response) -> Dict[str, Any]:
        if not response.is_success:
            raise GraphQLClientHttpError(
                status_code=response.status_code, response=response
            )

        try:
            response_json = response.json()
        except ValueError as exc:
            raise GraphQLClientInvalidResponseError(response=response) from exc

        if (not isinstance(response_json, dict)) or (
            "data" not in response_json and "errors" not in response_json
        ):
            raise GraphQLClientInvalidResponseError(response=response)

        data = response_json.get("data")
        errors = response_json.get("errors")

        if errors:
            raise GraphQLClientGraphQLMultiError.from_errors_dicts(
                errors_dicts=errors, data=data
            )

        return cast(Dict[str, Any], data)

    def _execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        processed_variables, files, files_map = self._process_variables(variables)

        if files and files_map:
            return self._execute_multipart(
                query=query,
                operation_name=operation_name,
                variables=processed_variables,
                files=files,
                files_map=files_map,
                **kwargs,
            )

        return self._execute_json(
            query=query,
            operation_name=operation_name,
            variables=processed_variables,
            **kwargs,
        )

    def _process_variables(
        self, variables: Optional[Dict[str, Any]]
    ) -> Tuple[
        Dict[str, Any], Dict[str, Tuple[str, IO[bytes], str]], Dict[str, List[str]]
    ]:
        if not variables:
            return {}, {}, {}

        serializable_variables = self._convert_dict_to_json_serializable(variables)
        return self._get_files_from_variables(serializable_variables)

    def _convert_dict_to_json_serializable(
        self, dict_: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            key: self._convert_value(value)
            for key, value in dict_.items()
            if value is not UNSET
        }

    def _convert_value(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            return value.model_dump(by_alias=True, exclude_unset=True)
        if isinstance(value, list):
            return [self._convert_value(item) for item in value]
        return value

    def _get_files_from_variables(
        self, variables: Dict[str, Any]
    ) -> Tuple[
        Dict[str, Any], Dict[str, Tuple[str, IO[bytes], str]], Dict[str, List[str]]
    ]:
        files_map: Dict[str, List[str]] = {}
        files_list: List[Upload] = []

        def separate_files(path: str, obj: Any) -> Any:
            if isinstance(obj, list):
                nulled_list = []
                for index, value in enumerate(obj):
                    value = separate_files(f"{path}.{index}", value)
                    nulled_list.append(value)
                return nulled_list

            if isinstance(obj, dict):
                nulled_dict = {}
                for key, value in obj.items():
                    value = separate_files(f"{path}.{key}", value)
                    nulled_dict[key] = value
                return nulled_dict

            if isinstance(obj, Upload):
                if obj in files_list:
                    file_index = files_list.index(obj)
                    files_map[str(file_index)].append(path)
                else:
                    file_index = len(files_list)
                    files_list.append(obj)
                    files_map[str(file_index)] = [path]
                return None

            return obj

        nulled_variables = separate_files("variables", variables)
        files: Dict[str, Tuple[str, IO[bytes], str]] = {
            str(i): (file_.filename, cast(IO[bytes], file_.content), file_.content_type)
            for i, file_ in enumerate(files_list)
        }
        return nulled_variables, files, files_map

    def _execute_multipart(
        self,
        query: str,
        operation_name: Optional[str],
        variables: Dict[str, Any],
        files: Dict[str, Tuple[str, IO[bytes], str]],
        files_map: Dict[str, List[str]],
        **kwargs: Any,
    ) -> httpx.Response:
        data = {
            "operations": json.dumps(
                {
                    "query": query,
                    "operationName": operation_name,
                    "variables": variables,
                },
                default=to_jsonable_python,
            ),
            "map": json.dumps(files_map, default=to_jsonable_python),
        }

        return self.http_client.post(url=self.url, data=data, files=files, **kwargs)

    def _execute_json(
        self,
        query: str,
        operation_name: Optional[str],
        variables: Dict[str, Any],
        **kwargs: Any,
    ) -> httpx.Response:
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        headers.update(kwargs.get("headers", {}))

        merged_kwargs: Dict[str, Any] = kwargs.copy()
        merged_kwargs["headers"] = headers

        return self.http_client.post(
            url=self.url,
            content=json.dumps(
                {
                    "query": query,
                    "operationName": operation_name,
                    "variables": variables,
                },
                default=to_jsonable_python,
            ),
            **merged_kwargs,
        )

    def _execute_with_telemetry(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        with self.tracer.start_as_current_span(  # type: ignore
            self.root_span_name, context=self.root_context
        ) as root_span:
            root_span.set_attribute("component", "GraphQL Client")

            processed_variables, files, files_map = self._process_variables(variables)

            if files and files_map:
                return self._execute_multipart_with_telemetry(
                    root_span=root_span,
                    query=query,
                    operation_name=operation_name,
                    variables=processed_variables,
                    files=files,
                    files_map=files_map,
                    **kwargs,
                )

            return self._execute_json_with_telemetry(
                root_span=root_span,
                query=query,
                operation_name=operation_name,
                variables=processed_variables,
                **kwargs,
            )

    def _execute_multipart_with_telemetry(
        self,
        root_span: Span,
        query: str,
        operation_name: Optional[str],
        variables: Dict[str, Any],
        files: Dict[str, Tuple[str, IO[bytes], str]],
        files_map: Dict[str, List[str]],
        **kwargs: Any,
    ) -> httpx.Response:
        with self.tracer.start_as_current_span(  # type: ignore
            "multipart request", context=set_span_in_context(root_span)
        ) as span:
            span.set_attribute("component", "GraphQL Client")

            serialized_variables = json.dumps(variables, default=to_jsonable_python)
            serialized_map = json.dumps(files_map, default=to_jsonable_python)

            span.set_attribute("query", query)
            span.set_attribute("operationName", operation_name or "")
            span.set_attribute("variables", serialized_variables)
            span.set_attribute("map", serialized_map)

            return self._execute_multipart(
                query=query,
                operation_name=operation_name,
                variables=variables,
                files=files,
                files_map=files_map,
                **kwargs,
            )

    def _execute_json_with_telemetry(
        self,
        root_span: Span,
        query: str,
        operation_name: Optional[str],
        variables: Dict[str, Any],
        **kwargs: Any,
    ) -> httpx.Response:
        with self.tracer.start_as_current_span(  # type: ignore
            "json request", context=set_span_in_context(root_span)
        ) as span:
            span.set_attribute("component", "GraphQL Client")

            serialized_variables = json.dumps(variables, default=to_jsonable_python)

            span.set_attribute("query", query)
            span.set_attribute("operationName", operation_name or "")
            span.set_attribute("variables", serialized_variables)

            return self._execute_json(
                query=query,
                operation_name=operation_name,
                variables=variables,
                **kwargs,
            )
