import os

import grpc
import pytest


@pytest.fixture(scope='session')
def grpc_channel() -> grpc.Channel:
    target = os.getenv('GRPC_TARGET', 'localhost:50051')

    return grpc.insecure_channel(target)
