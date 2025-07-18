#!/usr/bin/env python3

import os
import subprocess
import sys

def main():
    print("[*] Installing NekoFetch...")

    # Install dependencies from requirements.txt
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("[!] Failed to install dependencies from requirements.txt")
        sys.exit(1)

    # Make neko.py executable
    neko_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "neko.py")
    if not os.path.isfile(neko_path):
        print(f"[!] {neko_path} does not exist.")
        sys.exit(1)
    os.chmod(neko_path, 0o755)

    # Symlink neko.py to /usr/local/bin/neko
    symlink_path = "/usr/local/bin/neko"
    try:
        if os.path.islink(symlink_path) or os.path.exists(symlink_path):
            os.remove(symlink_path)
        os.symlink(neko_path, symlink_path)
    except PermissionError:
        print("[!] Permission denied: You might need to run this script with sudo.")
        sys.exit(1)
    except OSError as e:
        print(f"[!] Failed to create symlink: {e}")
        sys.exit(1)

    print("[✓] Installed. Run with: neko")

if __name__ == "__main__":
    main()