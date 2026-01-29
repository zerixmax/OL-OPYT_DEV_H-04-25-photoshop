# PyInstaller Build Guide - PyZ3R Photoshop

Ovaj dokument opisuje kako kreirati standalone `.exe` datoteku od Python aplikacije.

## 🎯 Verzija

**Trenutna verzija:** v2.1 (2026-01-29)

## 📋 Preduvjeti

1. **Python 3.13+** instaliran (preferably standardna instalacija, ne Microsoft Store verzija)
2. **Virtualno okruženje aktivirano:**
   ```bash
   venv\Scripts\activate
   ```
3. **PyInstaller instaliran u venv:**
   ```bash
   pip install pyinstaller
   ```

## 🛠️ Build Proces

### Korak 1: Provjeri Kod

Osiguraj da kod ima `resource_path()` funkciju za dinamičko pronalaženje resursa:

```python
def resource_path(relative_path):
    """ Vraća apsolutnu putanju do resursa, radi i za DEV i za PyInstaller EXE """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
```

I koristi je za učitavanje slika:
```python
default_img = resource_path(os.path.join('images', 'IMG_0630.JPG'))
```

### Korak 2: Očisti Stare Buildove

```bash
Remove-Item -Recurse -Force build, dist
```

### Korak 3: Pokreni PyInstaller

**RADNA NAREDBA (testirano i potvrđeno):**

```bash
.\venv\Scripts\pyinstaller.exe --name "PyZeR_Photoshop_v2.1" --onefile --noconsole --add-data "images;images" --collect-all customtkinter --collect-all tkinter --collect-all pyfiglet --add-binary "C:\Users\z3r1x\AppData\Local\Programs\Python\Python313\DLLs\_tkinter.pyd;." py_photoshop_pyzer.py
```

### Objašnjenje Parametara:

| Parametar | Opis |
|-----------|------|
| `--name "PyZeR_Photoshop_v2.1"` | Ime finalne EXE datoteke |
| `--onefile` | Sve pakira u JEDНУ datoteku |
| `--noconsole` | Skriva crni CMD prozor (windowed app) |
| `--add-data "images;images"` | Pakira `images/` folder u EXE |
| `--collect-all customtkinter` | Uzima SVE customtkinter resurse (JSON, teme) |
| `--collect-all tkinter` | Uzima SVE Tcl/Tk data (kritično!) |
| `--collect-all pyfiglet` | Uzima sve pyfiglet fontove za ASCII art |
| `--add-binary "_tkinter.pyd;."` | Eksplicitno dodaje _tkinter C modul |

### Korak 4: Testiraj EXE

```bash
.\dist\PyZeR_Photoshop.exe
```

Ako se pokrene BEZ greške i vidiš GUI - **SUCCESS!** ✅

## 🐛 Debug Build (ako se EXE ruši)

Ako EXE ne radi, napravi debug verziju **BEZ** `--noconsole`:

```bash
.\venv\Scripts\pyinstaller.exe --name "Debug_Test" --onefile --add-data "images;images" --collect-all customtkinter --collect-all tkinter --add-binary "C:\Users\z3r1x\AppData\Local\Programs\Python\Python313\DLLs\_tkinter.pyd;." py_photoshop_pyzer.py
```

Pokreni iz CMD-a:
```bash
.\dist\Debug_Test.exe
```

I **pročitaj grešku** koja se ispiše u konzoli.

## 🚨 Česte Greške i Rješenja

### 1. `ModuleNotFoundError: No module named '_tkinter'`
**Razlog:** `_tkinter.pyd` nije uključen u build.
**Rješenje:** Dodaj `--add-binary "...\\_tkinter.pyd;."`

### 2. `FileNotFoundError: Tcl data directory not found`
**Razlog:** Tcl/Tk dependency-ji nisu pakirani.
**Rješenje:** Koristi `--collect-all tkinter`

### 3. `ModuleNotFoundError: No module named 'customtkinter'`
**Razlog:** PyInstaller ne vidi venv pakete.
**Rješenje:** Koristi `.\venv\Scripts\pyinstaller.exe` umjesto globalnog `pyinstaller`

### 4. EXE se pokrene ali puca kod učitavanja slike
**Razlog:** `resource_path()` funkcija nije implementirana.
**Rješenje:** Dodaj funkciju iz Koraka 1

### 5. `ModuleNotFoundError: No module named 'pyfiglet.fonts'`
**Razlog:** Pyfiglet fontovi nisu uključeni u build (potrebni za ASCII art).
**Rješenje:** Dodaj `--collect-all pyfiglet` u PyInstaller naredbu

## 📦 Finalni Output

Nakon uspješnog builda imaš:
- `dist/PyZeR_Photoshop.exe` (~45MB)
- Standalone - radi bez instaliranog Pythona!
- Portabilno - možeš staviti na USB i pokrenuti bilo gdje

## ⚠️ Napomena o `.gitignore`

**NIKAD** ne commitaj `build/` i `dist/` foldere na GitHub!
Tvoj `.gitignore` već sadrži:
```
build/
dist/
*.spec
```

---

**Autor:** PyZ3R @ Algebra 2026
**Verzija dokumenta:** v2.1
