# The MIT License (MIT)
#
# Copyright (c) 2016-Present Syrus Akbary
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# ----------------------------------------------------------------------------
#
# This is a Cylc port of the graphene-django graphene integration:
# https://github.com/graphql-python/graphene-django
# with reference to:
# https://github.com/graphql-python/graphene-tornado
# https://github.com/graphql-python/graphql-server
#
# Excludes GraphiQL

from asyncio import iscoroutinefunction
import json
import re
import sys
import traceback
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

from tornado import web
from tornado.escape import json_encode
from tornado.escape import to_unicode
from tornado.httpclient import HTTPClientError
from tornado.log import app_log
from tornado.web import HTTPError


from graphql import (
    DocumentNode,
    ExecutionResult,
    OperationType,
    execute,
    get_operation_ast,
    parse,
    validate_schema,
)
from graphql.error import GraphQLError
from graphql.execution.middleware import MiddlewareManager
from graphql.pyutils import is_awaitable
from graphql.validation import validate

from cylc.flow.network.graphql import (
    NULL_VALUE,
    instantiate_middleware,
    strip_null
)

if TYPE_CHECKING:
    from graphene import Schema
    from tornado.httputil import HTTPServerRequest

MUTATION_ERRORS_FLAG = "graphene_mutation_has_errors"
MAX_VALIDATION_ERRORS = None


def data_search_action(data, action):
    if isinstance(data, dict):
        return {
            key: data_search_action(val, action)
            for key, val in data.items()
        }
    if isinstance(data, list):
        return [
            data_search_action(val, action)
            for val in data
        ]
    return action(data)


def get_content_type(request: 'HTTPServerRequest') -> str:
    return request.headers.get("Content-Type", "").split(";", 1)[0].lower()


def get_accepted_content_types(request: 'HTTPServerRequest') -> list:
    def qualify(x):
        parts = x.split(";", 1)
        if len(parts) == 2:
            match = re.match(
                r"(^|;)q=(0(\.\d{,3})?|1(\.0{,3})?)(;|$)", parts[1])
            if match:
                return parts[0].strip(), float(match.group(2))
        return parts[0].strip(), 1

    raw_content_types = request.headers.get("Accept", "*/*").split(",")
    qualified_content_types = map(qualify, raw_content_types)
    return [
        x[0]
        for x in sorted(
            qualified_content_types, key=lambda x: x[1], reverse=True)
    ]


class ExecutionError(Exception):
    def __init__(self, status_code=400, errors=None):
        self.status_code = status_code
        if errors is None:
            self.errors = []
        else:
            self.errors = [str(e) for e in errors]
        self.message = "\n".join(self.errors)


