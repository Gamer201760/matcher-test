from logging import getLogger
from uuid import uuid4

import grpc
import pytest

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


def test_leave_group_once(
    group_service: pb2_grpc.GroupQueryServiceStub,
    form_service: pb2_grpc.FormServiceStub,
):
    id = uuid4()
    form_service.CreateForm(create_form_with_user_id(id))

    with pytest.raises(grpc.RpcError) as e:
        group_service.LeaveGroup(pb2.LeaveGroupRequest(user_id=str(id)))

    det = e.value.details() or ''
    assert 'Вы не можете выйти из группы, когда остались только вы' in det

    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(id)))


def test_leave_group(
    group_service: pb2_grpc.GroupQueryServiceStub,
    form_service: pb2_grpc.FormServiceStub,
    req_serivice: pb2_grpc.GroupServiceStub,
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
        user_id=str(user_id),
        group_id=group.id,
    )
    resp = req_serivice.SendJoinRequest(request)
    logger.debug(f'send request to group:\n{group}')
    logger.debug(resp)

    resp = req_serivice.GetRequests(
        pb2.GetRequestsRequest(
            group_id=group.id,
        )
    )
    assert isinstance(resp, pb2.GetRequestsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 1

    request = pb2.AcceptJoinRequestRequest(
        owner_id=str(owner_id),
        request_id=resp.requests[0].id,
    )
    req_serivice.AcceptJoinRequest(request)

    resp = req_serivice.GetRequests(
        pb2.GetRequestsRequest(
            group_id=group.id,
        )
    )
    assert isinstance(resp, pb2.GetRequestsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 0

    resp = group_service.ListGroupMembers(
        pb2.ListGroupMembersRequest(group_id=group.id)
    )
    assert isinstance(resp, pb2.ListGroupMembersResponse)
    logger.debug(resp)
    for member in resp.members:
        assert member.user_id in [str(owner_id), str(user_id)]

    fin_group = group_service.GetGroup(pb2.GetGroupRequest(group_id=group.id))
    assert isinstance(fin_group, pb2.Group)
    logger.debug(f'Final group:\n{fin_group}')
    assert fin_group.id == group.id
    assert fin_group.owner_id == group.owner_id

    group_service.LeaveGroup(pb2.LeaveGroupRequest(user_id=str(user_id)))
    resp = group_service.ListGroupMembers(
        pb2.ListGroupMembersRequest(group_id=group.id)
    )
    assert isinstance(resp, pb2.ListGroupMembersResponse)
    logger.debug(resp)
    for member in resp.members:
        assert member.user_id in [str(owner_id)]


def test_kick_group(
    group_service: pb2_grpc.GroupQueryServiceStub,
    form_service: pb2_grpc.FormServiceStub,
    req_serivice: pb2_grpc.GroupServiceStub,
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
        user_id=str(user_id),
        group_id=group.id,
    )
    resp = req_serivice.SendJoinRequest(request)
    logger.debug(f'send request to group:\n{group}')
    logger.debug(resp)

    resp = req_serivice.GetRequests(
        pb2.GetRequestsRequest(
            group_id=group.id,
        )
    )
    assert isinstance(resp, pb2.GetRequestsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 1

    request = pb2.AcceptJoinRequestRequest(
        owner_id=str(owner_id),
        request_id=resp.requests[0].id,
    )
    req_serivice.AcceptJoinRequest(request)

    resp = req_serivice.GetRequests(
        pb2.GetRequestsRequest(
            group_id=group.id,
        )
    )
    assert isinstance(resp, pb2.GetRequestsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 0

    resp = group_service.ListGroupMembers(
        pb2.ListGroupMembersRequest(group_id=group.id)
    )
    assert isinstance(resp, pb2.ListGroupMembersResponse)
    logger.debug(resp)
    for member in resp.members:
        assert member.user_id in [str(owner_id), str(user_id)]

    fin_group = group_service.GetGroup(pb2.GetGroupRequest(group_id=group.id))
    assert isinstance(fin_group, pb2.Group)
    logger.debug(f'Final group:\n{fin_group}')
    assert fin_group.id == group.id
    assert fin_group.owner_id == group.owner_id

    group_service.KickGroup(
        pb2.KickGroupRequest(user_id=str(user_id), owner_id=str(owner_id))
    )
    resp = group_service.ListGroupMembers(
        pb2.ListGroupMembersRequest(group_id=group.id)
    )
    assert isinstance(resp, pb2.ListGroupMembersResponse)
    logger.debug(resp)
    for member in resp.members:
        assert member.user_id in [str(owner_id)]
