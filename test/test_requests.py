from logging import getLogger
from uuid import uuid4

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

    request = pb2.GetRequestsRequest(
        group_id=group.id,
    )
    resp = req_serivice.GetRequests(request)
    assert isinstance(resp, pb2.GetRequestsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 1

    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(owner_id)))
    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(user_id)))


def test_accept_join_request(
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

    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(owner_id)))
    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(user_id)))


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

    request = pb2.GetRequestsRequest(
        group_id=group.id,
    )
    resp = req_serivice.GetRequests(request)
    assert isinstance(resp, pb2.GetRequestsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 1

    request = pb2.RejectJoinRequestRequest(
        owner_id=str(owner_id),
        request_id=resp.requests[0].id,
    )
    req_serivice.RejectJoinRequest(request)

    request = pb2.GetRequestsRequest(
        group_id=group.id,
    )
    resp = req_serivice.GetRequests(request)
    assert isinstance(resp, pb2.GetRequestsResponse)
    logger.debug(resp)
    assert len(resp.requests) == 0

    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(owner_id)))
    form_service.DeleteForm(pb2.DeleteFormRequest(user_id=str(user_id)))
