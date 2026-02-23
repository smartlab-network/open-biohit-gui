import subprocess
import sys
import os
from pathlib import Path


def check_and_install_dotnet():
    try:
        result = subprocess.run(
            ["dotnet", "--list-runtimes"],
            capture_output=True, text=True, timeout=5
        )
        if "Microsoft.NETCore.App 6" in result.stdout:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    installer = Path(sys.executable).parent / "dotnet-runtime-installer.exe"

    if installer.exists():
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            ".NET 6 Runtime is required and will now be installed.\nThis may take a minute. Please wait.",
            "Installing .NET 6 Runtime",
            0x40
        )
        result = subprocess.run(
            [str(installer), "/install", "/quiet", "/norestart"],
            timeout=120
        )
        if result.returncode == 0 or result.returncode == 3010:
            return True
        else:
            _show_error(f"The .NET installer failed (code {result.returncode}).\nPlease install .NET 6 Runtime manually from:\nhttps://dotnet.microsoft.com/download/dotnet/6.0")
            return False
    else:
        _show_error("This app requires .NET 6 Runtime (x86).\nPlease download and install it from:\nhttps://dotnet.microsoft.com/download/dotnet/6.0")
        return False


def _show_error(message):
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, message, "Missing Dependency", 0x10)


# ↓ THIS runs directly, no if __name__ check
if check_and_install_dotnet():
    from biohit_pipettor_plus.gui.gui2 import main
    main()