from dpv import get_purpose_detail
from odrl import get_action_detail

# Get action details
action_level, action_parent, action_siblings = get_action_detail("display")

# Get purpose details
purpose_level, purpose_parent, purpose_siblings = get_purpose_detail("PersonalisedAdvertising")

# Print action details
print("=== Action Details ===")
print(f"Level: {action_level}")
print(f"Parent: {action_parent}")
print(f"Siblings: {action_siblings}")

# Print purpose details
print("\n=== Purpose Details ===")
print(f"Level: {purpose_level}")
print(f"Parent: {purpose_parent}")
print(f"Siblings: {purpose_siblings}")