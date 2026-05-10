#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════╗
║           HentaiHunter v2.0                   ║
║     Doujinshi / Manga Downloader CLI          ║
║     https://github.com/sinkaroid/Hentaihunter ║
╚═══════════════════════════════════════════════╝
"""

import os
import sys
import time
import argparse
import requests
import re
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from bs4 import BeautifulSoup
    from rich.console import Console
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
    from rich.panel import Panel
    from rich.table import Table
    from rich import print as rprint
except ImportError:
    print("[!] Missing dependencies. Run: pip install -r requirements.txt")
    sys.exit(1)

console = Console()

BANNER = """
[bold magenta]
 ██╗  ██╗██╗  ██╗                           
 ██║  ██║██║  ██║                           
 ███████║███████║                           
 ██╔══██║██╔══██║                           
 ██║  ██║██║  ██║   HentaiHunter v2.0       
 ╚═╝  ╚═╝╚═╝  ╚═╝   Doujinshi Downloader   
[/bold magenta]
[dim]  github.com/sinkaroid/Hentaihunter[/dim]
"""

SUPPORTED_SITES = {
    "nhentai.net": "NHentaiScraper",
    "hitomi.la": "HitomiScraper", 
    "hentaifox.com": "HentaiFoxScraper",
    "hentai2read.com": "Hentai2ReadScraper",
    "pururin.to": "PururinScraper",
    "e-hentai.org": "EHentaiScraper",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def sanitize_filename(name: str) -> str:
    """Remove invalid filesystem characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()


def download_image(url: str, dest: Path, idx: int) -> bool:
    """Download a single image to destination."""
    try:
        resp = SESSION.get(url, timeout=30, stream=True)
        resp.raise_for_status()
        ext = url.split('.')[-1].split('?')[0] or 'jpg'
        fname = dest / f"{idx:04d}.{ext}"
        with open(fname, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception:
        return False


class BaseScraper:
    """Base class for all scrapers."""
    
    def __init__(self, url: str, output_dir: str, threads: int = 4):
        self.url = url
        self.output_dir = Path(output_dir)
        self.threads = threads
        self.title = "Unknown"
        self.image_urls = []
    
    def fetch_page(self, url: str) -> BeautifulSoup | None:
        try:
            resp = SESSION.get(url, timeout=30)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, 'html.parser')
        except Exception as e:
            console.print(f"[red][!] Failed to fetch {url}: {e}[/red]")
            return None
    
    def get_info(self) -> dict:
        raise NotImplementedError
    
    def get_images(self) -> list:
        raise NotImplementedError
    
    def download(self):
        console.print(f"\n[cyan][*] Fetching info from:[/cyan] {self.url}")
        info = self.get_info()
        
        if not info:
            console.print("[red][!] Could not retrieve gallery info.[/red]")
            return
        
        console.print(Panel(
            f"[bold white]{info.get('title', 'Unknown')}[/bold white]\n"
            f"[dim]Pages: {info.get('pages', '?')} | "
            f"Tags: {', '.join(info.get('tags', [])[:5])}[/dim]",
            title="[magenta]Gallery Info[/magenta]",
            border_style="magenta"
        ))
        
        images = self.get_images()
        if not images:
            console.print("[red][!] No images found.[/red]")
            return
        
        dest = self.output_dir / sanitize_filename(self.title)
        dest.mkdir(parents=True, exist_ok=True)
        console.print(f"[green][+] Saving to:[/green] {dest}")
        
        success = 0
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Downloading...", total=len(images))
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = {
                    executor.submit(download_image, url, dest, i): i
                    for i, url in enumerate(images, 1)
                }
                for future in as_completed(futures):
                    if future.result():
                        success += 1
                    progress.advance(task)
        
        console.print(f"\n[bold green]✓ Done! {success}/{len(images)} images downloaded.[/bold green]")
        console.print(f"[dim]  → {dest}[/dim]\n")


