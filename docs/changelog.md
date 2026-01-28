# Changelog

## [v1.5] - 2026-01-28
### Promjene
- **Ikone:** Dodana podrška za Material Design ikone (PNG) umjesto tekstualnih gumba za moderniji izgled.
- **UI Layout:** Gumbi "Otvori", "Spremi" i "Reset" su sada poravnati u jednom redu.
- **Dizajn:** Zamijenjen tekstualni separator s vizualnom linijom i poboljšan prikaz informacija o slici (centrirano, bold).
- **Bug Fix:** Riješen `AttributeError` pri pokretanju uzrokovan krivim redoslijedom učitavanja ikona.

## [v1.4] - 2026-01-28
### Promjene
- **Asinkronost:** Implementirano asinkrono učitavanje slika (`threading`) kako se sučelje ne bi smrzavalo tijekom obrade velikih datoteka.
- **UI Feedback:** Dodan `ProgressBar` koji se pojavljuje tijekom učitavanja slike.
- **Refactoring:** Kod restrukturiran za odvajanje UI logike od "heavy-lifting" operacija.

## [v1.3] - 2026-01-28
### Promjene
- **GUI Potpis:** Dodan "PyZ3R" ASCII art direktno u footer aplikacije (desni panel) koristeći `Courier New` font.
- **Stabilnost:** Riješen problem s garbage collectionom slike (`self.current_image`) i omogućen rad s velikim slikama (`PIL.Image.MAX_IMAGE_PIXELS = None`).
- **Fix:** Integrirana sva prethodna rješenja (Tcl/Tk fix, lokalizacija) u finalnu verziju.

## [v1.2] - 2026-01-28
### Promjene
- **Default Slika:** Promijenjena zadana slika pri pokretanju s `Algebra_campus.jpg` na `IMG_0630.JPG`.
- **Lokalizacija:** Kompletno sučelje (gumbi, labele, tabovi) prevedeno na hrvatski jezik.
- **Bug Fix (Critical):** Implementirano robusno rješenje za `TclError` na Windowsima (hardcoded fallback putanje).
- **Kod:** Dodani detaljni komentari na hrvatskom jeziku za lakše razumijevanje ("The IF Loop", konfiguracija).

## [v1.0] - 2026-01-28
- Inicijalna implementacija aplikacije.
- Integracija `customtkinter` i `Pillow`.
- Implementacija "PyZ3R" ASCII potpisa.
