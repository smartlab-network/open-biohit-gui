import subprocess
import sys
import os
from pathlib import Path


def check_and_install_dotnet():
    # Step 1: Check if .NET 6 is already installed
    try:
        result = subprocess.run(
            ["dotnet", "--list-runtimes"],
            capture_output=True, text=True, timeout=5
        )
        if "Microsoft.NETCore.App 6" in result.stdout:
            return True  # already installed, good to go
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass  # dotnet command not found at all

    # Step 2: .NET missing — try to run the bundled installer silently
    installer = Path(sys.executable).parent / "dotnet-runtime-installer.exe"

    if installer.exists():
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(
            "Installing .NET 6 Runtime",
            ".NET 6 Runtime is required and will now be installed.\n"
            "This may take a minute. Please wait."
        )
        root.destroy()

        result = subprocess.run(
            [str(installer), "/install", "/quiet", "/norestart"],
            timeout=120
        )

        if result.returncode == 0 or result.returncode == 3010:
            # 3010 means success but reboot needed
            return True
        else:
            _show_error(
                f"The .NET installer failed (code {result.returncode}).\n"
                "Please install .NET 6 Runtime manually from:\n"
                "https://dotnet.microsoft.com/download/dotnet/6.0"
            )
            return False
    else:
        # Installer not bundled — direct user to download page
        _show_error(
            "This app requires .NET 6 Runtime (x86).\n"
            "Please download and install it from:\n"
            "https://dotnet.microsoft.com/download/dotnet/6.0"
        )
        return False


def _show_error(message):
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Missing Dependency", message)
    root.destroy()


if __name__ == "__main__":
    if check_and_install_dotnet():
        from biohit_pipettor_plus.gui.gui2 import main

        main()