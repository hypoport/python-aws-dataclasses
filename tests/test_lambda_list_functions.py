import datetime

import pytest
from dateutil.tz import tzutc

from aws_dataclasses.lambda_function_configuration import LambdaFunctionConfiguration

from .util import get_event_dict


@pytest.fixture(scope="module")
def lambda_functionconfig_raw():
    return get_event_dict("function_configuration.json")


@pytest.fixture(scope="module")
def lambda_functionconfig(lambda_functionconfig_raw):
    return LambdaFunctionConfiguration.from_json(lambda_functionconfig_raw)


def test_toplevel_items(lambda_functionconfig):
    cfg = lambda_functionconfig
    assert cfg.function_name == "test"
    assert cfg.function_arn == "arn:aws:lambda:eu-central-1:0123456789:function:test"
    assert cfg.runtime == "python3.6"
    assert cfg.role == "arn:aws:iam::0123456789:role/test-role"
    assert cfg.handler == "main.lambda_handler"
    assert cfg.code_sha_256 == "ucRYwmrtivyiEicBTcxbPvsmPWw0Sy6LAWuTPvjWX1g="
    assert cfg.timeout == 300
    assert cfg.code_size == 30280933
    assert cfg.memory_size == 3008
    assert cfg.last_modified == datetime.datetime(2018, 9, 11, 7, 45, 58, 641000, tzinfo=tzutc())


def test_environment(lambda_functionconfig):
    env = lambda_functionconfig.environment
    assert "STAGE" in env.variables
    assert env.variables["S3_BUCKET"] == "testbucket"


def test_vpcconfig(lambda_functionconfig):
    vpc = lambda_functionconfig.vpc_config
    assert vpc.vpc_id == "1234"
    assert len(vpc.subnet_ids) is 2
