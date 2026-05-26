# Fürth Unternehmensbranchen – Unternehmen & Branchen-Explorer

## Übersicht
Dieses Projekt sammelt und visualisiert über 2.000 Unternehmen und deren Branchen aus Fürth. Die Unternehmensdaten werden per Webscraping mit Python automatisiert abgerufen und in CSV sowie JSON gespeichert. Mit einem HTML-Dashboard kannst du die Firmen nach Branchen interaktiv erkunden.

## Kernfunktionen
- **Webscraping**: Python-Skripte generieren automatisch `furth_companies.csv` und `furth_companies.json` mit allen Unternehmensdaten.
- **Dashboard**: Die Datei `dashboard.html` bietet eine visuelle, interaktive Ansicht und Analyse der Unternehmen nach Branche.
- **Flexible Datenformate**: CSV für Tabellen (Excel/Google Sheets) & JSON für Programmierung und Metadaten.

## Wichtige Dateien
- `run_scraper.sh` — Startet den gesamten Scrape-Prozess automatisch und installiert alles Notwendige.
- `furth_scraper_advanced.py` — Hauptscraping-Script mit mehreren Ausführungsoptionen (Debug, sichtbarem Browser, etc.).
- `dashboard.html` — Visualisiert die gesammelten Daten interaktiv im Browser.
- `furth_companies.csv`/`.json` — Enthalten die vollständigen gesammelten Unternehmensdaten.

## Schnellstart

1. **Scraper ausführen:**
   ```bash
   bash run_scraper.sh
   # oder
   python3 furth_scraper_advanced.py
   ```

2. **Dashboard visualisieren:**
   Damit die HTML-Visualisierung (dashboard.html) alle Daten korrekt lädt, muss ein HTTP-Server gestartet werden, weil lokale Datei-URLs sonst aus Sicherheitsgründen nicht funktionieren:

   ```bash
   # Im Verzeichnis mit der dashboard.html:
   python3 -m http.server 8000
   ```
   Jetzt kannst du `http://localhost:8000/dashboard.html` im Browser öffnen und alle Unternehmen durchsuchen.

## Voraussetzungen
- Python 3.7 oder neuer
- pip (Python Package Installer)

## Weitere Hilfe & Dokumentation
- **START_HERE.md** – Ultimativer Schnellstart (mit häufigen Problemen & Lösungen)
- **INSTALLATION.md** – Detaillierte Installationsanleitung & Troubleshooting
- **QUICKSTART.md** – Kurzreferenz für Kommandos und Optionen
- **PROJECT_SUMMARY.md** – Projektübersicht

---

Viel Spaß beim Erkunden der Fürther Unternehmenslandschaft! 🚀

