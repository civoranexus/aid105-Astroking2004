from typing import List, Dict

def score_schemes(user: Dict, schemes: List[Dict]):
    """Simple hybrid rule-based scorer.

    - Checks income eligibility and location match.
    - Adds small boost for matching user needs/tags.
    Returns list of {scheme, score, reasons} sorted by score desc.
    """
    scored = []
    user_inc = user.get("income") or 0
    user_state = (user.get("state") or "").lower()
    needs = set([n.lower() for n in user.get("needs", [])])

    for s in schemes:
        score = 0.0
        reasons = []

        min_inc = s.get("eligible_income_min")
        max_inc = s.get("eligible_income_max")

        # Income eligibility (primary)
        eligible = True
        if min_inc is not None and user_inc < min_inc:
            eligible = False
        if max_inc is not None and user_inc > max_inc:
            eligible = False

        if eligible:
            score += 0.5
            reasons.append("income_match")

        # Location match
        states = [st.lower() for st in s.get("eligible_states", [])]
        if states and user_state in states:
            score += 0.3
            reasons.append("location_match")

        # Needs/tags overlap
        tags = set([t.lower() for t in s.get("tags", [])])
        overlap = len(needs & tags)
        if overlap:
            score += 0.2 * overlap
            reasons.append("needs_match")

        scored.append({"scheme": s, "score": round(score, 3), "reasons": reasons})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
