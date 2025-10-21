from langchain_core.messages import ToolMessage
from langgraph.graph import END


def should_regenerate_query(state: State) -> str:
    messages = state["messages"]
    error_count = state.get("error_count", 0)
    last_message = messages[-1]

    # If last message is tool with error and in the valid retries range
    # go to correction else manager.
    if (
        isinstance(last_message, ToolMessage)
        and last_message.content.startswith("Error:")
        and error_count <= MAX_QUERY_RETRIES
    ):
        return "generate_sql_query"
    else:
        return "manager"


def route_after_manager(state: State) -> str:
    if state.get("final_answer"):
        return END
    elif state.get("instruction"):
        return "identify_relevant_tables"


from langchain_core.runnables import RunnableLambda
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode


# When a tool error the state key 'error' will contain thre error
# so we run the handler to get that error and formate it and add it to the messages for correction
def handle_tool_error(state: State) -> State:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ],
    }


sql_execution_node = ToolNode([db_query_tool]).with_fallbacks(
    [RunnableLambda(handle_tool_error)], exception_key="error"
)
