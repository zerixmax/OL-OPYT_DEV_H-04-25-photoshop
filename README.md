# 🎨 Algebra Python Photoshop - PyZ3R Edition 2026

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Edition](https://img.shields.io/badge/Edition-PyZ3R%202026-00ff00)
![Status](https://img.shields.io/badge/Status-Exam%20Ready-success)

Napredna desktop aplikacija za obradu fotografija razvijena u sklopu **Algebra Python Developer** programa.

Ova verzija (**PyZ3R Edition**) predstavlja potpunu modernizaciju originalne skripte, prebacujući je u **Objektno Orijentirani (OOP)** kod s modernim **CustomTkinter** sučeljem.

## ✨ Ključne Značajke

### 1. Moderno UI Sučelje (CustomTkinter)
* **Dark/Light Mode:** Ugrađena podrška za teme (default: Dark Blue).
* **Tabovi (Tabview):** Alati su organizirani u logičke cjeline ("Datoteka", "Uređivanje", "Efekti") radi preglednosti.
* **Responzivnost:** Sučelje se prilagođava veličini prozora.

### 2. Napredna Obrada Slika (Pillow)
* **Rotacija:** Mogućnost rotiranja slike za 90° u oba smjera.
* **Zrcaljenje:** Horizontalni flip.
* **Filteri:** Implementirani Pillow filteri: *Blur, Contour, Emboss, Sharpen, Black & White*.
* **Live Enhancements:** Klizači (Sliders) za podešavanje svjetline (Brightness) i kontrasta u stvarnom vremenu.

### 3. 🧠 Pametna Logika (Exam Task: "The IF Loop")
Implementirana je ključna logika za optimizaciju učitavanja slika koja je bila naglašena na predavanjima:
* Aplikacija provjerava širinu slike pri učitavanju.
* **IF uvjet:** `if img.width > 2000:` -> Slika se automatski smanjuje (resize) uz zadržavanje omjera (aspect ratio) koristeći `LANCZOS` filter za kvalitetu.
* **ELSE:** Ako je slika manja, ostaje u originalnoj rezoluciji.

### 4. Custom Branding (PyZ3R)
* Integriran **ASCII Art potpis** pri pokretanju aplikacije.
* Koristi biblioteke `pyfiglet` i `colorama` za ispis logotipa **"PyZ3R"** u zelenoj boji u konzoli.

```text
   ___      _____ _____ ___ 
  / _ \_   |__  /|___ /| _ \
 / /_)/ | | |/ /   |_ \|   /
/ ___/| |_| / /___ ___) |_\ \
\/     \__, /____/|____/|_\_\
       |___/                 
```

## 🛠️ Instalacija i Pokretanje

Projekt zahtijeva Python 3.10+ i nekoliko vanjskih biblioteka.

### 1. Kloniranje i Priprema
```bash
git clone https://github.com/tvoj-username/pyzer-photoshop.git
cd pyzer-photoshop
python -m venv venv
```

### 2. Aktivacija Virtualnog Okruženja
* **Windows:** `.\venv\Scripts\activate`
* **Mac/Linux:** `source venv/bin/activate`

### 3. Instalacija Paketa
```bash
pip install customtkinter Pillow pyfiglet colorama
```

### 4. Pokretanje Aplikacije
```bash
python py_photoshop_pyzer.py
```

## 📂 Struktura Koda
* `py_photoshop_pyzer.py` - Glavna izvršna datoteka (sadrži App klasu).
* `images/` - Mapa za testne slike.
* `README.md` - Dokumentacija projekta.

## 👨💻 Autor
Created by PyZ3R @ Algebra 2026. Based on concepts from Algebra Python Developer modules.
