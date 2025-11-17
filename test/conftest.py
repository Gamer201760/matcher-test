import os

import grpc
import pytest

import gen.matcher.matcher_pb2_grpc as pb2_grpc


@pytest.fixture(scope='session')
def grpc_channel() -> grpc.Channel:
    target = os.getenv('GRPC_TARGET', 'localhost:50051')

    return grpc.insecure_channel(target)


@pytest.fixture(scope='session')
def form_service(grpc_channel: grpc.Channel) -> pb2_grpc.FormServiceStub:
    return pb2_grpc.FormServiceStub(grpc_channel)
