import os
import requests
from urllib.parse import urlparse
import time

def download_file(url, download_dir, filename_override=None):
    if filename_override:
        local_filename = filename_override
    else:
        local_filename = os.path.basename(urlparse(url).path) or "downloaded_file"
    local_path = os.path.join(download_dir, local_filename)
    try:
        with requests.get(url, stream=True, timeout=15) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0
            start_time = time.time()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        elapsed = time.time() - start_time
                        speed = downloaded / elapsed if elapsed > 0 else 0
                        eta = (total_size - downloaded) / speed if speed > 0 else 0
                        percent = (downloaded / total_size) * 100 if total_size else 0
                        bar = '=' * int(50 * downloaded / total_size) if total_size else ''
                        print(f"\r[{bar:<50}] {percent:5.1f}% {downloaded}/{total_size} bytes ETA: {int(eta)}s", end='')
            print()  # For newline after progress bar
        print(f"[+] Downloaded: {local_filename}")
    except Exception as e:
        print(f"\033[41m[!] Failed to download {url}: {e}\033[0m")