# engine/decision_engine.py

PRIORITY = {
    "restrict": 3,
    "invest": 2,
    "allow": 1,
    "avoid": 0,
    "hold": -1
}

def decide(outputs):
    # Normalize scores and attach priority
    for o in outputs:
        o["priority"] = PRIORITY.get(o.get("action"), 0)

    # Step 1: sort by score, then by priority
    sorted_outputs = sorted(
        outputs,
        key=lambda x: (x["score"], x["priority"]),
        reverse=True
    )

    best = sorted_outputs[0]

    # Step 2: conflict awareness
    actions = [o["action"] for o in outputs]

    conflict = False
    if "restrict" in actions and "allow" in actions:
        conflict = True
    if "invest" in actions and "allow" in actions:
        conflict = True

    # Step 3: attach meta decision info
    decision = {
        "agent": best["agent"],
        "score": best["score"],
        "action": best["action"],
        "reason": best["reason"],
        "conflict": conflict,
        "all_agents": outputs
    }

    return decision
