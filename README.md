# Contributing to HentaiHunter

Thanks for your interest in contributing! 🎉

## Ways to Contribute

- 🐛 **Bug reports** — open an Issue with steps to reproduce
- ✨ **New site scrapers** — see the guide in README.md
- 📝 **Documentation** — improve examples, fix typos
- 🌐 **Translations** — help localize the README

## Development Setup

```bash
git clone https://github.com/sinkaroid/Hentaihunter.git
cd Hentaihunter
pip install -r requirements.txt
python hentaihunter.py --help
```

## Pull Request Guidelines

- One feature/fix per PR
- Test your changes with at least one real URL
- Follow existing code style
- Update README if you add a new supported site

## Adding a Scraper

1. Create a class inheriting `BaseScraper`
2. Implement `get_info()` and `get_images()`  
3. Register in `get_scraper()` dict
4. Test it, then open a PR!

See existing scrapers (`NHentaiScraper`, `HentaiFoxScraper`) for examples.
