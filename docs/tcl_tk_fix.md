# Dokumentacija: Windows Tcl/Tk Fix

**Datum:** 28.01.2026.
**Problem:** Aplikacija se nije mogla pokrenuti na Windows okruženju koristeći Python 3.13.
**Greška:** `_tkinter.TclError: Can't find a usable init.tcl ...`

## Opis Problema
`customtkinter` se oslanja na `tkinter`, koji zahtijeva pristup sistemskim Tcl/Tk bibliotekama. Na nekim Windows instalacijama Pythona (posebno novijim 3.13 verzijama ili virtualnim okruženjima), `tkinter` ne uspijeva automatski detektirati putanje do mapa `tcl8.6` i `tk8.6`.

## Implementirano Rješenje
U datoteku `py_photoshop_pyzer.py` dodan je kod koji se izvršava **prije** uvoza `customtkinter` biblioteke.

```python
import sys
import os

# --- FIX: Windows Tcl/Tk Environment ---
if sys.platform == "win32":
    import os.path
    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    
    # Putanje unutar Python instalacije
    tcl_path = os.path.join(base_prefix, "tcl", "tcl8.6")
    tk_path = os.path.join(base_prefix, "tcl", "tk8.6")
    
    # Ručno postavljanje varijabli okruženja ako nisu postavljene
    if os.path.exists(tcl_path) and "TCL_LIBRARY" not in os.environ:
        os.environ["TCL_LIBRARY"] = tcl_path
        
    if os.path.exists(tk_path) and "TK_LIBRARY" not in os.environ:
        os.environ["TK_LIBRARY"] = tk_path
# ---------------------------------------
```

## Rezultat
Aplikacija sada automatski pronalazi potrebne biblioteke i pokreće se bez potrebe da korisnik ručno konfigurira varijable okruženja (`TCL_LIBRARY`, `TK_LIBRARY`) u terminalu.
