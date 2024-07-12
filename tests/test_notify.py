from unittest.mock import patch

from msteams_tickler.notify import notify


@patch("subprocess.run")
def test_notify(mock_run):
    # Call the function with test data
    notify("Test message", "Test title", "Test app", "Test sound")

    # Build the expected command
    expected_command = [
        "osascript",
        "-e",
        'display notification "Test message" with title "Test title" subtitle "Test app" sound name "Test sound"',
    ]

    # Assert that the function called subprocess.run with the expected command
    mock_run.assert_called_once_with(expected_command, check=False)
