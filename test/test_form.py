from logging import getLogger
from uuid import uuid4

import gen.matcher.matcher_pb2 as pb2
import gen.matcher.matcher_pb2_grpc as pb2_grpc

logger = getLogger(__name__)


def test_create_form(form_service: pb2_grpc.FormServiceStub):
    params = pb2.Parameters(
        name='Oleg',
        surname='Krivov',
        age=18,
        budget=20000,
        roommates_count=3,
        room_count=3,
        month=12,
        sex=pb2.Sex.SEX_MALE,
        user_type=pb2.USER_TYPE_STUDENT,
    )
    request = pb2.CreateFormRequest(user_id=str(uuid4()), parameters=params)
    response = form_service.CreateForm(request)
    logger.debug(response)
