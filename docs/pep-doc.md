# PEP 8 Implementacija i Standardi Kodiranja

Ovaj dokument opisuje kako primijenjeni stil kodiranja u projektu **PyZ3R Photoshop** slijedi [PEP 8](https://peps.python.org/pep-0008/) – službeni vodič za stil Python koda.

## 1. Organizacija Importa
Importi su grupirani u tri odjeljka, odvojena praznim redom, prema sljedećem redoslijedu:

1.  **Standardne biblioteke** (`os`, `sys`, `threading`, `time`, `tkinter`)
2.  **Third-party biblioteke** (`customtkinter`, `PIL`)
3.  **Lokalni moduli** (nema ih u ovom single-file projektu, ali bi išli ovdje)

Primjer iz koda:
```python
import os
import sys
import threading

import customtkinter as ctk
from PIL import Image
```

## 2. Docstringovi (Dokumentacija)
Svi moduli, klase i funkcije dokumentirani su koristeći **docstringove** (trostruke navodnike `"""`).
- **Modul**: Na samom vrhu datoteke nalazi se opis svrhe modula.
- **Klasa**: Klasa `PhotoshopApp` ima opis svoje odgovornosti.
- **Metode**: Svaka metoda (npr. `load_image_async`) ima kratak opis što radi.

## 3. Prazan Prostor (Whitespace)
- **Klase**: Definirane su s dva prazna reda prije početka.
- **Metode**: Unutar klase odvojene su jednim praznim redom.
- **Komentari**: Inline komentari odvojeni su s najmanje dva razmaka od koda.

## 4. Imenovanje Varijabli
Poštuje se `snake_case` za funkcije i varijable, te `PascalCase` za klase:
- ✅ `load_image_async` (funkcija)
- ✅ `file_path` (varijabla)
- ✅ `PhotoshopApp` (klasa)
- ✅ `MAX_WIDTH` (konstanta inside logic)

## 5. Duljina Linija
Kod je strukturiran da ne prelazi preveliku širinu, a dugački importi ili logički uvjeti su prelomljeni radi čitljivosti.

---
*Ovaj projekt strogo slijedi navedene smjernice kako bi osigurao čitljivost, održivost i profesionalnost koda.*
