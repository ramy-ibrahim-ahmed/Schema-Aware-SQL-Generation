from .state import State
from ..core.enums import AgentNamesEnums


def correct_router(state: State) -> str:
    if state.get("error_message", "") and state.get("error_count") < 3:
        return AgentNamesEnums.SQL_GENERATE.value

    return AgentNamesEnums.RESPOND.value
