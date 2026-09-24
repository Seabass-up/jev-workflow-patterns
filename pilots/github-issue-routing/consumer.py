"""Side-effect-free, predeclared title-routing policy for the public pilot."""


def decide(state, answers):
    if not state["title"].strip():
        return "human_review"
    kind = answers["issue_kind"]
    failure = answers["existing_behavior_failure"]["noul"]
    selected = kind["choice"]
    probability = kind["probabilities"][selected]
    if selected == "unclear" or probability < 0.80 or kind["confidence"] < 0.50:
        return "human_review"
    if selected == "bug" and failure >= 0.70:
        return "bug_queue"
    if selected == "enhancement" and failure <= 0.30:
        return "enhancement_queue"
    return "human_review"
