from agent.service import run_agent

EVAL_CASES = [
    ("u_101", "I was double charged on my latest invoice", "billing"),
    ("u_102", "Cannot log in after resetting my password", "account"),
    ("u_103", "Webhook deliveries are returning HTTP 500", "technical"),
    ("u_104", "Need a refund for last month's plan", "billing"),
]

def test_tool_trajectory_and_schema():
    result = run_agent("u_101", "I was double charged on my latest invoice")
    assert result.tools_used == ["lookup_account"]
    assert result.category == "billing"
    assert len(result.summary) >= 5

def test_eval_suite_threshold():
    passed = 0
    for user_id, prompt_text, expected_category in EVAL_CASES:
        res = run_agent(user_id, prompt_text)
        if res.category == expected_category and "lookup_account" in res.tools_used:
            passed += 1

    pass_rate = passed / len(EVAL_CASES)
    assert pass_rate >= 0.75, f"Eval pass rate {pass_rate:.0%} below 75% threshold"
