import os
from datetime import datetime, timedelta, timezone

CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), "checkpoint.txt")

def get_checkpoint():
    """Return last saved timestamp, or 24 hours ago if no checkpoint exists."""
    if not os.path.exists(CHECKPOINT_FILE):
        since = datetime.now(timezone.utc) - timedelta(hours=24)
        return since.strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(CHECKPOINT_FILE, "r") as f:
        val = f.read().strip()
    return val if val else (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")

def save_checkpoint(ts):
    """Save the latest timestamp string to checkpoint file."""
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(ts))

def clear_checkpoint():
    """Delete checkpoint to force a full re-fetch on next run."""
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
        print("🗑️ Checkpoint cleared.")
