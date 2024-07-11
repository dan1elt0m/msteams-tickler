import subprocess
import time
from pathlib import Path

from mac_notifications import client


def open_teams():
    """Opens MS Teams"""
    subprocess.Popen(["open", "-a", "Microsoft Teams"])


def notify(wait_time: int = 10):
    """Sends a notification and waits 10 second for user to click on the open teams button"""
    icon = Path(__file__).parent / "img" / "expired.png"
    client.create_notification(
        title="Teams token expired!",
        subtitle="Token expired",
        icon=icon,
        action_callback=open_teams,
        action_button_str="Open Teams",
    )
    time.sleep(wait_time)
    client.stop_listening_for_callbacks()
