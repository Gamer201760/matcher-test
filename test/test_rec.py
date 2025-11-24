from logging import getLogger
from uuid import uuid4

import gen.matcher.matcher_pb2 as pb2
import gen.matcher.matcher_pb2_grpc as pb2_grpc
from test.conftest import create_form_with_user_id

logger = getLogger(__name__)


def test_random_recomendation(
    rec_serivice: pb2_grpc.FindGroupServiceStub, form_service: pb2_grpc.FormServiceStub
):
    ids = []
    for _ in range(2):
        rand_id = uuid4()
        form_service.CreateForm(create_form_with_user_id(rand_id))
        ids.append(rand_id)
    user_id = uuid4()
    form_service.CreateForm(create_form_with_user_id(user_id))
    last_resp = form_service.GetFormByUser(
        pb2.GetFormByUserRequest(user_id=str(user_id))
    )
    logger.debug(f'User params {last_resp}')

    req = pb2.FindGroupsRequest(user_id=str(user_id))
    resp = rec_serivice.FindGroups(req)
    assert isinstance(resp, pb2.FindGroupsResponse)
    logger.debug(resp)

    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(user_id)))
    for i in ids:
        form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(i)))
