# TV Wake

A small Windows utility that wakes a Google/Android TV when a Windows workstation is unlocked.

Built to solve a simple problem: a TCL Google TV used as a third monitor would enter standby after the PC stopped sending an HDMI signal, but would not wake when the HDMI signal returned.

Instead of using HDMI-CEC or triggering a fake Cast session, this utility uses the Android TV Remote Protocol to check the TV's power state and send a power command only when the TV is asleep.

## How it works

1. Windows Task Scheduler runs `wake_tv.py` when the workstation is unlocked.
2. The script connects to the TV using `androidtvremote2`.
3. It checks the TV's current power state.
4. If the TV is already on, nothing happens.
5. If the TV is asleep, the script sends a POWER command.
6. The script disconnects and exits.

The script does not run continuously in the background.

## Requirements

- Windows
- Python 3
- Google TV or Android TV supporting Android TV Remote Protocol v2
- TV and PC accessible on the same network
- `androidtvremote2`

Install dependencies:

```powershell
pip install -r requirements.txt