"""
Bridge — IPC between the Python host and the UE4SS Lua mod running inside Palworld.

Protocol: Named pipe on Windows (\\\\.\\pipe\\PalatableAPI).
Messages: newline-delimited JSON.
  Send:    { "cmd": "set_player_health", "args": { ... } }
  Receive: { "ok": true, "message": "..." } or { "ok": false, "message": "..." }

The Lua mod listens on the pipe. The Python host connects, sends a command,
reads a response, and closes.
"""

import json
import sys
from typing import Any

PIPE_NAME = r"\\.\pipe\PalatableAPI"
TIMEOUT_MS = 5000

_connected = False


def is_connected() -> bool:
    """Check whether the pipe is reachable (Palworld + mod are running)."""
    try:
        _open_pipe()
        return True
    except Exception:
        return False


def send(payload: dict) -> dict:
    """
    Send a command payload to the Lua mod and return the response dict.
    Raises BridgeError if the pipe is not available or the call times out.
    """
    if sys.platform != "win32":
        raise BridgeError("Named pipe IPC is Windows-only. Run on Windows.")

    try:
        pipe = _open_pipe()
    except Exception as e:
        raise BridgeError(
            f"Cannot connect to Palworld. Is the game running with UE4SS and "
            f"the PalatableAPI mod loaded?\nDetails: {e}"
        ) from e

    try:
        message = (json.dumps(payload) + "\n").encode("utf-8")
        import win32file  # type: ignore
        win32file.WriteFile(pipe, message)

        # Read response (up to 64KB)
        _, response_bytes = win32file.ReadFile(pipe, 65536)
        response = json.loads(response_bytes.decode("utf-8").strip())
        return response
    except Exception as e:
        raise BridgeError(f"Pipe communication error: {e}") from e
    finally:
        try:
            import win32file
            win32file.CloseHandle(pipe)
        except Exception:
            pass


def _open_pipe():
    """Open the named pipe. Returns a win32 handle."""
    import win32file  # type: ignore
    import pywintypes  # type: ignore

    try:
        handle = win32file.CreateFile(
            PIPE_NAME,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None,
        )
        return handle
    except pywintypes.error as e:
        raise BridgeError(f"Failed to open pipe '{PIPE_NAME}': {e}") from e


class BridgeError(Exception):
    pass
