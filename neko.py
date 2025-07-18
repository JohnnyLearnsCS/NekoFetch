import os
import subprocess

def main():
    try:
        subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "cli.py")])
    except KeyboardInterrupt:
        print("\n[!] Exiting gracefully.")

if __name__ == "__main__":
    main()
