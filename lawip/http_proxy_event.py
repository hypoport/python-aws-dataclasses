from typing import Dict

class Identity:
    def __init__(self,
                 api_key: str,
                 user_arn: str,
                 cognito_auth_type: str,
                 caller: str,
                 user_agent: str,
                 user: str,
                 cognito_identity_pool_id: str,
                 cognito_auth_provider: str,
                 source_ip: str,
                 account_id: str,
                 cognito_identity_id: str):
        self._api_key = api_key
        self._user_arn = user_arn
        self._cognito_auth_type = cognito_auth_type
        self._caller = caller
        self._user_agent = user_agent
        self._user = user
        self._cognito_identity_pool_id = cognito_identity_pool_id
        self._cognito_auth_provider = cognito_auth_provider
        self._source_ip = source_ip
        self._account_id = account_id
        self._cognito_identity_id = cognito_identity_id

    @classmethod
    def from_json(cls, identity):
        return cls(identity["apiKey"],
                   identity["userArn"],
                   identity["cognitoAuthenticationType"],
                   identity["caller"],
                   identity["userAgent"],
                   identity["user"],
                   identity["cognitoIdentityPoolId"],
                   identity["cognitoAuthenticationProvider"],
                   identity["sourceIp"],
                   identity["accountId"],
                   identity["cognitoIdentityId"])


class RequestContext:
    def __init__(self, resource_id: str,
                 api_id: str,
                 resource_path: str,
                 http_method: str,
                 request_id: str,
                 account_id: str,
                 identity: Identity,
                 stage: str):
        self._resource_id = resource_id
        self._api_id = api_id
        self._resource_path = resource_path
        self._http_method = http_method
        self._request_id = request_id
        self._account_id = account_id
        self._identity = identity
        self._stage = stage

    @classmethod
    def from_json(cls, context):
        return cls(context["resourceId"],
                   context["apiId"],
                   context["resourcePath"],
                   context["httpMethod"],
                   context["requestId"],
                   context["accountId"],
                   context["identity"],
                   context["stage"])

    @property
    def resource_id(self):
        return self._resource_id

    @property
    def resource_path(self):
        return self._resource_path

    @property
    def api_id(self):
        return self._api_id

    @property
    def http_method(self):
        return self._http_method

    @property
    def request_id(self):
        return self._request_id

    @property
    def account_id(self):
        return self._account_id

    @property
    def identity(self):
        return self._identity

    @property
    def stage(self):
        return self._stage


class ApiGwProxyEvent:
    def __init__(self, body: str,
                 resource: str,
                 request_context: RequestContext,
                 query_string_parameters: Dict[str, str],
                 headers: Dict[str, str],
                 path_parameters: Dict[str, str],
                 http_method: str,
                 stage_variables: Dict[str, str],
                 path: str):
        self._body = body
        self._resource = resource
        self._request_context = request_context
        self._query_string_parameters = query_string_parameters
        self._headers = headers
        self._path_parameters = path_parameters
        self._http_method = http_method
        self._stage_variables = stage_variables
        self._path = path

    @classmethod
    def from_event(cls, event):
        return cls(event["body"],
                   event["resource"],
                   RequestContext.from_json(event["requestContext"]),
                   event["queryStringParameters"],
                   event["headers"],
                   event["pathParameters"],
                   event["httpMethod"],
                   event["stageVariables"],
                   event["path"])

    @property
    def body(self) -> str:
        return self._body

    @property
    def resource(self) -> str:
        return self._resource

    @property
    def request_context(self) -> RequestContext:
        return self._request_context

    @property
    def query_string_parameters(self) -> dict:
        return self._query_string_parameters

    @property
    def headers(self) -> dict:
        return self._headers

    @property
    def path_parameters(self) -> dict:
        return self._path_parameters

    @property
    def http_method(self) -> str:
        return self._http_method

    @property
    def stage_variables(self) -> dict:
        return self._stage_variables

    @property
    def path(self) -> str:
        return self._path
