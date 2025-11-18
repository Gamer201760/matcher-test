from logging import getLogger
from uuid import uuid4

import pytest

import gen.matcher.matcher_pb2 as pb2
import gen.matcher.matcher_pb2_grpc as pb2_grpc
from test.conftest import create_form_with_user_id

logger = getLogger(__name__)


def test_join_request(
    req_serivice: pb2_grpc.GroupServiceStub,
    group_service: pb2_grpc.GroupQueryServiceStub,
    form_service: pb2_grpc.FormServiceStub,
):
    user_id = uuid4()
    owner_id = uuid4()

    form_service.CreateForm(create_form_with_user_id(owner_id))
    form_service.CreateForm(create_form_with_user_id(user_id))

    group = group_service.GetGroupByUser(
        pb2.GetGroupByUserRequest(user_id=str(owner_id))
    )
    assert isinstance(group, pb2.Group)

    request = pb2.SendJoinRequestRequest(
        user_id=str(owner_id),
        group_id=group.id,
    )
    resp = req_serivice.SendJoinRequest(request)
    logger.debug(f'send request to group {group.id}')
    logger.debug(resp)
    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(owner_id)))
    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(user_id)))


def test_get_all_request(
    req_serivice: pb2_grpc.GroupServiceStub,
    group_service: pb2_grpc.GroupQueryServiceStub,
    form_service: pb2_grpc.FormServiceStub,
):
    user_id = uuid4()
    owner_id = uuid4()

    form_service.CreateForm(create_form_with_user_id(owner_id))
    form_service.CreateForm(create_form_with_user_id(user_id))

    group = group_service.GetGroupByUser(
        pb2.GetGroupByUserRequest(user_id=str(owner_id))
    )
    assert isinstance(group, pb2.Group)

    request = pb2.SendJoinRequestRequest(
        user_id=str(owner_id),
        group_id=group.id,
    )
    resp = req_serivice.SendJoinRequest(request)
    logger.debug(f'send request to group {group.id}')
    logger.debug(resp)

    request = pb2.GetReqeustsRequest(
        group_id=group.id,
    )
    resp = req_serivice.GetReqeusts(request)
    assert isinstance(resp, pb2.GetReqeustsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 1

    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(owner_id)))
    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(user_id)))


@pytest.mark.skip(reason='жду когда пофиксят group.add_user')
def test_accept_join_request(req_serivice: pb2_grpc.GroupServiceStub):
    request = pb2.AcceptJoinRequestRequest(
        owner_id='b4ff0548-e91a-4fef-9e98-6902275b8078',
        request_id='db96ba5c-a271-480b-9431-047fe208a5ed',
    )
    req_serivice.AcceptJoinRequest(request)


def test_reject_join_request(
    req_serivice: pb2_grpc.GroupServiceStub,
    group_service: pb2_grpc.GroupQueryServiceStub,
    form_service: pb2_grpc.FormServiceStub,
):
    user_id = uuid4()
    owner_id = uuid4()

    form_service.CreateForm(create_form_with_user_id(owner_id))
    form_service.CreateForm(create_form_with_user_id(user_id))

    group = group_service.GetGroupByUser(
        pb2.GetGroupByUserRequest(user_id=str(owner_id))
    )
    assert isinstance(group, pb2.Group)

    request = pb2.SendJoinRequestRequest(
        user_id=str(owner_id),
        group_id=group.id,
    )
    resp = req_serivice.SendJoinRequest(request)
    logger.debug(f'send request to group {group.id}')
    logger.debug(resp)

    request = pb2.GetReqeustsRequest(
        group_id=group.id,
    )
    resp = req_serivice.GetReqeusts(request)
    assert isinstance(resp, pb2.GetReqeustsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 1

    request = pb2.RejectJoinRequestRequest(
        owner_id=str(owner_id),
        request_id=resp.requests[0].id,
    )
    req_serivice.RejectJoinRequest(request)

    request = pb2.GetReqeustsRequest(
        group_id=group.id,
    )
    resp = req_serivice.GetReqeusts(request)
    assert isinstance(resp, pb2.GetReqeustsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 0

    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(owner_id)))
    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(user_id)))
