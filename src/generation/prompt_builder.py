SYSTEM_INSTRUCTIONS = """
You are the **Civic Scribe**, an elite Intelligence Officer for the Republic of Ghana. 
Your ONLY purpose is to provide formal, structured briefing reports to the Executive Branch.

### ABSOLUTE PROHIBITIONS:
1. **NO PYTHON CODE:** Never, under any circumstances, output Python code, 'import pandas', 'pd.read_csv', or any technical scripts.
2. **NO TUTORIALS:** Do not explain HOW to get the data. I already have the data. Just report the results found in the EVIDENTIARY CONTEXT.
3. **NO BACKTICKS:** Never use code blocks (```).

### REPORTING PROTOCOL:
- Use a formal, authoritative tone.
- Present election results or budget figures in bulleted lists or narrative summaries.
- If the data is in the context, extract the final numbers and report them as "verified findings."
- Base your response ONLY on the provided context.
"""

def build_context_block(chunks: list) -> str:
    """Format chunks into a readable context block."""
    context_parts = []
    for chunk in chunks:
        src = chunk.get("source", "unknown")
        text = chunk.get("text", "")
        context_parts.append(f"[SOURCE: {src}]\n{text}\n")
    return "\n".join(context_parts)

def build_prompt_v3(query: str, context: str) -> str:
    """Structured, strict grounding prompt (Final Production)"""
    return (
        f"{SYSTEM_INSTRUCTIONS}\n"
        f"=== EVIDENTIARY CONTEXT ===\n"
        f"{context}\n"
        f"===============\n\n"
        f"EXECUTIVE DIRECTIVE: {query}\n"
        f"SCRIBE BRIEFING REPORT:"
    )

def build_prompt_with_history(query: str, context: str, chat_history: list) -> str:
    """Combines chat history, context, and the new query."""
    history_str = ""
    for msg in chat_history[-6:]: 
        role = "EXECUTIVE" if msg["role"] == "user" else "SCRIBE"
        history_str += f"{role}: {msg['content']}\n"
    
    return (
        f"{SYSTEM_INSTRUCTIONS}\n"
        f"=== CONVERSATION HISTORY ===\n"
        f"{history_str}\n"
        f"=== EVIDENTIARY CONTEXT ===\n"
        f"{context}\n"
        f"===============\n\n"
        f"EXECUTIVE DIRECTIVE: {query}\n"
        f"SCRIBE BRIEFING REPORT:"
    )

def generate_prompt(query: str, chunks: list, version: str = "v3", chat_history: list = None) -> str:
    context = build_context_block(chunks)
    if chat_history:
        return build_prompt_with_history(query, context, chat_history)
    return build_prompt_v3(query, context)
