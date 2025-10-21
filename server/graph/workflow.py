from langgraph.graph import StateGraph, END


workflow = StateGraph(State)

workflow.add_node("manager", manager)
workflow.add_node("identify_relevant_tables", identify_relevant_tables)
workflow.add_node("generate_sql_query", generate_sql_query)
workflow.add_node("execute_sql", sql_execution_node)

workflow.set_entry_point("manager")

workflow.add_conditional_edges(
    "manager",
    route_after_manager,
    {
        "identify_relevant_tables": "identify_relevant_tables",
        END: END,
    },
)

workflow.add_edge("identify_relevant_tables", "generate_sql_query")
workflow.add_edge("generate_sql_query", "execute_sql")

workflow.add_conditional_edges(
    "execute_sql",
    should_regenerate_query,
    {
        "generate_sql_query": "generate_sql_query",
        "manager": "manager",
    },
)

GRAPH = workflow.compile()
