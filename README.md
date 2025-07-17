
"""
# NekoFetch - CLI File & Video Scraper 🐾

NekoFetch is a powerful and flexible terminal-based tool for scraping and downloading files across the web, including videos, documents, images, archives, and more.

## Features

- Search or scrape directly from a URL
- Headless browser support (Playwright) for JavaScript-heavy sites
- Supports videos (.mp4, .m3u8), audio, PDFs, images, and archives
- Language and keyword filters
- Subtitles auto-detection and download (.srt/.vtt)
- Video conversion (e.g., .m3u8 → .mp4)
- Smart guided CLI or Advanced power mode
- Secure mode with virus warning and --agree requirement
- Prevents .onion usage in beginner mode

## Advanced Mode

Use `--advanced` to disable hand-holding and customize search/filter/download behavior. Required to allow scraping `.onion` domains.

## Onion Access

Accessing `.onion` domains is **disabled by default** for safety.
If you are an advanced user and understand the risks:
- Use `--advanced`
- Use a TOR proxy/router like `torsocks` or TOR browser gateway
- Consider setting `https_proxy` or `http_proxy` in your terminal to route traffic via TOR

⚠️ NEVER access `.onion` domains without understanding legal and security implications.

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/NekoFetch.git
cd NekoFetch
python3 scraper.py --agree ...
```

## Recommended Alias

```bash
echo "alias nekofetch='python3 ~/NekoFetch/scraper.py'" >> ~/.zshrc
source ~/.zshrc
```

## License

MIT License. Built for educational and research use.
"""
