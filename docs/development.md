# Development Documentation

Ovaj direktorij sadrži dokumentaciju o razvoju aplikacije.

## Status Implementacije (v2.0)
Aplikacija je kompletirana, lokalizirana, vizualno polirana i koristi asinkrono učitavanje. U verziji 2.0 uveden je potpuni redizajn sučelja s bočnim izbornikom (Sidebar).

### 1. Osnovna Konfiguracija
- **GUI Framework**: `customtkinter`.
- **Jezik Sučelja**: Hrvatski.
- **Potpis**: ASCII Art integriran u **konzolu** (PyFiglet + Colorama) i **GUI** (Monospaced font u footeru).
- **Asinkronost**: Koristi `threading` za učitavanje slika.
- **Ikone**: Koristi Material Design ikone (PNG) s podrškom za Light/Dark mode.

### 2. Funkcionalnosti
- **Učitavanje Slika**: Defaultno učitava `IMG_0630.JPG`.
- **Progress Bar**: Prikazuje vizualni indikator dok se slika učitava.
- **Automatska Promjena Veličine ("The IF Loop")**: Slike šire od 2000px se automatski smanjuju zadržavajući omjer stranica.
- **Uređivanje**:
    - Rotacija (lijevo/desno za 90°).
    - Zrcaljenje (horizontalno).
- **Efekti**:
    - Filteri: Normal, B&W, Blur, Contour, Emboss, Sharpen.
    - Podešavanje svjetline i kontrasta klizačima.
- **Spremanje**: Mogućnost spremanja obrađene slike.

## Planirani moduli (Budući razvoj)
- [x] Osnovna obrada slika (PIL)
- [x] Korisničko sučelje (GUI)
- [x] Napredni filteri
- [x] Batch processing (obrada više slika odjednom)
- [x] Undo/Redo funkcionalnost
- [x] Dodavanje ikona za alate.
- [x] Poboljšanje rasporeda (Layout) za još moderniji izgled.

### 3. Ideje za Version 2.0 (The "Pro" Update)
- [x] **Watermark (Vodeni Žig):** Automatsko dodavanje potpisa "PyZ3R Edition" na slike pomoću `ImageDraw`.
- [x] **Distribucija (.EXE):** Pakiranje aplikacije s `PyInstaller` (jedna datoteka). Ispravljeni problemi s putanjama i `customtkinter` dependencijem.
- [x] **UI Skaliranje:** Mogućnost promjene veličine sučelja (80%, 100%, 120%) za High DPI ekrane (inspirirano `complex_example.py`).
- [x] **Napredna Navigacija:** Zamjena tabova s lijevim sidebarom za profesionalniji izgled.

---

> *"Nije da se ne usuđujemo jer su stvari teške, već su stvari teške jer se ne usuđujemo."*  
> — **Seneka**

**Pozdrav ekipi s tečaja! 👋**  
Konstruktivno rješavanje problema je put do majstorstva. Sretno svima! 🚀
