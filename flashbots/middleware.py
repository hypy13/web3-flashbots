from typing import Any, Callable

from web3 import Web3
from web3.middleware import Middleware
from web3.types import RPCEndpoint, RPCResponse

from .provider import FlashbotProvider

FLASHBOTS_METHODS = [
    "eth_sendBundle",
    "eth_callBundle",
    "eth_cancelBundle",
    "eth_sendPrivateTransaction",
    "eth_cancelPrivateTransaction",
    "flashbots_getBundleStats",
    "flashbots_getUserStats",
    "flashbots_getBundleStatsV2",
    "flashbots_getUserStatsV2",
]


def construct_flashbots_middleware(
    flashbots_provider: FlashbotProvider,
) -> Middleware:
    """Captures Flashbots RPC requests and sends them to the Flashbots endpoint
    while also injecting the required authorization headers

    Keyword arguments:
    flashbots_provider -- An HTTP provider instantiated with any authorization headers
    required
    """

    def flashbots_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any]
    ) -> Callable[[RPCEndpoint, Any], RPCResponse]:
        def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
            if method not in FLASHBOTS_METHODS:
                return make_request(method, params)
            else:
                # otherwise intercept it and POST it
                return flashbots_provider.make_request(method, params)

        return middleware

    return flashbots_middleware
