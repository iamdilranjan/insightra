from langgraph.graph import StateGraph
from langchain_core.messages import SystemMessage, HumanMessage

# ---- State schema ----
class VerifyState(dict):
    """
    Expected keys:
    - answer
    - context
    - verified
    """
    pass

def build_verifier_graph(llm):
    """
    LLM is captured via closure (NOT passed in state)
    """

    def verifier_node(state: VerifyState):
        answer = state["answer"]
        context = state["context"]

        messages = [
            SystemMessage(content=(
                "You are a verification agent. "
                "Check if the answer is fully supported by the context. "
                "Reply ONLY with YES or NO."
            )),
            HumanMessage(content=f"""
Context:
{context}

Answer:
{answer}
""")
        ]

        result = llm.invoke(messages).content.strip().upper()
        state["verified"] = (result == "YES")
        return state

    graph = StateGraph(VerifyState)
    graph.add_node("verify", verifier_node)
    graph.set_entry_point("verify")
    graph.set_finish_point("verify")

    return graph.compile()
