import os
import platform
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, unquote
from playwright.sync_api import sync_playwright
from download import download_file

# Global download queue for batch downloads
download_queue = []  # now stores (title, url, optional_filename)

def get_default_download_path():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Downloads")
    elif system == "Darwin":
        return os.path.join(os.environ["HOME"], "Desktop")
    else:
        return os.path.join(os.environ["HOME"], "Downloads")

def find_links(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            html = page.content()
            browser.close()
            soup = BeautifulSoup(html, "html.parser")
        results = []
        seen = set()
        for link_tag in soup.find_all("a", href=True):
            href = link_tag["href"].strip()
            # Skip internal anchors
            if href.startswith("#"):
                continue
            # Detect and decode Mojeek redirect links
            if href.startswith("https://mojeek.com/out?u="):
                parsed = urlparse(href)
                qs = parse_qs(parsed.query)
                u_vals = qs.get("u")
                if u_vals:
                    decoded_url = unquote(u_vals[0])
                    final_url = decoded_url
                else:
                    continue
            # Absolute http/https links
            elif href.startswith("http"):
                final_url = href
            # Relative links (not anchors)
            elif not urlparse(href).scheme and not href.startswith("#"):
                final_url = urljoin(url, href)
            else:
                continue
            # Avoid duplicates
            if final_url in seen:
                continue
            seen.add(final_url)
            # Get link text
            link_text = link_tag.get_text(strip=True)
            if not link_text:
                # fallback to domain if no text
                parsed_url = urlparse(final_url)
                link_text = parsed_url.netloc or final_url
            results.append((link_text, final_url))
        return results
    except Exception as e:
        print(f"[!] Failed to fetch or parse URL: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="CLI Search Engine Result Previewer")
    parser.add_argument("--url", required=True, help="Target URL to scrape")
    parser.add_argument("--type", required=True, help="File extension to download (e.g., pdf, txt, docx)")
    parser.add_argument("--target", help="Optional download directory")
    args = parser.parse_args()

    # No longer filter by file extension, just preview links.
    print(f"[*] Scraping {args.url} for links...")

    import webbrowser
    download_dir = args.target if args.target else get_default_download_path()

    def show_links_and_menu(links, parent_url=None):
        if not links:
            print("[!] No links found.")
            return
        print("[*] Found links:")
        for idx, (title, link_url) in enumerate(links, 1):
            parsed = urlparse(link_url)
            domain = parsed.netloc or "(no-domain)"
            # Try to extract file extension
            path = parsed.path
            file_ext = ""
            if '.' in os.path.basename(path):
                file_ext = os.path.basename(path).split('.')[-1]
                ext_str = f".{file_ext}"
            else:
                ext_str = ""
            print(f"[{idx}] {title} - {domain} [{ext_str}]")
            # If the title is not the URL, show the full link below
            if title != link_url:
                print(f"    {link_url}")

        while True:
            try:
                selection = input("Enter link number: ").strip()
                if not selection.isdigit() or not (1 <= int(selection) <= len(links)):
                    print("[!] Invalid selection. Please enter a valid link number.")
                    continue
                sel_idx = int(selection) - 1
                selected_title, selected_url = links[sel_idx]
            except (ValueError, IndexError):
                print("[!] Invalid selection. Please enter a valid link number.")
                continue
            # Show options
            print()
            print("[O] Open in browser")
            print("[D] Download file")
            print("[G] Dig deeper")
            print("[V] View Queue")
            print("[B] Back to main menu")
            opt = input("Choose an option [O/D/G/V/B]: ").strip().upper()
            if opt == "O":
                print(f"[*] Opening {selected_url} in browser...")
                webbrowser.open(selected_url)
            elif opt == "D":
                print()
                print("[Sa] Save As...")
                print("[S] Single Download")
                print("[B] Batch Download")
                download_opt = input("Choose a download option [Sa/S/B]: ").strip().upper()
                if download_opt == "SA":
                    save_path = input("Enter full file path to save as: ").strip()
                    if save_path:
                        print(f"[*] Downloading {selected_url} to {save_path} ...")
                        download_file(selected_url, os.path.dirname(save_path), filename_override=os.path.basename(save_path))
                    else:
                        print("[!] No path entered. Cancelled.")
                elif download_opt == "S":
                    print(f"[*] Downloading {selected_url} ...")
                    download_file(selected_url, download_dir)
                elif download_opt == "B":
                    # Add to global batch download queue with no filename override
                    download_queue.append((selected_title, selected_url, None))
                    print(f"[+] Added to batch queue: {selected_title}")
                else:
                    print("[!] Invalid download option. Please choose Sa, S, or B.")
            elif opt == "G":
                print(f"[*] Digging deeper into {selected_url} ...")
                sub_links = find_links(selected_url)
                show_links_and_menu(sub_links, parent_url=selected_url)
            elif opt == "V":
                while True:
                    if not download_queue:
                        print("[*] Batch queue is empty.")
                        break
                    else:
                        print("[*] Batch Queue:")
                        for i, (title, url, filename_override) in enumerate(download_queue, 1):
                            display_name = filename_override if filename_override else url
                            print(f"[{i}] {title} - {display_name}")
                        print("[R] Remove item from queue")
                        print("[C] Clear all")
                        print("[E] Edit file name before download")
                        print("[B] Back to link menu")
                        queue_opt = input("Choose an option [R/C/E/B]: ").strip().upper()
                        if queue_opt == "R":
                            rem_input = input("Enter item number to remove: ").strip()
                            if not rem_input.isdigit():
                                print("[!] Invalid input. Please enter a valid number.")
                                continue
                            rem_idx = int(rem_input) - 1
                            if 0 <= rem_idx < len(download_queue):
                                removed_item = download_queue.pop(rem_idx)
                                print(f"[+] Removed from queue: {removed_item[0]}")
                            else:
                                print("[!] Invalid item number.")
                        elif queue_opt == "C":
                            download_queue.clear()
                            print("[*] Batch queue cleared.")
                        elif queue_opt == "E":
                            edit_input = input("Enter item number to edit filename: ").strip()
                            if not edit_input.isdigit():
                                print("[!] Invalid input. Please enter a valid number.")
                                continue
                            edit_idx = int(edit_input) - 1
                            if 0 <= edit_idx < len(download_queue):
                                current_title, current_url, current_override = download_queue[edit_idx]
                                new_filename = input("Enter new filename (with extension): ").strip()
                                if new_filename:
                                    download_queue[edit_idx] = (current_title, current_url, new_filename)
                                    print(f"[+] Filename updated for '{current_title}' to '{new_filename}'")
                                else:
                                    print("[!] No filename entered. Cancelled.")
                            else:
                                print("[!] Invalid item number.")
                        elif queue_opt == "B":
                            break
                        else:
                            print("[!] Invalid option. Please choose R, C, E, or B.")
            elif opt == "B":
                print("[*] Returning to main menu.")
                return
            else:
                print("[!] Invalid option. Please choose O, D, G, V, or B.")

    links = find_links(args.url)
    show_links_and_menu(links)

if __name__ == "__main__":
    main()
    # After main menu loop, process batch downloads if any
    if download_queue:
        print("\n[*] Starting batch download...")
        # Use the same download_dir as chosen above
        for title, url, filename_override in download_queue:
            print(f"[*] Downloading {title} ...")
            download_file(url, download_dir, filename_override=filename_override)