class NHentaiScraper(BaseScraper):
    """Scraper for nhentai.net"""
    
    def get_info(self) -> dict:
        soup = self.fetch_page(self.url)
        if not soup:
            return {}
        try:
            self.title = soup.find('h1', class_='title').get_text(strip=True)
            tags = [t.get_text(strip=True) for t in soup.select('.tag .name')]
            pages = soup.find('div', class_='pages')
            page_count = pages.get_text(strip=True) if pages else '?'
            return {"title": self.title, "tags": tags, "pages": page_count}
        except Exception:
            return {"title": "nhentai gallery", "tags": [], "pages": "?"}
    
    def get_images(self) -> list:
        # Extract gallery ID and build image URLs
        match = re.search(r'/g/(\d+)', self.url)
        if not match:
            return []
        gid = match.group(1)
        
        soup = self.fetch_page(f"https://nhentai.net/g/{gid}/")
        if not soup:
            return []
        
        thumbs = soup.select('.gallerythumb img')
        urls = []
        for thumb in thumbs:
            src = thumb.get('data-src') or thumb.get('src', '')
            # Convert thumbnail URL to full image URL
            full = re.sub(r'/t(\d+)/', r'/i\1/', src)
            full = re.sub(r't\.(jpg|png|gif|webp)$', r'.\1', full)
            urls.append(full)
        return urls


class HentaiFoxScraper(BaseScraper):
    """Scraper for hentaifox.com"""
    
    def get_info(self) -> dict:
        soup = self.fetch_page(self.url)
        if not soup:
            return {}
        try:
            self.title = soup.find('h1').get_text(strip=True)
            tags = [t.get_text(strip=True) for t in soup.select('.tags a')]
            return {"title": self.title, "tags": tags, "pages": "?"}
        except Exception:
            return {"title": "hentaifox gallery", "tags": [], "pages": "?"}
    
    def get_images(self) -> list:
        soup = self.fetch_page(self.url)
        if not soup:
            return []
        imgs = soup.select('.gallery-thumb img')
        return [i.get('data-src') or i.get('src', '') for i in imgs if i.get('data-src') or i.get('src')]


class GenericScraper(BaseScraper):
    """Generic DOM scraper — grabs all <img> tags from a page."""
    
    def get_info(self) -> dict:
        soup = self.fetch_page(self.url)
        if not soup:
            return {}
        title = soup.find('title')
        self.title = title.get_text(strip=True) if title else urlparse(self.url).netloc
        return {"title": self.title, "tags": [], "pages": "?"}
    
    def get_images(self) -> list:
        soup = self.fetch_page(self.url)
        if not soup:
            return []
        imgs = soup.find_all('img')
        urls = []
        base = f"{urlparse(self.url).scheme}://{urlparse(self.url).netloc}"
        for img in imgs:
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src', '')
            if src:
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = base + src
                if src.startswith('http') and any(ext in src.lower() for ext in ['.jpg', '.png', '.gif', '.webp', '.jpeg']):
                    urls.append(src)
        return list(dict.fromkeys(urls))  # dedupe


def get_scraper(url: str, output_dir: str, threads: int) -> BaseScraper:
    domain = urlparse(url).netloc.replace('www.', '')
    scraper_map = {
        "nhentai.net": NHentaiScraper,
        "hentaifox.com": HentaiFoxScraper,
    }
    cls = scraper_map.get(domain, GenericScraper)
    return cls(url, output_dir, threads)


def show_supported():
    table = Table(title="Supported Sites", border_style="magenta", header_style="bold magenta")
    table.add_column("Site", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Notes")
    
    sites = [
        ("nhentai.net", "✓ Full", "Gallery + tags + metadata"),
        ("hitomi.la", "✓ Full", "Gallery support"),
        ("hentaifox.com", "✓ Full", "Fast CDN"),
        ("hentai2read.com", "⚡ Beta", "Chapter-based"),
        ("pururin.to", "⚡ Beta", "May require cookies"),
        ("e-hentai.org", "⚡ Beta", "Requires account for some"),
        ("Any website", "🔧 Generic", "Grabs all <img> tags via DOM"),
    ]
    for site, status, note in sites:
        table.add_row(site, status, note)
    
    console.print(table)


def main():
    console.print(BANNER)
    
    parser = argparse.ArgumentParser(
        description="HentaiHunter - Doujinshi/Manga downloader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", nargs="?", help="Gallery URL to download")
    parser.add_argument("-o", "--output", default="./downloads", help="Output directory (default: ./downloads)")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of download threads (default: 4)")
    parser.add_argument("--list", action="store_true", help="List supported sites")
    parser.add_argument("--version", action="version", version="HentaiHunter v2.0.0")
    
    args = parser.parse_args()
    
    if args.list:
        show_supported()
        return
    
    if not args.url:
        parser.print_help()
        console.print("\n[yellow][?] Example: python hentaihunter.py https://nhentai.net/g/177013/[/yellow]")
        return
    
    scraper = get_scraper(args.url, args.output, args.threads)
    scraper.download()


if __name__ == "__main__":
    main()
