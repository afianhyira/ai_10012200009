def build_context_block(chunks: list) -> str:
    """Format chunks into a readable context block."""
    context_parts = []
    for chunk in chunks:
        cid = chunk.get("chunk_id", "unknown")
        src = chunk.get("source", "unknown")
        text = chunk.get("text", "")
        context_parts.append(f"[ID: {cid} | Source: {src}]\n{text}\n")
    return "\n".join(context_parts)

def build_prompt_v1(query: str, context: str) -> str:
    """Basic Prompt"""
    return f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

def build_prompt_v2(query: str, context: str) -> str:
    """Hallucination-Controlled Prompt"""
    return (
        f"You are an AI assistant. Answer the question based ONLY on the context below.\n"
        f"If the answer is not in the context, say 'I do not have enough information'.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\nAnswer:"
    )

def build_prompt_v3(query: str, context: str) -> str:
    """Structured, strict grounding prompt (Final Production)"""
    return (
        f"=== CONTEXT ===\n"
        f"{context}\n"
        f"===============\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )

def build_prompt_with_history(query: str, context: str, chat_history: list) -> str:
    """Combines chat history, context, and the new query."""
    history_str = ""
    # Keep last 3 exchanges to maintain focus and context window
    for msg in chat_history[-6:]: 
        role = "Executive" if msg["role"] == "user" else "Assistant"
        history_str += f"{role}: {msg['content']}\n"
    
    return (
        f"=== CONVERSATION HISTORY ===\n"
        f"{history_str}\n"
        f"=== EVIDENTIARY CONTEXT ===\n"
        f"{context}\n"
        f"===============\n\n"
        f"New Directive: {query}\n"
        f"Response:"
    )

def generate_prompt(query: str, chunks: list, version: str = "v3", chat_history: list = None) -> str:
    context = build_context_block(chunks)
    if chat_history:
        return build_prompt_with_history(query, context, chat_history)
    
    if version == "v1":
        return build_prompt_v1(query, context)
    elif version == "v2":
        return build_prompt_v2(query, context)
    else:
        return build_prompt_v3(query, context)
