import sys

def main():
    print(r"""
         ／＞　 フ
         | 　_　_| 
       ／` ミ＿xノ 
      /　　　　 |
     /　 ヽ　　 ﾉ
    │　　|　|　|
  ／￣|　　 |　|　|
  (￣ヽ＿_ヽ_)__)
  ＼二)

  NekoFetch - File & Video Scraper
    """)

    print("\n[1] Start Searching")
    print("[2] Advanced User Mode")

    choice = input("Enter choice [1 or 2]: ")
    if choice == '1':
        print("[✓] Starting guided mode...")
        keyword = input("[?] Enter a keyword to search (e.g., 'linux guide'): ").strip()
        if keyword:
            print(f"[*] Searching for: {keyword}")
            # TODO: Implement search and display results here
        else:
            print("[!] No keyword entered. Returning to menu.")
    elif choice == '2':
        print("[✓] Launching advanced interface...")
        print("[✓] You are now in advanced mode.")
        print("Type your command with flags, e.g., --url https://google.com --type pdf")
        # TODO: Parse and handle advanced mode input
        advanced_input = input(">>> ").strip()
        if not advanced_input:
            print("[!] No command entered. Returning to menu.")
        else:
            print(f"[✓] Received command: {advanced_input}")
            # TODO: Call parsing/handling logic here
    else:
        print("[!] Invalid choice. Exiting.")
