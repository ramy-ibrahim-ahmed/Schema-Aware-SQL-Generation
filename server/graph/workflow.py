from functools import partial
from langgraph.graph import StateGraph, END
from ..agents import IdentifyAgent, RespondAgent, SQLAgent, ExecuteNode
from ..store.nlp.interface import BaseNLP
from ..core.enums import AgentNamesEnums
from .routers import correct_router
from .state import State


def init_workflow(db_path, nlp: BaseNLP):
    identify = partial(IdentifyAgent, nlp=nlp, db_path=db_path)
    respond = partial(RespondAgent, nlp=nlp)
    sql = partial(SQLAgent, nlp=nlp)
    execute = partial(ExecuteNode, db_path=db_path)

    workflow = StateGraph(State)

    workflow.add_node(AgentNamesEnums.IDENTIFY.value, identify)
    workflow.add_node(AgentNamesEnums.RESPOND.value, respond)
    workflow.add_node(AgentNamesEnums.SQL_GENERATE.value, sql)
    workflow.add_node(AgentNamesEnums.SQL_EXECUTE.value, execute)

    workflow.set_entry_point(AgentNamesEnums.IDENTIFY.value)
    workflow.add_edge(
        AgentNamesEnums.IDENTIFY.value, AgentNamesEnums.SQL_GENERATE.value
    )
    workflow.add_edge(
        AgentNamesEnums.SQL_GENERATE.value, AgentNamesEnums.SQL_EXECUTE.value
    )
    workflow.add_conditional_edges(
        AgentNamesEnums.SQL_EXECUTE.value,
        correct_router,
        {
            AgentNamesEnums.RESPOND.value: AgentNamesEnums.RESPOND.value,
            AgentNamesEnums.SQL_GENERATE.value: AgentNamesEnums.SQL_GENERATE.value,
        },
    )
    workflow.add_edge(AgentNamesEnums.RESPOND.value, END)

    return workflow.compile()
