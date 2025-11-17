from logging import getLogger
from random import randint
from uuid import uuid4

import names

import gen.matcher.matcher_pb2 as pb2
import gen.matcher.matcher_pb2_grpc as pb2_grpc

logger = getLogger(__name__)


def test_create_form(form_service: pb2_grpc.FormServiceStub):
    params = pb2.Parameters(
        name=names.get_first_name(),
        surname=names.get_last_name(),
        age=randint(17, 25),
        budget=randint(12000, 60000),
        roommates_count=randint(1, 5),
        room_count=randint(1, 5),
        month=randint(1, 12 * 10),
        sex=pb2.Sex.SEX_MALE,
        user_type=pb2.USER_TYPE_STUDENT,
    )
    request = pb2.CreateFormRequest(user_id=str(uuid4()), parameters=params)
    response = form_service.CreateForm(request)
    logger.debug(response)
