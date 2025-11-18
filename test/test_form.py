from datetime import UTC, datetime
from logging import getLogger
from uuid import uuid4

import grpc
import pytest

import gen.matcher.matcher_pb2 as pb2
import gen.matcher.matcher_pb2_grpc as pb2_grpc
from test.conftest import create_form_with_user_id, gen_random_parameters

logger = getLogger(__name__)


def test_create_form(form_service: pb2_grpc.FormServiceStub):
    request = create_form_with_user_id(uuid4())
    form_service.CreateForm(request)


def test_get_form(form_service: pb2_grpc.FormServiceStub):
    id = uuid4()
    form_req = create_form_with_user_id(id)
    form_service.CreateForm(form_req)

    req = pb2.GetFormByUserRequest(user_id=str(id))
    resp = form_service.GetFormByUser(req)
    logger.debug(resp)
    logger.debug(form_req)

    assert isinstance(resp, pb2.Form)
    assert resp.parameters.name == form_req.parameters.name
    assert resp.parameters.budget == form_req.parameters.budget
    assert resp.parameters.roommates_count == form_req.parameters.roommates_count
    assert resp.parameters.room_count == form_req.parameters.room_count
    assert resp.user_id == form_req.user_id
    diff = abs((datetime.now(UTC) - resp.created_at.ToDatetime(UTC)).total_seconds())
    assert diff <= 1


def test_delete_form(form_service: pb2_grpc.FormServiceStub):
    id = uuid4()
    form_req = create_form_with_user_id(id)
    form_service.CreateForm(form_req)

    resp = form_service.GetFormByUser(pb2.GetFormByUserRequest(user_id=str(id)))
    logger.debug(resp)

    req = pb2.DeleteFormRequest(user_id=str(id))
    form_service.DeleteForm(req)
    with pytest.raises(grpc.RpcError) as e:
        form_service.GetFormByUser(pb2.GetFormByUserRequest(user_id=str(id)))
    logger.debug(e.value)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND


def test_update_form(form_service: pb2_grpc.FormServiceStub):
    id = uuid4()
    form_req = create_form_with_user_id(id)
    form_service.CreateForm(form_req)

    last_resp = form_service.GetFormByUser(pb2.GetFormByUserRequest(user_id=str(id)))
    logger.debug(last_resp)

    new_params = gen_random_parameters()
    logger.debug(new_params)
    form_service.UpdateForm(
        pb2.UpdateFormRequest(user_id=str(id), parameters=new_params)
    )

    new_resp = form_service.GetFormByUser(pb2.GetFormByUserRequest(user_id=str(id)))
    logger.debug(new_resp)
