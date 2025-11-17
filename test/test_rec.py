from logging import getLogger
from uuid import uuid4

import gen.matcher.matcher_pb2 as pb2
import gen.matcher.matcher_pb2_grpc as pb2_grpc
from test.conftest import create_form_with_user_id, create_random_form

logger = getLogger(__name__)


def test_random_recomendation(
    rec_serivice: pb2_grpc.FindGroupServiceStub, form_service: pb2_grpc.FormServiceStub
):
    for _ in range(10):
        form_service.CreateForm(create_random_form())
    user_id = uuid4()
    form_service.CreateForm(create_form_with_user_id(user_id))
    req = pb2.FindGroupsRequest(user_id=str(user_id))
    resp = rec_serivice.FindGroups(req)
    assert isinstance(resp, pb2.FindGroupsResponse)
    logger.info(resp)
