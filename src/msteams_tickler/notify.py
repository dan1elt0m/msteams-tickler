import subprocess


def notify(message: str, title: str = "", app_name: str = "", sound_name: str = ""):
    title_text = f'with title "{title}"' if title else ""
    subtitle_text = f'subtitle "{app_name}"' if app_name else ""
    soundname_text = f'sound name "{sound_name}"' if sound_name else ""

    notification_text = f'display notification "{message}" {title_text} {subtitle_text} {soundname_text}'
    subprocess.run(["osascript", "-e", notification_text], check=False)
