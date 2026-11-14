
import json
import sys


def check_plan(plan_path: str) -> int:
    """
    Returns 0 if every resource being created or updated has
    landlord_account_id, otherwise returns 1.
    """

    with open(plan_path, "r", encoding="utf-8") as file:
        plan = json.load(file)

    missing_tags = []

    for resource in plan.get("resource_changes", []):
        change = resource.get("change", {})
        actions = change.get("actions", [])

        # Check only resources being created or updated.
        if not any(action in ("create", "update") for action in actions):
            continue

        after = change.get("after")

        if not isinstance(after, dict):
            continue

        tags = after.get("tags")

        if not isinstance(tags, dict) or not tags.get("landlord_account_id"):
            missing_tags.append(resource.get("address", "<unknown>"))

    # Print each missing resource exactly once.
    for address in sorted(set(missing_tags)):
        print(f"Missing landlord_account_id tag: {address}")

    return 1 if missing_tags else 0


if __name__ == "__main__":
    sys.exit(check_plan(sys.argv[1]))
