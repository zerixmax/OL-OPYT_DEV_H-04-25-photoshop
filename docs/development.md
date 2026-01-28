# Development Documentation

Ovaj direktorij sadrži dokumentaciju o razvoju aplikacije.

## Status Implementacije (v1.4)
Aplikacija je kompletirana, lokalizirana, vizualno polirana i koristi asinkrono učitavanje.

### 1. Osnovna Konfiguracija
- **GUI Framework**: `customtkinter`.
- **Jezik Sučelja**: Hrvatski.
- **Potpis**: ASCII Art integriran u **konzolu** (PyFiglet + Colorama) i **GUI** (Monospaced font u footeru).
- **Asinkronost**: Koristi `threading` za učitavanje slika.

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
- [ ] Batch processing (obrada više slika odjednom)
- [ ] Undo/Redo funkcionalnost
- [ ] Dodavanje ikona za alate.
- [ ] Poboljšanje rasporeda (Layout) za još moderniji izgled.

---

> *"Nije da se ne usuđujemo jer su stvari teške, već su stvari teške jer se ne usuđujemo."*  
> — **Seneka**

**Pozdrav ekipi s tečaja! 👋**  
Konstruktivno rješavanje problema je put do majstorstva. Sretno svima! 🚀
