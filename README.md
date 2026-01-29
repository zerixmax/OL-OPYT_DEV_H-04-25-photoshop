# Kako pokrenuti PyZ3R Photoshop

## Pokretanje iz izvornog koda (PREPORUČENO)

1. Kloniraj repozitorij:
```bash
git clone https://github.com/zerixmax/OL-OPYT_DEV_H-04-25-photoshop.git
cd OL-OPYT_DEV_H-04-25-photoshop
```

2. Aktiviraj virtualno okruženje:
```bash
venv\Scripts\activate
```

3. Pokreni aplikaciju:
```bash
python py_photoshop_pyzer.py
```

## Problemi s EXE verzijom

Trenutno postoji problem s Microsoft Store verzijom Pythona i PyInstaller-om koji uzrokuje `ModuleNotFoundError: No module named '_tkinter'` grešku.

**Rješenje:** Koristi izvorni kod kao što je opisano gore. Aplikacija će raditi savršeno!

## Systemski zahtjevi

- Python 3.13+
- Windows 10/11
- Instaliran Tcl/Tk (dolazi s standardnom Python instalacijom)
