from logging import getLogger
from uuid import uuid4

import gen.matcher.matcher_pb2_grpc as pb2_grpc
from test.conftest import create_form_with_user_id

logger = getLogger(__name__)


def test_create_form(form_service: pb2_grpc.FormServiceStub):
    request = create_form_with_user_id(uuid4())
    response = form_service.CreateForm(request)
    logger.debug(response)
