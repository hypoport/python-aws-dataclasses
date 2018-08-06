from typing import Dict

from dataclasses import dataclass, field, InitVar

from util import GenericDataClass


@dataclass
class Identity(GenericDataClass):
    caller: str
    user: str
    api_key: str = field(init=False)
    user_arn: str = field(init=False)
    cognito_auth_type: str = field(init=False)
    user_agent: str = field(init=False)
    cognito_identity_pool_id: str = field(init=False)
    cognito_auth_provider: str = field(init=False)
    source_ip: str = field(init=False)
    account_id: str = field(init=False)
    cognito_identity_id: str = field(init=False)
    apiKey: InitVar[str] = field(repr=False, default=None)
    userArn: InitVar[str] = field(repr=False, default=None)
    cognitoAuthenticationType: InitVar[str] = field(repr=False, default=None)
    userAgent: InitVar[str] = field(repr=False, default=None)
    cognitoIdentityPoolId: InitVar[str] = field(repr=False, default=None)
    cognitoAuthenticationProvider: InitVar[str] = field(repr=False, default=None)
    sourceIp: InitVar[str] = field(repr=False, default=None)
    accountId: InitVar[str] = field(repr=False, default=None)
    cognitoIdentityId: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, apiKey: str, userArn: str, cognitoAuthenticationType: str, userAgent: str,
                      cognitoIdentityPoolId: str, cognitoAuthenticationProvider: str, sourceIp: str, accountId: str,
                      cognitoIdentityId: str):
        self.api_key = apiKey
        self.user_arn = userArn
        self.user_agent = userAgent
        self.cognito_auth_type = cognitoAuthenticationType
        self.cognito_auth_provider = cognitoAuthenticationProvider
        self.cognito_identity_id = cognitoIdentityId
        self.cognito_identity_pool_id = cognitoIdentityPoolId
        self.source_ip = sourceIp
        self.account_id = accountId


@dataclass
class RequestContext(GenericDataClass):
    stage: str
    identity: Identity
    resource_id: str = field(init=False)
    api_id: str = field(init=False)
    resource_path: str = field(init=False)
    http_method: str = field(init=False)
    request_id: str = field(init=False)
    account_id: str = field(init=False)
    resourceId: InitVar[str] = field(repr=False, default=None)
    apiId: InitVar[str] = field(repr=False, default=None)
    resourcePath: InitVar[str] = field(repr=False, default=None)
    httpMethod: InitVar[str] = field(repr=False, default=None)
    requestId: InitVar[str] = field(repr=False, default=None)
    accountId: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, resourceId: str, apiId: str, resourcePath: str, httpMethod: str, requestId: str,
                      accountId: str):
        self.request_id = requestId
        self.resource_id = resourceId
        self.resource_path = resourcePath
        self.account_id = accountId
        self.api_id = apiId
        self.http_method = httpMethod
        self.identity = Identity(**self.identity)


@dataclass
class ApiGwProxyEvent(GenericDataClass):
    body: str
    resource: str
    path: str
    headers: Dict[str, str]
    http_method: str = field(init=False)
    request_context: RequestContext = field(init=False)
    query_string_parameters: Dict[str, str] = field(init=False)
    path_parameters: Dict[str, str] = field(init=False)
    stage_variables: Dict[str, str] = field(init=False)
    requestContext: InitVar[Dict] = field(repr=False, default=None)
    queryStringParameters: InitVar[str] = field(repr=False, default=None)
    pathParameters: InitVar[str] = field(repr=False, default=None)
    httpMethod: InitVar[str] = field(repr=False, default=None)
    stageVariables: InitVar[str] = field(repr=False, default=None)

    def __post_init__(self, requestContext: str, queryStringParameters: str, pathParameters: str, httpMethod: str,
                      stageVariables: str):
        self.request_context = RequestContext(**requestContext)
        self.query_string_parameters = queryStringParameters
        self.path_parameters = pathParameters
        self.http_method = httpMethod
        self.stage_variables = stageVariables

    @classmethod
    def from_event(cls, event):
        print(event)
        return cls.from_json(event)
