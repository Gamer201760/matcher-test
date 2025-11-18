from logging import getLogger

import gen.matcher.matcher_pb2 as pb2
import gen.matcher.matcher_pb2_grpc as pb2_grpc

logger = getLogger(__name__)


def test_join_request(req_serivice: pb2_grpc.GroupServiceStub):
    request = pb2.SendJoinRequestRequest(
        user_id='16a153ff-2a89-447b-b3c6-231900d2cec1',
        group_id='466c7376-5b9d-4a35-b9c5-7d97f4383298',
    )
    resp = req_serivice.SendJoinRequest(request)
    logger.debug(resp)


def test_get_all_request(req_serivice: pb2_grpc.GroupServiceStub):
    request = pb2.GetReqeustsRequest(
        group_id='466c7376-5b9d-4a35-b9c5-7d97f4383298',
    )
    resp = req_serivice.GetReqeusts(request)
    logger.debug(resp)


def test_accept_join_request(req_serivice: pb2_grpc.GroupServiceStub):
    request = pb2.AcceptJoinRequestRequest(
        owner_id='b4ff0548-e91a-4fef-9e98-6902275b8078',
        request_id='db96ba5c-a271-480b-9431-047fe208a5ed',
    )
    req_serivice.AcceptJoinRequest(request)


def test_reject_join_request(req_serivice: pb2_grpc.GroupServiceStub):
    request = pb2.RejectJoinRequestRequest(
        owner_id='b4ff0548-e91a-4fef-9e98-6902275b8078',
        request_id='db96ba5c-a271-480b-9431-047fe208a5ed',
    )
    req_serivice.RejectJoinRequest(request)
