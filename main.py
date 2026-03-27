# main.py

from agents.save_agent import evaluate as save_eval
from agents.spend_agent import evaluate as spend_eval
from agents.invest_agent import evaluate as invest_eval

from engine.decision_engine import decide
from engine.action_engine import take_action


def run_system(data):
    """
    data = {
        "income": int,
        "expense": int,
        "category": str,
        "history": list[{"amount": int, "category": str}]
    }
    """

    # --- Default Safety ---
    if "history" not in data:
        data["history"] = []

    if "category" not in data:
        data["category"] = "other"

    # --- Run Agents ---
    save_output = save_eval(data)
    spend_output = spend_eval(data)
    invest_output = invest_eval(data)

    outputs = [save_output, spend_output, invest_output]

    # --- Decision ---
    decision = decide(outputs)

    # --- Action ---
    action = take_action(decision, data)

    # --- Build System Response ---
    system_response = {
        "agents": outputs,
        "decision": decision,
        "action": action,
        "meta": {
            "total_agents": 3,
            "confidence_score": decision.get("score", 0),
        }
    }

    return system_response



