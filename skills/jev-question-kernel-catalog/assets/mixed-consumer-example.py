"""Trusted, side-effect-free example consumer for mixed-support-intake-demo.

Illustrative thresholds are not operationally qualified. Return a planned queue,
never execute a refund, send email, or modify a ticket.
"""


def decide(state, answers):
    if not state["message"].strip():
        return "human_review"
    route = answers["request_kind"]
    refund = answers["refund_requested"]["noul"]
    urgency = answers["urgency"]["score"]
    if urgency >= 1.5 or route["confidence"] < 0.5:
        return "human_review"
    if route["choice"] == "refund" and refund >= 0.75:
        return "billing_review"
    if route["choice"] == "receipt_only" and refund <= 0.25:
        return "receipt_queue"
    return "human_review"
