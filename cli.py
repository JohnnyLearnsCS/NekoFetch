import os
import sys
import subprocess
import urllib.parse

def banner():
    print("""
   ____ _     ___                       
  / ___| |   |_ _|_ __   __ _  ___ ___ 
 | |   | |    | || '_ \ / _` |/ __/ _ \\
 | |___| |___ | || | | | (_| | (_|  __/
  \____|_____|___|_| |_|\__,_|\___\___|
                                        
    CLI Scraper Tool
    """)

def interactive_menu():
    while True:
        print("\nSelect mode:")
        print("1. Guided Mode")
        print("2. Advanced Mode")
        print("3. Exit")

        choice = input("Enter your choice [1-3]: ").strip()

        if choice == '1':
            run_guided_mode()
        elif choice == '2':
            run_advanced_mode()
        elif choice == '3':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def run_guided_mode():
    print("\nGuided Search Mode")

    # Read search engine options from searchEngine.txt
    engine_path = os.path.join(os.path.dirname(__file__), 'searchEngine.txt')
    try:
        with open(engine_path, 'r') as f:
            engines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[!] searchEngine.txt not found.")
        return

    if not engines:
        print("[!] No search engines found in searchEngine.txt.")
        return

    language = input("Enter language (e.g., 'en'): ").strip()
    ftype = input("Enter file type (e.g., 'pdf', 'mp4', 'jpg', 'all'): ").strip()
    name = input("Enter search keyword (e.g., 'lecture', 'episode'): ").strip()

    if not language or not ftype or not name:
        print("[!] All fields are required.")
        return run_guided_mode()

    scraper_path = os.path.join(os.path.dirname(__file__), "scraper.py")

    if ftype.lower() == "all":
        extensions = ['pdf', 'mp4', 'mp3', 'jpg', 'png', 'doc', 'txt']
        for selected_engine in engines:
            for ext in extensions:
                query = f"{name} filetype:{ext} lang:{language}"
                encoded_query = urllib.parse.quote_plus(query)
                url = f"https://{selected_engine}/search?q={encoded_query}"
                command = ['python3', scraper_path, '--url', url, '--type', ext, '--target', language]
                try:
                    subprocess.run(command, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"An error occurred while running scraper on {selected_engine} for {ext}: {e}")
            break  # Only use the first engine, to match previous break behavior
    else:
        for selected_engine in engines:
            query = f"{name} filetype:{ftype} lang:{language}"
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://{selected_engine}/search?q={encoded_query}"
            command = ['python3', scraper_path, '--url', url, '--type', ftype, '--target', language]
            try:
                subprocess.run(command, check=True)
                break
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while running scraper on {selected_engine}: {e}")

def run_advanced_mode():
    print("Enter the full scraper command arguments (excluding 'python3 scraper.py'):")
    args = input("> ").strip().split()
    scraper_path = os.path.join(os.path.dirname(__file__), "scraper.py")
    command = ['python3', scraper_path] + args
    run_scraper(command)

def run_scraper(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running scraper: {e}")

def main():
    banner()
    interactive_menu()

if __name__ == "__main__":
    main()