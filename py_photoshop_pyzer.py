"""
Glavni modul za PyZ3R Photoshop Aplikaciju.

Ovaj modul implementira grafičko sučelje (GUI) koristeći CustomTkinter,
te logiku za obradu slika koristeći Pillow (PIL).
Podržava asinkrono učitavanje slika kako bi se osigurala responzivnost sučelja.
"""

import os
import sys
import threading
import time
from tkinter import filedialog, messagebox

# Third-party imports
import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter

# --- FIX: Windows Tcl/Tk Environment ---
# Automatski postavlja putanje do Tcl/Tk biblioteka na Windowsima kako bi se izbjegao "TclError"
if sys.platform == "win32":
    import os.path
    
    # 1. Pokušaj dinamicke detekcije
    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    possible_tcl_paths = [
        os.path.join(base_prefix, "tcl", "tcl8.6"),
        os.path.join(os.path.dirname(os.path.dirname(base_prefix)), "tcl", "tcl8.6"),  # Fallback
        # 2. Hardcoded fallback za korisnika z3r1x (jer base_prefix zeza)
        r"C:\Users\z3r1x\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
    ]
    
    tcl_path = None
    for p in possible_tcl_paths:
        if os.path.exists(p):
            tcl_path = p
            break
            
    if tcl_path:
        tk_path = tcl_path.replace("tcl8.6", "tk8.6")
        if "TCL_LIBRARY" not in os.environ:
            os.environ["TCL_LIBRARY"] = tcl_path
        if "TK_LIBRARY" not in os.environ and os.path.exists(tk_path):
            os.environ["TK_LIBRARY"] = tk_path
    else:
        print("UPOZORENJE: Nisam uspio pronaci Tcl/Tk biblioteke!")
# ---------------------------------------

# Optional third-party imports (Handling ImportError)
try:
    from pyfiglet import figlet_format
    from colorama import Fore, Style, init
except ImportError:
    print("Nedostaju biblioteke! Instaliraj: pip install pyfiglet colorama")
    sys.exit()


