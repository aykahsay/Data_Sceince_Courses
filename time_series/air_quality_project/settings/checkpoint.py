import os
from datetime import datetime, timezone

CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), "checkpoint.txt")

def get_checkpoint():
    """Returns last loaded timestamp string, or None on first run."""
    if not os.path.exists(CHECKPOINT_FILE):
        return None
    with open(CHECKPOINT_FILE, "r") as f:
        val = f.read().strip()
    return val if val else None

def save_checkpoint(ts):
    """Save latest timestamp as checkpoint."""
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(ts))

def clear_checkpoint():
    """Delete checkpoint to force a fresh 1000-record pull on next run."""
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
        print("🗑️ Checkpoint cleared — next run fetches latest 1000 fresh.")
