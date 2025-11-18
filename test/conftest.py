import os
from random import randint
from uuid import UUID, uuid4

import grpc
import names
import pytest

import gen.matcher.matcher_pb2 as pb2
import gen.matcher.matcher_pb2_grpc as pb2_grpc


@pytest.fixture(scope='session')
def grpc_channel() -> grpc.Channel:
    target = os.getenv('GRPC_TARGET', 'localhost:50051')

    return grpc.insecure_channel(target)


@pytest.fixture(scope='session')
def form_service(grpc_channel: grpc.Channel) -> pb2_grpc.FormServiceStub:
    return pb2_grpc.FormServiceStub(grpc_channel)


@pytest.fixture(scope='session')
def group_service(grpc_channel: grpc.Channel) -> pb2_grpc.GroupQueryServiceStub:
    return pb2_grpc.GroupQueryServiceStub(grpc_channel)


@pytest.fixture(scope='session')
def rec_serivice(grpc_channel: grpc.Channel) -> pb2_grpc.FindGroupServiceStub:
    return pb2_grpc.FindGroupServiceStub(grpc_channel)


@pytest.fixture(scope='session')
def req_serivice(grpc_channel: grpc.Channel) -> pb2_grpc.GroupServiceStub:
    return pb2_grpc.GroupServiceStub(grpc_channel)


def gen_random_parameters() -> pb2.Parameters:
    return pb2.Parameters(
        name=names.get_first_name(),
        surname=names.get_last_name(),
        age=randint(17, 25),
        budget=randint(12000, 60000),
        roommates_count=randint(2, 5),
        room_count=randint(1, 5),
        month=randint(1, 12 * 10),
        sex=pb2.Sex.SEX_MALE,
        user_type=pb2.USER_TYPE_STUDENT,
    )


def create_form_with_user_id(user_id: UUID) -> pb2.CreateFormRequest:
    return pb2.CreateFormRequest(
        user_id=str(user_id), parameters=gen_random_parameters()
    )


def create_random_form() -> pb2.CreateFormRequest:
    return create_form_with_user_id(uuid4())
