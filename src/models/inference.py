from typing import List, Dict, Any

def score_schemes(user_data: Dict[str, Any], schemes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scores and filters schemes based on user profile criteria.
    Factors used:
    - Hard filters: state, income range, age range (if user age provided)
    - Soft scoring: matching between user needs and scheme tags/benefits
    """
    scored_results = []

    user_income = user_data.get("income") or 0
    user_state = user_data.get("state")
    user_age = user_data.get("age")
    user_needs = set(user_data.get("needs", []))

    for scheme in schemes:
        score = 0
        # 1. Basic Filtering (Hard Constraints)
        # Check State Eligibility
        eligible_states = scheme.get("eligible_states") or []
        # Normalize state names to lowercase for comparison
        eligible_states_lower = [s.lower() for s in eligible_states]
        if eligible_states_lower and user_state and user_state.lower() not in eligible_states_lower:
            continue

        # Check Income Eligibility
        inc_min = scheme.get("eligible_income_min") or 0
        inc_max = scheme.get("eligible_income_max")
        if inc_max is None:
            inc_max = float('inf')
        if not (inc_min <= user_income <= inc_max):
            continue

        # Check Age Eligibility (only if user_age provided)
        age_min = scheme.get("eligible_age_min")
        age_max = scheme.get("eligible_age_max")
        if user_age is not None:
            if age_min is not None and user_age < age_min:
                continue
            if age_max is not None and user_age > age_max:
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