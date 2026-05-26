#!/bin/bash

# Fürth Companies Web Scraper - Setup and Run Script
# This script sets up dependencies and runs the scraper

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════╗"
echo "║   Fürth Companies Web Scraper - Setup & Run            ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "✗ pip3 not found. Please install pip3."
    exit 1
fi
echo "✓ pip3 found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Install Playwright browsers
echo "Installing Playwright browsers (this may take a minute)..."
python3 -m playwright install chromium

echo "✓ Playwright browsers installed"
echo ""

# Parse arguments
SHOW_BROWSER=false
DEBUG_MODE=false

for arg in "$@"; do
    case $arg in
        --show)
            SHOW_BROWSER=true
            ;;
        --debug)
            DEBUG_MODE=true
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --show    Show browser window during scraping"
            echo "  --debug   Enable debug output"
            echo "  --help    Show this help message"
            exit 0
            ;;
    esac
done

# Build command
CMD="python3 furth_scraper_advanced.py"

if [ "$SHOW_BROWSER" = true ]; then
    CMD="$CMD --show"
fi

if [ "$DEBUG_MODE" = true ]; then
    CMD="$CMD --debug"
fi

echo "╔════════════════════════════════════════════════════════╗"
echo "║   Starting Web Scraper                                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Command: $CMD"
echo ""
echo "This will scrape all companies from:"
echo "https://service-on.fuerth.de/KWISwebComp/sections/search/company.jsf"
echo ""
echo "Expected output files:"
echo "  • furth_companies.csv"
echo "  • furth_companies.json"
echo ""
echo "Starting in 2 seconds... (Press Ctrl+C to cancel)"
sleep 2
echo ""

# Run the scraper
$CMD

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   Scraping Complete!                                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Output files:"
if [ -f "furth_companies.csv" ]; then
    lines=$(wc -l < furth_companies.csv)
    companies=$((lines - 1))
    echo "  ✓ furth_companies.csv ($companies companies)"
fi

if [ -f "furth_companies.json" ]; then
    echo "  ✓ furth_companies.json"
fi

echo ""
echo "Next steps:"
echo "  • View the CSV: open furth_companies.csv"
echo "  • View the JSON: cat furth_companies.json | less"
echo "  • Re-run scraper: bash run_scraper.sh"
echo ""
