# TV Wake

A small Windows utility that wakes a Google TV or Android TV when a Windows workstation is unlocked.

This project was built to solve a simple problem: a TCL Google TV being used as a third PC monitor would enter standby after the computer stopped sending an HDMI signal, but it would not wake back up when the HDMI signal returned.

TV Wake uses the Android TV Remote Protocol to check the TV's current power state and sends a POWER command only when the TV is asleep.

The script runs when Windows is unlocked, wakes the TV if necessary, then disconnects and exits. It does not run continuously in the background.

## How it works

Windows Task Scheduler launches `wake_tv.py` when the workstation is unlocked.

The script:

1. Connects to the TV using `androidtvremote2`.
2. Waits briefly for the TV's current state.
3. Checks whether the TV is already awake.
4. If the TV is already on, nothing happens.
5. If the TV is asleep, a POWER command is sent.
6. The connection is closed and the script exits.

Because the TV's state is checked before sending POWER, the script avoids accidentally turning an already-running TV off.

## Requirements

- Windows
- Python 3
- A Google TV or Android TV supporting Android TV Remote Protocol v2
- The TV and PC must be accessible to each other over the network
- `androidtvremote2`

This project was originally created and tested with a TCL Google TV running Android TV 12. Other Google TV and Android TV devices may work but have not necessarily been tested.

## Installation

Clone or download this repository.

Open a terminal in the project folder and create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependency:

```powershell
pip install -r requirements.txt
```

## Configure the TV

Make a copy of:

```text
config.example.json
```

and name the copy:

```text
config.json
```

Edit `config.json`:

```json
{
  "tv_ip": "192.168.1.100",
  "client_name": "Windows PC"
}
```

Replace `192.168.1.100` with the IP address of your TV.

`client_name` is the name that will identify this computer to the TV during pairing.

It is a good idea to give the TV a DHCP reservation or otherwise keep its IP address from changing.

`config.json` is excluded from Git so your local configuration is not committed to the repository.

## Pair with the TV

Before the wake script can control the TV, the computer must be paired with it.

Make sure the TV is turned on, then run:

```powershell
python pair_tv.py
```

A pairing code should appear on the TV.

Enter that code when prompted in the terminal.

After successful pairing, two files will be created:

```text
cert.pem
key.pem
```

These files identify the computer as a paired remote.

**Do not share or commit `key.pem`.**

Both files are excluded by `.gitignore`.

Normally, pairing only needs to be completed once.

## Test the wake script

Run:

```powershell
python wake_tv.py
```

If the TV is already awake, the script should report that it is on and do nothing.

If the TV is asleep or in standby, the script should send the POWER command and wake it.

Once this works manually, Windows Task Scheduler can run it automatically.

## Run automatically when Windows is unlocked

Open **Task Scheduler** in Windows and create a new task.

### General

Give the task a name such as:

```text
Wake Office TV
```

Select:

```text
Run only when user is logged on
```

Running with highest privileges should not normally be necessary.

### Trigger

Create a new trigger:

```text
Begin the task: On workstation unlock
```

You can configure the trigger for your specific Windows user.

### Action

Create a new action:

```text
Action: Start a program
```

For **Program/script**, use the `pythonw.exe` inside the project's virtual environment.

For example:

```text
C:\Path\To\tv-wake\.venv\Scripts\pythonw.exe
```

For **Add arguments**, enter the full path to `wake_tv.py`:

```text
"C:\Path\To\tv-wake\wake_tv.py"
```

For **Start in**, enter the project directory:

```text
C:\Path\To\tv-wake
```

Using `pythonw.exe` instead of `python.exe` prevents a terminal window from briefly appearing every time the workstation is unlocked.

Save the task.

You can test it by allowing the TV to enter standby, locking Windows with `Win + L`, and then unlocking the workstation.

## Project files

```text
tv-wake/
├── .gitignore
├── config.example.json
├── LICENSE
├── pair_tv.py
├── README.md
├── requirements.txt
└── wake_tv.py
```

After local setup, you will also have:

```text
config.json
cert.pem
key.pem
.venv/
```

These local files are excluded from Git.

## Troubleshooting

### The TV cannot be found

Make sure the TV and PC can communicate over the network and verify that the IP address in `config.json` is correct.

Some networks may block communication between devices even when both have internet access.

### The TV's IP address changed

Update `tv_ip` in `config.json`.

A DHCP reservation for the TV can prevent this from happening.

### Pairing fails

Run `pair_tv.py` again and make sure the pairing code displayed by the TV is entered correctly.

### The script works manually but not from Task Scheduler

Double-check the full paths used for:

- `pythonw.exe`
- `wake_tv.py`
- the **Start in** directory

Using absolute paths avoids problems caused by Task Scheduler starting programs from a different working directory.

### The TV is already on

Nothing should happen. This is intentional.

`wake_tv.py` checks the TV's current power state before sending the POWER command.

## Security

The pairing process creates a certificate and private key used to authenticate this computer to the TV.

The following files are intentionally excluded from this repository:

```text
config.json
cert.pem
key.pem
```

Do not publish your private key.

## Credits

This project uses [`androidtvremote2`](https://github.com/tronikos/androidtvremote2) by [tronikos](https://github.com/tronikos), an open-source Python library implementing Android TV Remote Protocol v2.

`androidtvremote2` is licensed under the Apache License 2.0.

TV Wake is an independent project and is not affiliated with Google, Android, TCL, or the `androidtvremote2` project.

## License

TV Wake is released under the MIT License.

See [LICENSE](LICENSE) for details.