# 🐾 NekoFetch - File & Video Scraper CLI

NekoFetch is a terminal-based intelligent file and media scraper that lets users search, find, and optionally download documents, media, and files across the internet.

Supports: `.pdf`, `.zip`, `.mkv`, `.mp4`, `.mp3`, `.jpg`, `.png`, subtitles, and more.

---

## 🚀 Features

- 🔍 Simple CLI Interface
- 🧠 Guided prompts with optional `--advanced` mode
- 🎯 Filter by type: `--pdf`, `--zip`, `--audio`, `--video`, etc.
- 📁 Queue system for downloading, viewing, and tracking
- 📡 Uses Presearch, DuckDuckGo, and decentralized [SearxNG](https://searx.space/) instances
- ⚠️ Built-in virus warning prompt (requires `--agree`)
- 🧪 Experimental support for `.onion` links (Advanced mode only)
- 💬 Supports subtitle downloads for videos (with language filter)
- 📦 Auto-installs dependencies with progress bar

---

## 🛠 Installation

### Option 1: Python Package

```bash
pip install --user .
```

Then run it anywhere with:

```bash
neko
```

### Option 2: Easy Shell Installer

```bash
git clone https://github.com/JohnnyLearnsCS/nekofetch.git
cd nekofetch
bash install.sh
```

Run with:

```bash
neko
```

---

## 🧪 Advanced Mode

```bash
neko --advanced
```

Advanced mode disables safety rails and lets you:

- Customize your search engine
- Access `.onion` domains (Tor proxy/router required)
- Change scraping depth, headers, and rules
- Run direct links or advanced queries

---

## ⚠️ Safety Disclaimer

NekoFetch **does not verify** file contents.

> You **must** type `--agree` to confirm you're aware files may be harmful.  
> Type `--disagree` to cancel and exit.

---

## 🌐 .onion / Tor Usage

If you want to search `.onion` domains:

- You must run in `--advanced` mode
- You need to route traffic through [Tor](https://www.torproject.org/)
- This feature is disabled by default for safety

📖 [Tor Setup Guide (External)](https://tb-manual.torproject.org/)

---

## 🧷 Topics

- `cli`
- `scraper`
- `downloader`
- `file-search`
- `pdf`
- `video`
- `tor`
- `open-source`
- `python3`
- `terminal-tool`

---

## 📜 License

[MIT License](LICENSE)

---

> NekoFetch is a personal experiment in open-source tooling and safe scraping. Not responsible for misuse.
