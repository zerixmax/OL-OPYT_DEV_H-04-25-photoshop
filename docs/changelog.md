# Changelog

## [v2.0] - 2026-01-29
### Promjene
- **Napredna Navigacija (Sidebar):** Potpuni redizajn sučelja! Kartice (tabovi) su zamijenjene modernim bočnim izbornikom (Sidebar).
- **Profesionalni Layout:** Alati se sada dinamički učitavaju u bočni panel, ostavljajući više prostora za prikaz slike.
- **Optimizacija:** Kod refaktoriran za bolju modularnost (Frame-based architecture).
- **Watermark (NOVO):** Dodan gumb za automatsko dodavanje "PyZ3R Edition" potpisa na slike.
- **UI Scaling (NOVO):** Mogućnost skaliranja sučelja (80-120%) za prilagodbu različitim ekranima.
- **Standalone EXE:** Aplikacija je kompajlirana u jednu .EXE datoteku za jednostavnu distribuciju.
  > **NAPOMENA:** U ovoj verziji (v2.0) prijavljen je problem s pokretanjem .EXE datoteke. Preporučuje se pokretanje iz izvornog koda (`python py_photoshop_pyzer.py`) dok se problem ne otkloni.

## [v1.7] - 2026-01-29
### Promjene
- **Batch Processing:** Masovna obrada slika! Dodan novi tab gdje možete odabrati mapu i konvertirati SVE slike u WebP, JPG ili PNG jednim klikom. Podržava automatsko smanjivanje (resize) i računa ukupnu uštedu prostora.
- **Undo/Redo:** Dodana povijest promjena. Sada možete poništiti greške (gumb ⟲ Undo) i vratiti poništeno (gumb ⟳ Redo). Povijest pamti zadnjih 10 koraka.
- **UI:** Dodani gumbi za Undo/Redo u glavni alatni okvir.

## [v1.6] - 2026-01-29
### Promjene
- **WebP Optimizer:** Dodan novi tab "Export" sa sliderom za kontrolu kvalitete kompresije.
- **Statistika:** Aplikacija sada računa i prikazuje uštedu veličine datoteke (KB/MB) nakon konverzije u WebP.
- **Info:** Dodan prikaz veličine trenutno učitane datoteke u panelu s informacijama.

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
