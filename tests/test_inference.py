from src.models.inference import score_schemes

def test_score_schemes_filtering():
    schemes = [
        {
            "scheme_id": "match",
            "eligible_income_max": 50000,
            "eligible_states": ["StateA"],
            "tags": ["health"]
        },
        {
            "scheme_id": "wrong_state",
            "eligible_income_max": 50000,
            "eligible_states": ["StateB"],
            "tags": ["health"]
        },
        {
            "scheme_id": "too_rich",
            "eligible_income_max": 30000,
            "eligible_states": ["StateA"],
            "tags": ["health"]
        }
    ]
    
    user = {
        "income": 40000,
        "state": "StateA",
        "needs": ["health"]
    }
    
    results = score_schemes(user, schemes)
    
    # Only "match" should pass the hard filters
    assert len(results) == 1
    assert results[0]["scheme_id"] == "match"
    # Base score (10) + health match (15) + state match bonus (5) = 30
    assert results[0]["match_score"] == 30

def test_score_schemes_empty_input():
    assert score_schemes({}, []) == []

def test_score_schemes_no_needs_match():
    schemes = [{"scheme_id": "S1", "tags": ["health"]}]
    user = {"needs": ["education"]}
    results = score_schemes(user, schemes)
    # Base score for passing filters (no need matches)
    assert results[0]["match_score"] == 10

def test_score_schemes_income_min_filter():
    """Test that the lower bound of income eligibility is respected."""
    schemes = [
        {"scheme_id": "high_income_only", "eligible_income_min": 50000}
    ]
    # User below minimum
    assert len(score_schemes({"income": 40000}, schemes)) == 0
    # User at minimum
    assert len(score_schemes({"income": 50000}, schemes)) == 1

def test_score_schemes_ranking_order():
    """Test that schemes with more matching tags are ranked higher."""
    schemes = [
        {"scheme_id": "partial_match", "tags": ["health"]},
        {"scheme_id": "full_match", "tags": ["health", "finance"]}
    ]
    user = {"needs": ["health", "finance"]}
    results = score_schemes(user, schemes)
    
    assert len(results) == 2
    assert results[0]["scheme_id"] == "full_match"
    # Base (10) + 2 matches * 15 = 40
    assert results[0]["match_score"] == 40
    assert results[1]["scheme_id"] == "partial_match"
    # Base (10) + 1 match * 15 = 25
    assert results[1]["match_score"] == 25

def test_score_schemes_benefits_match():
    """Test that benefits are also used for matching user needs."""
    schemes = [
        {"scheme_id": "benefit_match", "benefits": ["housing"], "tags": []}
    ]
    user = {"needs": ["housing"]}
    results = score_schemes(user, schemes)
    
    assert len(results) == 1
    # Base (10) + housing benefit match (15) = 25
    assert results[0]["match_score"] == 25