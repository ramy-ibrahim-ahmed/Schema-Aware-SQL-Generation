from ..graph.state import State
from ..store.nlp.interface import BaseNLP
from ..store.prompts.factory import PromptFactory
from ..core.enums import GeminiChatEnums


def RespondAgent(state: State, nlp: BaseNLP) -> State:
    user_message = state.get("user_message", "")
    sql_result = state.get("sql_result", "")
    system_instruction = PromptFactory().get_prompt("system_respond")
    messages = [
        {
            GeminiChatEnums.ROLE.value: GeminiChatEnums.USER.value,
            GeminiChatEnums.CONTENT.value: user_message,
        },
        {
            GeminiChatEnums.ROLE.value: GeminiChatEnums.USER.value,
            GeminiChatEnums.CONTENT.value: str(sql_result),
        },
    ]
    response = nlp.chat(
        model_name="gemini-2.5-flash",
        instructions=system_instruction,
        messages=messages,
    )
    return {"response": response}
