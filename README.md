<div align="center">

```
 ██╗  ██╗███████╗███╗   ██╗████████╗ █████╗ ██╗
 ██║  ██║██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██║
 ███████║█████╗  ██╔██╗ ██║   ██║   ███████║██║
 ██╔══██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██║██║
 ██║  ██║███████╗██║ ╚████║   ██║   ██║  ██║██║
 ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝
 ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗
 ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
 ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
 ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
 ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

**Doujinshi & Manga Bulk Downloader · Fast · Beautiful · Cross-platform**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/github/license/sinkaroid/Hentaihunter?style=for-the-badge&color=magenta)](LICENSE)
[![Stars](https://img.shields.io/github/stars/sinkaroid/Hentaihunter?style=for-the-badge&logo=github&color=yellow)](https://github.com/sinkaroid/Hentaihunter/stargazers)
[![Issues](https://img.shields.io/github/issues/sinkaroid/Hentaihunter?style=for-the-badge&color=red)](https://github.com/sinkaroid/Hentaihunter/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

---

*One command. Any site. All pages. Zero hassle.*

[**⚡ Quick Install**](#-installation) · [**📖 Usage**](#-usage) · [**🌐 Supported Sites**](#-supported-sites) · [**🤝 Contributing**](#-contributing)

</div>

---

## ✨ What is HentaiHunter?

**HentaiHunter** is a fast, beautiful Python CLI tool for bulk-downloading doujinshi, manga, and manhwa from popular sites. Give it a URL — it handles everything: gallery info, parallel image downloads, smart filename ordering, and clean progress bars.

No browser extension. No bloated GUI. No ads. Just:

```
python hentaihunter.py https://nhentai.net/g/177013/
```

---

## 🚀 Installation

### Windows — One Command *(recommended)*

Open **PowerShell** and run:

```powershell
irm https://raw.githubusercontent.com/sinkaroid/Hentaihunter/master/install.ps1 | iex
```

That's it. Python, dependencies, and a `hh` shortcut command — all set up automatically.

---

### Manual Install (Windows / Linux / macOS)

**Requirements:** Python 3.9+

```bash
# 1. Clone the repo
git clone https://github.com/sinkaroid/Hentaihunter.git
cd Hentaihunter

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python hentaihunter.py --help
```

---

## 📖 Usage

```
python hentaihunter.py [URL] [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `URL` | Gallery page URL | *(required)* |
| `-o, --output DIR` | Output folder | `./downloads` |
| `-t, --threads N` | Parallel download threads | `4` |
| `--list` | Show all supported sites | — |
| `--version` | Print version | — |

### Examples

```bash
# Download a gallery from nhentai
python hentaihunter.py https://nhentai.net/g/177013/

# Save to a custom folder with 8 threads
python hentaihunter.py https://hentaifox.com/gallery/12345/ -o D:\Manga -t 8

# Use the generic scraper on any site
python hentaihunter.py https://example-manga-site.com/chapter/1/

# List supported sites
python hentaihunter.py --list
```

### Windows shortcut (after installer)

```cmd
hh https://nhentai.net/g/177013/
hh https://hentaifox.com/gallery/12345/ -o D:\Downloads -t 8
```

---

## 🌐 Supported Sites

| Site | Status | Notes |
|------|--------|-------|
| [nhentai.net](https://nhentai.net) | ✅ Full | Metadata, tags, parallel DL |
| [hentaifox.com](https://hentaifox.com) | ✅ Full | Fast CDN |
| [hitomi.la](https://hitomi.la) | ✅ Full | Gallery support |
| [hentai2read.com](https://hentai2read.com) | ⚡ Beta | Chapter-based |
| [pururin.to](https://pururin.to) | ⚡ Beta | May require cookies |
| [e-hentai.org](https://e-hentai.org) | ⚡ Beta | Some galleries need account |
| **Any website** | 🔧 Generic | DOM parser grabs all `<img>` tags |

> **Generic mode** works on virtually any manga/doujin site — even ones not listed above. HentaiHunter scrapes all image tags from the page.

---

## ⚙️ How It Works

```
URL provided
     │
     ▼
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│ Site Detect │────▶│ Gallery Metadata │────▶│ Image URLs   │
└─────────────┘     └──────────────────┘     └──────┬───────┘
                                                     │
                           ┌─────────────────────────┘
                           ▼
                  ┌────────────────────┐
                  │  ThreadPoolExecutor │   (parallel download)
                  └────────┬───────────┘
                           │
                  ┌────────▼───────────┐
                  │  ./downloads/      │
                  │  GalleryTitle/     │
                  │  ├─ 0001.jpg       │
                  │  ├─ 0002.jpg       │
                  │  └─ ...            │
                  └────────────────────┘
```

1. **Detect** the site from the URL
2. **Fetch** gallery metadata (title, tags, page count)
3. **Collect** all image URLs via DOM parsing
4. **Download** in parallel with configurable threads
5. **Save** to numbered files in a named subfolder

---

## 📸 Demo

```
 ██╗  ██╗██╗  ██╗   HentaiHunter v2.0
 ██║  ██║██║  ██║   Doujinshi Downloader
 ███████║███████║   github.com/sinkaroid/Hentaihunter
 ╚═╝  ╚═╝╚═╝  ╚═╝

[*] Fetching info from: https://nhentai.net/g/177013/

╭──────────── Gallery Info ─────────────╮
│ [Pachimon Inro] Emergence              │
│ Pages: 225  Tags: mind break, netorare │
╰────────────────────────────────────────╯

[+] Saving to: ./downloads/Emergence/

⠸ Downloading...  ████████████████████  87%  (196/225)  0:00:12
✓ Done! 225/225 images downloaded.
  → ./downloads/Emergence/
```

---

## 🧩 Architecture

```
Hentaihunter/
├── hentaihunter.py      # Main CLI entry point
├── requirements.txt     # Dependencies
├── install.ps1          # Windows one-command installer (PowerShell)
├── install.bat          # Windows installer (CMD)
├── LICENSE
└── README.md
```

---

## 🤝 Contributing

All contributions are welcome! Here's how:

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feat/new-site-scraper`
3. Commit your changes: `git commit -m "feat: add mangadex scraper"`
4. Push and open a **Pull Request**

### Adding a new site scraper

```python
class MySiteScraper(BaseScraper):
    def get_info(self) -> dict:
        soup = self.fetch_page(self.url)
        self.title = soup.find('h1').get_text(strip=True)
        return {"title": self.title, "tags": [], "pages": "?"}
    
    def get_images(self) -> list:
        soup = self.fetch_page(self.url)
        return [img['src'] for img in soup.select('.gallery img')]
```

Then register it in `get_scraper()`:

```python
"mysite.com": MySiteScraper,
```

That's it — the download logic is handled by the base class.

---

## 📋 FAQ

**Q: Does it work on Linux/Mac?**  
A: Yes. `python hentaihunter.py` works everywhere Python runs.

**Q: A site requires login — can I use cookies?**  
A: Set them in the `SESSION` headers at the top of `hentaihunter.py`.

**Q: Downloads are slow — how do I speed up?**  
A: Increase threads: `-t 16`. The default is 4 to avoid rate-limiting.

**Q: My site isn't in the list — does it work?**  
A: Try it — the generic DOM scraper grabs all image tags. Open an issue if you need a dedicated scraper.

**Q: I'm getting 403/blocked — what do I do?**  
A: Some sites block bots. Try adding a `Referer` header or use a real browser's User-Agent string.

---

## ⚖️ Legal Disclaimer

> This tool is for **personal use and educational purposes only**. Only download content you are legally permitted to access. The authors are not responsible for any misuse. Always respect a site's `robots.txt` and Terms of Service.

---

## 📜 License

[Apache License 2.0](LICENSE) © 2024–2025 [sinkaroid](https://github.com/sinkaroid)

---

<div align="center">

**If this tool saved you time, drop a ⭐ — it keeps the project alive!**

[![Star History Chart](https://api.star-history.com/svg?repos=sinkaroid/Hentaihunter&type=Date)](https://star-history.com/#sinkaroid/Hentaihunter&Date)

</div>
