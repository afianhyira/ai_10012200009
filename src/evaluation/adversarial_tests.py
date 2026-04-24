# A set of queries to test the RAG system

EVALUATION_QUERIES = [
    # Factual Queries
    {
        "query": "Who won the presidential election in the Ashanti Region?",
        "type": "factual",
        "expected_domain": "Election"
    },
    {
        "query": "What is the projected total tax revenue for 2025?",
        "type": "factual",
        "expected_domain": "Budget"
    },
    # Adversarial / Ambiguous
    {
        "query": "What did the president say about the budget?",
        "type": "ambiguous",
        "expected_domain": "Mixed"
    },
    {
        "query": "Who is the king of Ghana?",
        "type": "out_of_domain",
        "expected_domain": "Mixed"
    },
    # Incomplete
    {
        "query": "tell me about 2025",
        "type": "incomplete",
        "expected_domain": "Budget"
    },
    # Numeric
    {
        "query": "How many votes did NDC get in total?",
        "type": "numeric",
        "expected_domain": "Election"
    }
]
