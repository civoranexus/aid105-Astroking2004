from typing import List, Dict, Any

def score_schemes(user_data: Dict[str, Any], schemes: List[Dict[str, Any]], include_central: bool = True) -> List[Dict[str, Any]]:
    """
    Scores and filters schemes based on user profile criteria.
    Factors used:
    - Hard filters: state, income range, scheme level (optional)
    - Soft scoring: matching between user needs and scheme tags/benefits
    
    Args:
        user_data: User profile information
        schemes: List of schemes to score
        include_central: If True, include central/national schemes; if False, exclude them
    """
    scored_results = []

    user_income = user_data.get("income")
    user_state = user_data.get("state")
    user_needs = set(user_data.get("needs", []))
    
    # Normalize user needs to lowercase for better matching
    user_needs = {need.lower().strip() for need in user_needs}

    for scheme in schemes:
        score = 0
        
        # 1. Basic Filtering (Hard Constraints)
        
        # Filter by scheme level if include_central is False
        level = (scheme.get("level") or "").lower().strip()
        if not include_central and level in {"central", "national"}:
            continue
        
        # Check State Eligibility
        eligible_states = scheme.get("eligible_states") or []
        # Normalize state names to lowercase for comparison
        eligible_states_lower = [s.lower().strip() for s in eligible_states]

        if user_state:
            user_state_normalized = user_state.lower().strip()
            level = (scheme.get("level") or "").lower().strip()
            scheme_text = f"{scheme.get('title', '')} {scheme.get('description', '')}".lower()

            # If scheme has state restrictions, user's state must be in the list
            if eligible_states_lower:
                if user_state_normalized not in eligible_states_lower:
                    continue
            else:
                # No explicit state list: allow Central/National schemes
                if level in {"central", "national"}:
                    pass
                else:
                    # For State-level schemes without explicit states, try to infer from text
                    if user_state_normalized not in scheme_text:
                        continue
        # If no state provided, show all schemes

        # Check Income Eligibility - only filter OUT if user provided income and it doesn't match
        inc_min = scheme.get("eligible_income_min")
        inc_max = scheme.get("eligible_income_max")
        
        # If user provided income AND scheme has income restrictions, check them
        if user_income is not None and (inc_min is not None or inc_max is not None):
            actual_min = inc_min if inc_min is not None else 0
            actual_max = inc_max if inc_max is not None else float('inf')
            
            if not (actual_min <= user_income <= actual_max):
                continue
        # If no income provided OR scheme has no restrictions, allow it through

        # 2. Scoring (Soft Constraints)
        # Base score for passing all filters
        score = 10
        
        # Match tags/benefits against user needs
        scheme_tags = (scheme.get("tags") or []) + (scheme.get("benefits") or [])
        # Normalize scheme tags to lowercase
        scheme_tags_normalized = {tag.lower().strip() for tag in scheme_tags}
        
        matches = user_needs.intersection(scheme_tags_normalized)
        score += len(matches) * 15  # Weight for direct need match
        
        # Bonus for schemes that match user's state (even if they're national)
        if user_state and eligible_states_lower:
            if user_state.lower().strip() in eligible_states_lower:
                score += 5

        # Add the scheme to results if it passed filters
        scheme_copy = scheme.copy()
        scheme_copy["match_score"] = score
        scored_results.append(scheme_copy)

    # Sort by score descending
    scored_results.sort(key=lambda x: x["match_score"], reverse=True)

    return scored_results