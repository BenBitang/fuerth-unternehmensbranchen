# 🚀 START HERE

Welcome! This guide will help you get up and running in less than 5 minutes.

## ⚡ Ultra-Quick Start (5 minutes)

```bash
cd /Users/benb/Documents/scraping
bash run_scraper.sh
```

That's it! The script will:
1. ✅ Check your system
2. ✅ Install dependencies
3. ✅ Download the browser
4. ✅ Scrape all 1,743 companies
5. ✅ Save to CSV & JSON

**Result:** `furth_companies.csv` will be created with all company data.

---

## 📋 Before You Start

### Verify Prerequisites
```bash
# Check if you have Python 3.7+
python3 --version

# Check if you have pip
pip3 --version
```

If either command fails, see the **"I Need Help"** section below.

### Optional: Check System
```bash
python3 check_system.py
```

This verifies everything is set up correctly.

---

## 🎯 Choose Your Method

### Method 1: Fully Automatic ⭐ (Easiest)
```bash
bash run_scraper.sh
```
- Installs everything automatically
- Starts scraping immediately
- Best for first-time users

### Method 2: Manual with Debug
```bash
python3 furth_scraper_advanced.py --debug
```
- See what's happening
- Good for troubleshooting
- More control

### Method 3: See the Browser
```bash
python3 furth_scraper_advanced.py --show
```
- Watch the browser window
- Verify it's working
- Helpful for debugging

### Method 4: Everything
```bash
python3 furth_scraper_advanced.py --show --debug
```
- Browser window visible
- Debug output enabled
- Maximum information

---

## ✨ What You Get

After running the scraper, you'll have:

### CSV File (`furth_companies.csv`)
```
Company Name,Industry Branch
Company ABC,Manufacturing
Company XYZ,Retail Services
```
- Ready for Excel, Google Sheets, etc.
- ~1,700 rows of company data
- ~1-2 MB file size

### JSON File (`furth_companies.json`)
```json
{
  "timestamp": "2026-01-17T17:45:23",
  "total_companies": 1743,
  "companies": [
    {"name": "Company ABC", "branch": "Manufacturing"},
    ...
  ]
}
```
- Programmatically parseable
- Includes timestamp
- Full metadata

---

## 🆘 I Need Help

### "Python 3 not found"
```bash
# Option 1: Use Homebrew
brew install python3

# Option 2: Download from python.org
# https://www.python.org/downloads/
```

### "pip3 not found"
```bash
# Reinstall/upgrade pip
python3 -m pip install --upgrade pip
```

### "Permission denied on run_scraper.sh"
```bash
chmod +x /Users/benb/Documents/scraping/run_scraper.sh
```

### "Script gets stuck or hangs"
```bash
# Kill the script
Ctrl + C

# Try with debug mode
python3 furth_scraper_advanced.py --debug

# Check your internet connection
ping google.com
```

### "ModuleNotFoundError: No module named 'playwright'"
```bash
# Install dependencies manually
pip3 install -r requirements.txt

# Install Playwright browsers
python3 -m playwright install chromium
```

### "Still having issues?"
1. Read: `README.md` (detailed documentation)
2. Read: `INSTALLATION.md` (setup guide)
3. Run: `check_system.py` (system verification)
4. Use `--debug` flag for detailed output

---

## 🎓 Documentation Guide

- **START HERE** (this file) - Quick start guide
- **QUICKSTART.md** - Commands and options reference
- **README.md** - Detailed technical documentation
- **INSTALLATION.md** - Full installation guide with troubleshooting
- **PROJECT_SUMMARY.md** - Project overview and features

---

## ⏱️ Timeline

| Step | Time | What Happens |
|------|------|---|
| Installation | 1-2 min | Dependencies installed |
| Browser download | 1-2 min | Playwright browser downloaded |
| Initial load | 10 sec | Website loads |
| Scraping | 5-15 min | All 1,743 companies extracted |
| **Total** | **8-20 min** | Depends on internet speed |

---

## 🛠️ Available Scrapers

If the main scraper doesn't work, try alternatives:

```bash
# Original Selenium version
python3 furth_scraper.py

# Lightweight version
python3 furth_scraper_simple.py

# Async Playwright version
python3 furth_scraper_playwright.py
```

Each handles different website structures, so if one fails, others might work.

---

## 💡 Pro Tips

1. **First time?** Run with `--show` to see the browser
2. **Slow?** Check your internet speed, not the script
3. **Debugging?** Use `--debug` flag for detailed output
4. **Want JSON?** Also exported automatically as `furth_companies.json`
5. **Need more data?** Check the JSON file for metadata
6. **Re-run anytime?** Just execute the script again

---

## 🔄 Regular Updates

To re-run the scraper later:

```bash
# Simple re-run
bash run_scraper.sh

# Or direct command
python3 furth_scraper_advanced.py
```

Each run overwrites the previous CSV/JSON files with fresh data.

---

## ✅ Verification Checklist

- [ ] Python 3.7+ installed
- [ ] run_scraper.sh is executable
- [ ] furth_companies.csv created
- [ ] Contains ~1,700+ companies
- [ ] Can open in Excel/Sheets
- [ ] furth_companies.json also created

---

## 📞 Quick Reference

```bash
# Check what Python version you have
python3 --version

# Check if pip works
pip3 --version

# Verify system is ready
python3 check_system.py

# Run the scraper (automatic setup)
bash run_scraper.sh

# Run with debug info
python3 furth_scraper_advanced.py --debug

# Run with visible browser
python3 furth_scraper_advanced.py --show

# View the results
open furth_companies.csv          # Mac
cat furth_companies.csv | head -20  # Linux/Mac terminal

# Count companies
wc -l furth_companies.csv
```

---

## 🎉 Success!

You're all set! The scraper is ready to use. 

**Next step:** Run `bash run_scraper.sh` and watch the magic happen! ✨

---

**Still confused?** Check `QUICKSTART.md` for command examples or `INSTALLATION.md` for detailed help.

Good luck! 🚀