# --- KONFIGURACIJA DIZAJNA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class PhotoshopApp(ctk.CTk):
    """
    Glavna klasa aplikacije koja nasljeđuje od ctk.CTk.
    Upravlja GUI-jem, učitavanjem slika i obradom.
    """

    def __init__(self):
        super().__init__()

        # Brending - Generiranje ASCII arta
        self.ascii_signature_text = figlet_format("PyZ3R", font="slant")
        self.print_startup_signature()

        # Konfiguracija prozora
        self.title("Algebra Python Photoshop - PyZ3R Edition 2026")
        self.geometry("1200x850")
        
        # Grid layout (Lijevo slika, Desno alati)
        self.grid_columnconfigure(0, weight=4) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        # Varijable stanja
        self.file_path = None
        self.original_image = None
        self.processed_image = None
        
        # Varijable za Async Loading
        self._temp_loaded_image = None  # Ovdje dretva ostavlja rezultat
        self._loading_error = None      # Ovdje dretva ostavlja grešku
        self.current_image = None       # Referenca na CTkImage da ga GC ne pojede
        
        # Učitaj ikone (PRIJE kreiranja UI-a!)
        self._load_icons()

        self._create_ui()

        # Učitaj defaultnu sliku ako postoji
        default_img = './images/IMG_0630.JPG'
        if os.path.exists(default_img):
            self.load_image_async(default_img)

    def print_startup_signature(self):
        """Ispisuje PyZ3R ASCII art u zelenoj boji u konzolu."""
        try:
            init(autoreset=True)
            GREEN = Fore.GREEN
            RESET = Style.RESET_ALL
            print("="*60)
            print(GREEN + self.ascii_signature_text + RESET)
            print(f"{GREEN}Created by: PyZ3R @ Algebra 2026{RESET}")
            print("="*60)
        except:
            pass

    def _load_icons(self):
        """Učitava ikone iz images/icons foldera."""
        self.icons = {}
        icon_names = ["folder_open", "save", "refresh", "rotate_left", "rotate_right", "swap_horiz"]
        
        for name in icon_names:
            try:
                # Putanje do ikona (black = za light mode, white = za dark mode)
                path_black = f"./images/icons/{name}_black.png"
                path_white = f"./images/icons/{name}_white.png"
                
                if os.path.exists(path_black) and os.path.exists(path_white):
                    self.icons[name] = ctk.CTkImage(
                        light_image=Image.open(path_black),
                        dark_image=Image.open(path_white),
                        size=(20, 20)
                    )
                else:
                    print(f"Warning: Icon {name} not found at {path_black}")
            except Exception as e:
                print(f"Error loading icon {name}: {e}")

    def _create_ui(self):
        """Kreira sve GUI elemente aplikacije."""
        # === LIJEVI PANEL (Okvir za sliku) ===
        self.frm_preview = ctk.CTkFrame(self, fg_color="transparent")
        self.frm_preview.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        self.lbl_image = ctk.CTkLabel(self.frm_preview, text="Povuci sliku ili klikni 'Otvori'...", font=("Roboto", 20))
        self.lbl_image.pack(expand=True, fill="both")

        # PROGRESS BAR (Inicijalno skriven) - Za async loading
        self.progress_bar = ctk.CTkProgressBar(self.frm_preview, mode="indeterminate", width=400)
        
        # === DESNI PANEL (Alati) ===
        self.frm_tools = ctk.CTkFrame(self, width=300, corner_radius=15)
        self.frm_tools.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        
        # Naslov Alata
        ctk.CTkLabel(self.frm_tools, text="Photo Editor", font=("Roboto", 24, "bold"), text_color="#3B8ED0").pack(pady=(20, 10))

        # TABS (Kartice)
        self.tabs = ctk.CTkTabview(self.frm_tools)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=10)
        self.tabs.add("Glavno")
        self.tabs.add("Edit")
        self.tabs.add("Efekti")

        self._setup_tab_main()
        self._setup_tab_edit()
        self._setup_tab_effects()

        # Footer
        ctk.CTkLabel(self.frm_tools, text="Dev: PyZ3R © 2026", font=("Roboto", 9), text_color="gray").pack(side="bottom", pady=(0, 15))
        
        # ASCII ART U GUI-u (Monospaced font)
        self.lbl_ascii_footer = ctk.CTkLabel(self.frm_tools, 
                                             text=self.ascii_signature_text,
                                             font=("Courier", 8, "bold"),
                                             text_color="#2CC985",
                                             justify="center")
        self.lbl_ascii_footer.pack(side="bottom", pady=(10, 0))

    def _setup_tab_main(self):
        """Postavlja elemente na tabu 'Glavno'."""
        tab = self.tabs.tab("Glavno")
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)

        # Dohvati ikone sigurno (get vraca None ako nema kljuca, ali CTkButton handlea image=None ok, samo nema slike)
        icon_open = self.icons.get("folder_open")
        icon_save = self.icons.get("save")
        icon_reset = self.icons.get("refresh")

        ctk.CTkButton(btn_frame, text="Otvori", image=icon_open, command=self.open_file, height=40).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(btn_frame, text="Spremi", image=icon_save, command=self.save_file, fg_color="green", height=40).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(btn_frame, text="Reset", image=icon_reset, command=self.reset_image, fg_color="#C0392B", height=40).pack(side="left", padx=5, expand=True, fill="x")
        

        # Separator (kao <hr>)
        ctk.CTkFrame(tab, height=2, fg_color=("gray70", "gray30")).pack(fill="x", padx=10, pady=20)
        
        self.switch_mode = ctk.CTkSwitch(tab, text="Dark Mode", command=self.toggle_mode)
        self.switch_mode.select()
        self.switch_mode.pack(pady=10)
        
        # Info labela - Centrirana i podebljana
        self.lbl_info = ctk.CTkLabel(tab, text="", justify="center", font=("Roboto", 13, "bold"))
        self.lbl_info.pack(pady=10)

    def _setup_tab_edit(self):
        """Postavlja elemente na tabu 'Edit'."""
        tab = self.tabs.tab("Edit")
        ctk.CTkLabel(tab, text="Rotacija", font=("Roboto", 14, "bold")).pack(pady=(15, 5))
        
        rot_frame = ctk.CTkFrame(tab, fg_color="transparent")
        rot_frame.pack(fill="x")
        
        icon_left = self.icons.get("rotate_left")
        icon_right = self.icons.get("rotate_right")
        icon_flip = self.icons.get("swap_horiz")

        ctk.CTkButton(rot_frame, text="Lijevo", image=icon_left, width=80, command=lambda: self.rotate("left")).pack(side="left", padx=5, expand=True)
        ctk.CTkButton(rot_frame, text="Desno", image=icon_right, width=80, command=lambda: self.rotate("right")).pack(side="right", padx=5, expand=True)

        ctk.CTkLabel(tab, text="Zrcaljenje", font=("Roboto", 14, "bold")).pack(pady=(20, 5))
        ctk.CTkButton(tab, text="Zrcali Vodoravno", image=icon_flip, command=self.flip_horizontal).pack(fill="x")

    def _setup_tab_effects(self):
        """Postavlja elemente na tabu 'Efekti'."""
        tab = self.tabs.tab("Efekti")
        
        ctk.CTkLabel(tab, text="Odaberi Filter:", font=("Roboto", 14)).pack(pady=(10, 5))
        self.filter_var = ctk.StringVar(value="Bez Filtera")
        ctk.CTkOptionMenu(tab, 
                          values=["Bez Filtera", "Crno-Bijelo", "Zamućenje (Blur)", "Konture", "Reljef (Emboss)", "Izoštravanje"],
                          variable=self.filter_var, 
                          command=self.apply_filter).pack(fill="x", pady=5)
        
        ctk.CTkLabel(tab, text="Svjetlina (Brightness)", font=("Roboto", 12)).pack(pady=(20, 0))
        self.slider_bright = ctk.CTkSlider(tab, from_=0.1, to=2.0, command=self.update_enhancements)
        self.slider_bright.set(1.0)
        self.slider_bright.pack(fill="x", pady=5)

        ctk.CTkLabel(tab, text="Kontrast (Contrast)", font=("Roboto", 12)).pack(pady=(10, 0))
        self.slider_contrast = ctk.CTkSlider(tab, from_=0.1, to=2.0, command=self.update_enhancements)
        self.slider_contrast.set(1.0)
        self.slider_contrast.pack(fill="x", pady=5)

    # =========================================================================
    # --- ASINKRONO UČITAVANJE SLIKE (THREADING) ---
    # =========================================================================
    
    def load_image_async(self, path):
        """1. Pripremi UI i pokreni dretvu."""
        self.file_path = path
        
        # Pokaži spinner / progress bar
        self.lbl_image.configure(text="Učitavanje slike...", image="")
        self.progress_bar.pack(pady=20)
        self.progress_bar.start()
        
        # Resetiraj temp varijable
        self._temp_loaded_image = None
        self._loading_error = None
        
        # Pokreni dretvu
        # Daemon=True znači da se dretva gasi ako ugasimo program
        threading.Thread(target=self._background_loader_task, args=(path,), daemon=True).start()
        
        # Pokreni polling (provjeru)
        self._check_loading_status()

    def _background_loader_task(self, path):
        """2. (POZADINA) Težak posao: otvaranje, resize."""
        try:
            # Simulacija delaya da se vidi progress bar (maknuti po potrebi)
            # time.sleep(0.5) 
            
            Image.MAX_IMAGE_PIXELS = None 
            img = Image.open(path)
            
            # [The IF Loop] - Resize u pozadini!
            MAX_WIDTH = 2000
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                new_height = int(img.height * ratio)
                # LANCZOS je spor, zato je super da je u dretvi!
                img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                print(f"[INFO THREAD] Slika optimizirana na: {img.size}")
            
            # Spremamo rezultat u varijablu
            self._temp_loaded_image = img.convert("RGB")
            
        except Exception as e:
            self._loading_error = str(e)

    def _check_loading_status(self):
        """3. (GLAVNA DRETVA) Provjerava jel gotovo."""
        if self._temp_loaded_image:
            # Gotovo je i imamo sliku!
            self._on_loading_complete()
        elif self._loading_error:
            # Gotovo je, ali s greškom!
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            messagebox.showerror("Greška", f"Ne mogu učitati sliku: {self._loading_error}")
            self.lbl_image.configure(text="Problem kod učitavanja!")
        else:
            # Nije još gotovo, provjeri opet za 100ms
            self.after(100, self._check_loading_status)

    def _on_loading_complete(self):
        """4. (GLAVNA DRETVA) Ažuriraj sučelje sa gotovom slikom."""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()  # Sakrij progress bar
        
        # Preuzmi sliku iz temp varijable
        self.original_image = self._temp_loaded_image
        self.processed_image = self.original_image.copy()
        
        # Resetiraj kontrole i prikaži
        self.reset_controls()
        self._update_display()
        self._update_info()

    # =========================================================================

    def _update_display(self):
        """Osvježava prikaz slike na ekranu."""
        if self.processed_image:
            # Uzimamo veličinu lijevog okvira kako bi slika stala unutra
            display_w = self.frm_preview.winfo_width() 
            if display_w < 100:
                display_w = 800 
            
            aspect_ratio = self.processed_image.width / self.processed_image.height
            target_h = int(display_w / aspect_ratio)
            
            self.current_image = ctk.CTkImage(light_image=self.processed_image,
                                              dark_image=self.processed_image,
                                              size=(display_w, target_h))
            self.lbl_image.configure(image=self.current_image, text="")

    def _update_info(self):
        """Ažurira tekstualne podatke o slici."""
        if self.processed_image:
            filename = os.path.basename(self.file_path)
            self.lbl_info.configure(text=f"Datoteka: {filename}\nRezolucija: {self.processed_image.size}")

    def reset_controls(self):
        """Resetira slidere i filtere na početne vrijednosti."""
        self.slider_bright.set(1.0)
        self.slider_contrast.set(1.0)
        self.filter_var.set("Bez Filtera")

    # --- AKCIJE (Callbacks) ---

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Slike", "*.jpg;*.png;*.jpeg")])
        if path:
            self.load_image_async(path)

    def save_file(self):
        if self.processed_image:
            path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if path:
                self.processed_image.save(path)

    def reset_image(self):
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.reset_controls()
            self._update_display()

    def toggle_mode(self):
        mode = "Dark" if ctk.get_appearance_mode() == "Light" else "Light"
        ctk.set_appearance_mode(mode)

    def rotate(self, direction):
        if self.processed_image:
            angle = 90 if direction == "left" else -90
            self.processed_image = self.processed_image.rotate(angle, expand=True)
            self._update_display()
            self._update_info()

    def flip_horizontal(self):
        if self.processed_image:
            self.processed_image = ImageOps.mirror(self.processed_image)
            self._update_display()

    def apply_filter(self, choice):
        if not self.original_image:
            return
        
        # Uvijek krećemo od originala kad mijenjamo filter
        img = self.original_image.copy()
        
        if choice == "Crno-Bijelo":
            img = ImageOps.grayscale(img).convert("RGB")
        elif choice == "Zamućenje (Blur)":
            img = img.filter(ImageFilter.BLUR)
        elif choice == "Konture":
            img = img.filter(ImageFilter.CONTOUR)
        elif choice == "Reljef (Emboss)":
            img = img.filter(ImageFilter.EMBOSS)
        elif choice == "Izoštravanje":
            img = img.filter(ImageFilter.SHARPEN)
        
        self.processed_image = img
        self.update_enhancements(None)

    def update_enhancements(self, _):
        """Primjenjuje promjene svjetline i kontrasta na trenutnu sliku."""
        if not self.processed_image:
            return
        
        enhancer = ImageEnhance.Brightness(self.processed_image)
        img = enhancer.enhance(self.slider_bright.get())
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(self.slider_contrast.get())
        
        # Prikaz (display)
        display_w = self.frm_preview.winfo_width() if self.frm_preview.winfo_width() > 100 else 800
        # Izracunaj novi height na brzinu
        target_h = int(display_w / (img.width / img.height))
        
        self.current_image = ctk.CTkImage(img, size=(display_w, target_h))
        self.lbl_image.configure(image=self.current_image)


if __name__ == "__main__":
    app = PhotoshopApp()
    app.mainloop()
