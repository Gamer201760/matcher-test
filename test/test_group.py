from logging import getLogger
from uuid import uuid4

import gen.matcher.matcher_pb2 as pb2
import gen.matcher.matcher_pb2_grpc as pb2_grpc
from test.conftest import create_form_with_user_id

logger = getLogger(__name__)


def test_get_group_by_user(
    group_service: pb2_grpc.GroupQueryServiceStub,
    form_service: pb2_grpc.FormServiceStub,
):
    id = uuid4()
    request = create_form_with_user_id(id)
    form_service.CreateForm(request)
    req = pb2.GetGroupByUserRequest(user_id=str(id))
    resp = group_service.GetGroupByUser(req)
    assert isinstance(resp, pb2.Group)
    logger.debug(resp)

    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(id)))
