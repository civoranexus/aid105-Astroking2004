from typing import List, Dict, Any

def score_schemes(user_data: Dict[str, Any], schemes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scores and filters schemes based on user profile criteria.
    """
    scored_results = []
    
    user_income = user_data.get("income") or 0
    user_state = user_data.get("state")
    user_needs = set(user_data.get("needs", []))

    for scheme in schemes:
        score = 0
        # 1. Basic Filtering (Hard Constraints)
        # Check State Eligibility
        eligible_states = scheme.get("eligible_states") or []
        if eligible_states and user_state and user_state not in eligible_states:
            continue
            
        # Check Income Eligibility
        inc_min = scheme.get("eligible_income_min") or 0
        inc_max = scheme.get("eligible_income_max") or float('inf')
        if not (inc_min <= user_income <= inc_max):
            continue

        # 2. Scoring (Soft Constraints)
        # Match tags/benefits against user needs
        scheme_tags = set((scheme.get("tags") or []) + (scheme.get("benefits") or []))
        matches = user_needs.intersection(scheme_tags)
        score += len(matches) * 10  # Weight for direct need match
        
        # Add the scheme to results if it passed filters
        scheme_copy = scheme.copy()
        scheme_copy["match_score"] = score
        scored_results.append(scheme_copy)

    # Sort by score descending
    scored_results.sort(key=lambda x: x["match_score"], reverse=True)
    
    return scored_results