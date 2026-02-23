import subprocess
import sys
from pathlib import Path
import ctypes


def msg(text, title="BiohitPipettorPlus", icon=0x40):
    ctypes.windll.user32.MessageBoxW(0, text, title, icon)


def check_and_install_dotnet():
    try:
        result = subprocess.run(
            ["dotnet", "--list-runtimes"],
            capture_output=True, text=True, timeout=5
        )
        msg(f"Runtimes found:\n{result.stdout if result.stdout else 'NONE'}")

        if "Microsoft.NETCore.App 6" in result.stdout:
            msg(".NET 6 found! Launching app...")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        msg(f"dotnet command failed:\n{str(e)}", icon=0x10)

    installer = Path(sys.executable).parent / "dotnet-runtime-installer.exe"
    msg(f"Looking for installer at:\n{installer}\nExists: {installer.exists()}")

    if installer.exists():
        msg("Installer found! Starting .NET install...")
        result = subprocess.run(
            [str(installer), "/install", "/quiet", "/norestart"],
            timeout=120
        )
        msg(f"Installer finished with code: {result.returncode}")

        if result.returncode == 0 or result.returncode == 3010:
            msg("Install successful! Relaunching app...")
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit(0)
        else:
            msg(f"Installer failed with code {result.returncode}", icon=0x10)
            sys.exit(1)
    else:
        msg("Installer NOT found in bundle!", icon=0x10)
        sys.exit(1)


def _show_error(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Missing Dependency", 0x10)


if check_and_install_dotnet():
    from biohit_pipettor_plus.gui.gui2 import main

    main()