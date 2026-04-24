import re

def clean_text(text: str) -> str:
    """Normalize whitespace and remove non-printable characters."""
    if not isinstance(text, str):
        return ""
    # Remove multiple spaces, newlines, tabs
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def extract_keywords(text: str) -> list:
    """Extract simple keywords by taking longer words."""
    words = re.findall(r'\b\w+\b', text.lower())
    # Return words longer than 4 characters as a simple heuristic
    return list(set(word for word in words if len(word) > 4))

def get_query_type(query: str) -> str:
    """Classify query as Election, Budget, or Mixed based on keywords."""
    query_lower = query.lower()
    election_keywords = ['election', 'vote', 'candidate', 'party', 'constituency', 'region', 'npp', 'ndc']
    budget_keywords = ['budget', 'finance', 'cedi', 'economy', 'tax', 'revenue', 'expenditure', 'debt', '2025']
    
    has_election = any(k in query_lower for k in election_keywords)
    has_budget = any(k in query_lower for k in budget_keywords)
    
    if has_election and has_budget:
        return "Mixed"
    elif has_election:
        return "Election"
    elif has_budget:
        return "Budget"
    else:
        return "Mixed" # default if unknown