class TornadoGraphQLHandler(web.RequestHandler):

    document: Optional[DocumentNode]
    graphql_params: Optional[Tuple[Any, Any, Any, Any]]
    middleware: Optional[Union[MiddlewareManager, List[Callable], None]]
    parsed_body: Optional[Dict[str, Any]]

    def initialize(
        self,
        schema: 'Schema',
        middleware: Union[MiddlewareManager, List[type], None] = None,
        root_value=None,
        pretty: bool = False,
        batch: bool = False,
        subscription_path=None,
        execution_context_class=None,
        validation_rules=None,
    ) -> None:
        super(TornadoGraphQLHandler, self).initialize()
        self.schema = schema
        self.root_value = root_value
        self.pretty = pretty
        self.batch = batch
        self.subscription_path = subscription_path
        self.execution_context_class = execution_context_class
        self.validation_rules = validation_rules

        self.graphql_params = None
        self.parsed_body = None

        if isinstance(middleware, MiddlewareManager):
            self.middleware = middleware
        elif middleware is not None:
            self.middleware = list(instantiate_middleware(middleware))
        else:
            self.middleware = None

    def get_context(self):
        return self.request

    def get_root_value(self):
        return self.root_value

    def get_middleware(self) -> Union[MiddlewareManager, List[Callable], None]:
        return self.middleware

    def get_parsed_body(self):
        return self.parsed_body

    async def get(self) -> None:
        try:
            await self.run("get")
        except Exception as ex:
            self.handle_error(ex)

    async def post(self) -> None:
        try:
            await self.run("post")
        except Exception as ex:
            self.handle_error(ex)

    async def run(self, *args, **kwargs):
        try:
            data = self.parse_body()

            if self.batch:
                responses = [
                    await self.get_response(entry)
                    for entry in data
                ]
                result = "[{}]".format(
                    ",".join([response[0] for response in responses])
                )
                status_code = (
                    responses
                    and max(responses, key=lambda response: response[1])[1]
                    or 200
                )
            else:
                result, status_code = await self.get_response(data)

            self.set_status(status_code)
            self.set_header("Content-Type", "application/json")
            self.write(result)
            await self.finish()

        except HTTPClientError as e:
            response = e.response
            response["Content-Type"] = "application/json"
            response.content = self.json_encode(
                self.request, {"errors": [self.format_error(e)]}
            )
            return response

    async def get_response(self, data):
        query, variables, operation_name, _id = self.get_graphql_params(
            self.request, data
        )

        execution_result = await self.execute_graphql_request(
            data, query, variables, operation_name
        )

        status_code = 200
        if execution_result:
            response = {}

            if is_awaitable(execution_result) or iscoroutinefunction(
                execution_result
            ):
                execution_result = await execution_result

            if hasattr(execution_result, "get"):
                execution_result = execution_result.get()

            if execution_result.errors:
                response["errors"] = [
                    self.format_error(e) for e in execution_result.errors
                ]

            if execution_result.errors and any(
                not getattr(e, "path", None) for e in execution_result.errors
            ):
                status_code = 400
            else:
                response["data"] = execution_result.data

            if self.batch:
                response["id"] = _id
                response["status"] = status_code
            try:
                result = self.json_encode(response)
            except TypeError:
                # Catch exceptions in response
                errors = []

                def exc_to_errors(data):
                    if isinstance(data, Exception):
                        errors.append({
                            'message': (
                                f'{data.value}'
                                if hasattr(data, 'value') else f'{data}'
                            )
                        })
                        return NULL_VALUE
                    return data

                response = data_search_action(
                    response,
                    exc_to_errors
                )
                response.setdefault("errors", []).extend(errors)
                response = strip_null(response)

                result = self.json_encode(response)
        else:
            result = None

        return result, status_code

    def json_encode(self, d, pretty=False):
        if (self.pretty or pretty) or self.get_query_argument("pretty", False):
            return json.dumps(
                d, sort_keys=True, indent=2, separators=(",", ": "))

        return json.dumps(d, separators=(",", ":"))

    def parse_body(self):
        content_type = get_content_type(self.request)

        if content_type == "application/graphql":
            self.parsed_body = {"query": to_unicode(self.request.body)}
            return self.parsed_body

        elif content_type == "application/json":
            try:
                body = self.request.body
            except Exception as e:
                raise ExecutionError(400, e)

            try:
                request_json = json.loads(body)
                if self.batch:
                    if not isinstance(request_json, list):
                        raise AssertionError(
                            "Batch requests should receive a list"
                            ", but received {}."
                        ).format(repr(request_json))
                    if len(request_json <= 0):
                        raise AssertionError(
                            "Received an empty list in the batch request."
                        )
                else:
                    if not isinstance(request_json, dict):
                        raise AssertionError(
                            "The received data is not a valid JSON query."
                        )
                self.parsed_body = request_json
                return self.parsed_body
            except AssertionError as e:
                raise HTTPError(status_code=400, log_message=str(e))
            except (TypeError, ValueError):
                raise HTTPError(
                    status_code=400, log_message="POST body sent invalid JSON."
                )

        elif content_type in [
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ]:
            self.parsed_body = self.request.query_arguments
            return self.parsed_body

        self.parsed_body = {}
        return self.parsed_body

    async def execute_graphql_request(
        self, data, query, variables, operation_name
    ):
        if not query:
            raise HTTPError(
                status_code=400, log_message="Must provide query string."
            )

        schema = self.schema.graphql_schema

        schema_validation_errors = validate_schema(schema)
        if schema_validation_errors:
            return ExecutionResult(data=None, errors=schema_validation_errors)

        try:
            self.document = parse(query)
        except Exception as e:
            return ExecutionResult(errors=[e])

        operation_ast = get_operation_ast(self.document, operation_name)

        if (
            self.request.method.lower() == "get"
            and operation_ast is not None
            and operation_ast.operation != OperationType.QUERY
        ):
            raise HTTPError(
                status_code=405,
                log_message=(
                    f'Can only perform a {operation_ast.operation.value} '
                    'operation from a POST request.'
                ),
            )

        validation_errors = validate(
            schema,
            self.document,
            self.validation_rules,
            MAX_VALIDATION_ERRORS,
        )
        if validation_errors:
            return ExecutionResult(data=None, errors=validation_errors)

        try:
            execute_options = {
                "root_value": self.get_root_value(),
                "context_value": self.get_context(),
                "variable_values": variables,
                "operation_name": operation_name,
                "middleware": self.get_middleware(),
            }
            if self.execution_context_class:
                execute_options[
                    "execution_context_class"
                ] = self.execution_context_class

            result = await self.execute(
                schema,
                self.document,
                **execute_options
            )

            return result
        except Exception as e:
            return ExecutionResult(errors=[e])

    async def execute(self, *args, **kwargs):
        return execute(*args, **kwargs)

    def request_wants_html(self):
        accepted = get_accepted_content_types(self.request)
        accepted_length = len(accepted)
        # the list will be ordered in preferred first - so we have to make
        # sure the most preferred gets the highest number
        html_priority = (
            accepted_length - accepted.index("text/html")
            if "text/html" in accepted
            else 0
        )
        json_priority = (
            accepted_length - accepted.index("application/json")
            if "application/json" in accepted
            else 0
        )

        return html_priority > json_priority

    def get_graphql_params(self, request, data):
        if self.graphql_params:
            return self.graphql_params

        single_args = {}
        for key in request.arguments.keys():
            single_args[key] = self.decode_argument(
                request.arguments.get(key)[0])

        query = single_args.get("query") or data.get("query")
        variables = single_args.get("variables") or data.get("variables")
        _id = single_args.get("id") or data.get("id")

        if variables and isinstance(variables, str):
            try:
                variables = json.loads(variables)
            except Exception:
                raise HTTPError(
                    status_code=400,
                    log_message="Variables are invalid JSON."
                )

        operation_name = (
            single_args.get("operationName") or data.get("operationName")
        )
        if operation_name == "null":
            operation_name = None

        self.graphql_params = query, variables, operation_name, _id
        return self.graphql_params

    def handle_error(self, ex: Exception) -> None:
        if not isinstance(ex, (web.HTTPError, ExecutionError, GraphQLError)):
            tb = "".join(traceback.format_exception(*sys.exc_info()))
            app_log.error("Error: {0} {1}".format(ex, tb))
        self.set_status(self.error_status(ex))
        error_json = json_encode({"errors": self.error_format(ex)})
        app_log.debug("error_json: %s", error_json)
        self.write(error_json)

    @staticmethod
    def error_status(exception: Exception) -> int:
        if isinstance(exception, web.HTTPError):
            return exception.status_code
        elif isinstance(exception, (ExecutionError, GraphQLError)):
            return 400
        else:
            return 500

    @staticmethod
    def error_format(exception: Exception) -> List[Dict[str, Any]]:
        if isinstance(exception, ExecutionError):
            return [{"message": e} for e in exception.errors]
        elif isinstance(exception, GraphQLError):
            return [{"message": exception.formatted["message"]}]
        elif isinstance(exception, web.HTTPError):
            return [{"message": exception.log_message}]
        else:
            return [{"message": "Unknown server error"}]

    @staticmethod
    def format_error(error):
        if isinstance(error, GraphQLError):
            return error.formatted

        return {"message": str(error)}
