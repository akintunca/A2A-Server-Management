from fastapi import APIRouter, Body, Request, Depends
from a2a.a2a_server import A2AServer
from a2a.a2a_types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    SendTaskRequest,
    SendTaskResponse,
    SendTaskStreamingRequest,
    SendTaskStreamingResponse,
)
from a2a.agent_task_manager import AgentTaskManager
from a2a.utils import PushNotificationSenderAuth
from agents.langgraph.agent import CurrencyAgent
from routers.payload_examples.agent import payload_example

router = APIRouter()


def get_a2a_server():
    notification_sender_auth = PushNotificationSenderAuth()
    notification_sender_auth.generate_jwk()
    task_manager = AgentTaskManager(
        agent=CurrencyAgent(), notification_sender_auth=notification_sender_auth
    )

    capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
    skill = AgentSkill(
        id="convert_currency",
        name="Currency Exchange Rates Tool",
        description="Helps with exchange values between various currencies",
        tags=["currency conversion", "currency exchange"],
        examples=["What is exchange rate between USD and GBP?"],
    )

    agent_card = AgentCard(
        name="Currency Agent",
        description="Helps with exchange rates for currencies",
        url="http://localhost:8000/api/v1/agent/currency",
        version="1.0.0",
        defaultInputModes=CurrencyAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=CurrencyAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=capabilities,
        skills=[skill],
    )

    return A2AServer(agent_card=agent_card, task_manager=task_manager)


@router.post(
    "/currency",
    response_model=SendTaskResponse | SendTaskStreamingResponse,
)
async def agent(
    payload: SendTaskRequest | SendTaskStreamingRequest = Body(
        examples=payload_example,
    ),
    a2a_server: A2AServer = Depends(get_a2a_server),
):
    """
    Agent endpoint for handling JSON-RPC requests.

    The request must follow JSON-RPC 2.0 specification with the following structure:
    - method: tasks/send for single response, tasks/sendSubscribe for streaming
    - params: must contain message with text parts for the query
    """
    request = Request(scope={"type": "http"})
    request._json = payload.model_dump()

    result = await a2a_server.process_request(request)
    return result


@router.get("/currency/.well-known/agent.json")
async def get_agent_card(a2a_server: A2AServer = Depends(get_a2a_server)):
    """
    Get agent card endpoint.
    """
    return await a2a_server.get_agent_card()
