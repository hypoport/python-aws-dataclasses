from datetime import datetime
from typing import Dict, Any, List

import arrow
from dataclasses import dataclass, InitVar, field

from aws_dataclasses.util import get_logger
from aws_dataclasses.base import GenericDataClass

LOG = get_logger(__name__)


@dataclass
class LambdaTracingConfig(GenericDataClass):
    Mode: InitVar[str] = field(repr=False, default=None)
    mode: str = field(init=False)

    def __post_init__(self, Mode: str):
        self.mode = Mode


@dataclass
class LambdaVpcConfig(GenericDataClass):
    SubnetIds: InitVar[List[str]] = field(repr=False, default=None)
    SecurityGroupIds: InitVar[List[str]] = field(repr=False, default=None)
    VpcId: InitVar[str] = field(repr=False, default=None)
    subnet_ids: List[str] = field(init=False)
    security_group_ids: List[str] = field(init=False)
    vpc_id: str = field(init=False)

    def __post_init__(self, SubnetIds: List[str], SecurityGroupIds: List[str], VpcId: str):
        self.subnet_ids = SubnetIds
        self.security_group_ids = SecurityGroupIds
        self.vpc_id = VpcId


@dataclass
class LambdaDlqConfig(GenericDataClass):
    TargetArn: InitVar[str] = field(repr=False, default=None)
    target_arn: str = field(init=False)

    def __post_init__(self, TargetArn: str):
        self.target_arn = TargetArn


@dataclass
class LambdaEnvironment(GenericDataClass):
    Variables: InitVar[Dict] = field(repr=False, default=None)
    variables: Dict = field(init=False)

    def __post_init__(self, Variables: Dict):
        self.variables = Variables


@dataclass
class LambdaFunctionConfiguration(GenericDataClass):
    FunctionName: InitVar[str] = field(repr=False, default=None)
    FunctionArn: InitVar[str] = field(repr=False, default=None)
    Runtime: InitVar[str] = field(repr=False, default=None)
    Role: InitVar[str] = field(repr=False, default=None)
    Handler: InitVar[str] = field(repr=False, default=None)
    CodeSize: InitVar[int] = field(repr=False, default=None)
    Description: InitVar[str] = field(repr=False, default=None)
    Timeout: InitVar[int] = field(repr=False, default=None)
    MemorySize: InitVar[int] = field(repr=False, default=None)
    LastModified: InitVar[str] = field(repr=False, default=None)
    CodeSha256: InitVar[str] = field(repr=False, default=None)
    Version: InitVar[str] = field(repr=False, default=None)
    VpcConfig: InitVar[Any] = field(repr=False, default=None)
    DeadLetterConfig: InitVar[Any] = field(repr=False, default=None)
    Environment: InitVar[Any] = field(repr=False, default=None)
    TracingConfig: InitVar[Any] = field(repr=False, default=None)
    RevisionId: InitVar[str] = field(repr=False, default=None)
    function_name: str = field(init=False)
    function_arn: str = field(init=False)
    runtime: str = field(init=False)
    role: str = field(init=False)
    handler: str = field(init=False)
    code_size: int = field(init=False)
    description: str = field(init=False)
    timeout: int = field(init=False)
    memory_size: int = field(init=False)
    last_modified: datetime = field(init=False)
    code_sha_256: str = field(init=False)
    version: str = field(init=False)
    vpc_config: VpcConfig = field(init=False)
    dead_letter_config: LambdaDlqConfig = field(init=False)
    environment: LambdaEnvironment = field(init=False)
    tracing_config: TracingConfig = field(init=False)
    revision_id: str = field(init=False)

    def __post_init__(self, FunctionName: str, FunctionArn: str, Runtime: str, Role: str, Handler: str, CodeSize: int,
                      Description: str, Timeout: int, MemorySize: int, LastModified: str, CodeSha256: str, Version: str,
                      VpcConfig: Any, DeadLetterConfig: Any, Environment: Any, TracingConfig: Any, RevisionId: str):
        self.last_modified = arrow.get(LastModified).datetime
        self.function_arn = FunctionArn
        self.function_name = FunctionName
        self.runtime = Runtime
        self.role = Role
        self.handler = Handler
        self.code_size = CodeSize
        self.description = Description
        self.timeout = Timeout
        self.memory_size = MemorySize
        self.code_sha_256 = CodeSha256
        self.version = Version
        self.vpc_config = LambdaVpcConfig.from_json(VpcConfig) if VpcConfig is not None else None
        self.dead_letter_config = LambdaDlqConfig.from_json(DeadLetterConfig) if DeadLetterConfig is not None else None
        self.environment = LambdaEnvironment.from_json(Environment) if Environment is not None else None
        self.tracing_config = LambdaTracingConfig.from_json(TracingConfig) if TracingConfig is not None else None
        self.revision_id = RevisionId
