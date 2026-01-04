# agents/analyst.py
from memory.vector_memory import VectorMemory
from memory.graph_memory import GraphMemory
from orchestration.state import ResearchState

vector_mem = VectorMemory()
graph_mem = GraphMemory()

# thresholds — tweakable knobs
MIN_VECTOR_HITS = 3
MIN_AVG_SCORE = 0.6
MIN_GRAPH_HITS = 1


def analyst_agent(state: ResearchState) -> ResearchState:
    query = state["query"]

    # --- 1. Vector retrieval ---
    vector_hits = vector_mem.search(query, k=10)
    state["vector_results"] = vector_hits

    if not vector_hits:
        state["analysis_decision"] = "need_more_info"
        return state

    avg_score = sum(v["score"] for v in vector_hits) / len(vector_hits)

    # --- 2. Graph reasoning ---
    graph_hits = []
    for hit in vector_hits:
        # simple heuristic: try multiple entity anchors
        tokens = hit["chunk"].split()[:5]
        for t in tokens:
            graph_hits.extend(graph_mem.query_entities(t))

    state["graph_results"] = graph_hits

    # --- 3. Analyst decision logic ---
    if len(vector_hits) < MIN_VECTOR_HITS:
        state["analysis_decision"] = "need_more_info"
        return state

    if avg_score < MIN_AVG_SCORE:
        state["analysis_decision"] = "need_more_info"
        return state

    if len(graph_hits) < MIN_GRAPH_HITS:
        # still acceptable — graph memory is a bonus
        state["analysis_decision"] = "ready"
    else:
        state["analysis_decision"] = "ready"

    # --- 4. Assemble context (do NOT summarize here) ---
    context_blocks = []
    for v in vector_hits:
        context_blocks.append(f"[SOURCE]\n{v['chunk']}")

    for g in graph_hits[:10]: 
        context_blocks.append(
            f"[GRAPH] {g['source']} --{g['relation']}--> {g['target']}"
        )

    state["final_context"] = "\n\n".join(context_blocks)

    return state
