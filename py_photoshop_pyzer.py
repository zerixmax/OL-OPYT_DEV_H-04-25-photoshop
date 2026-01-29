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
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont

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

        # Varijable za Undo/Redo
        self.history = []
        self.redo_stack = []
        self.max_history = 10

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
        """Kreira sve GUI elemente aplikacije (Sidebar Layout)."""
        
        # --- CONFIG GRID ---
        self.grid_columnconfigure(0, weight=0) # Sidebar (fiksno)
        self.grid_columnconfigure(1, weight=1) # Main (expand)
        self.grid_rowconfigure(0, weight=1)
        
        # === 1. SIDEBAR (Lijevo) ===
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1) # Spacer gura footer dolje

        # Logo / Header
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="PyZ3R LAB", font=("Roboto", 24, "bold"), text_color="#3B8ED0")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Navigacijski gumbi
        self.nav_buttons = {}
        section_names = ["Glavno", "Edit", "Efekti", "Export", "Batch"]
        
        for i, name in enumerate(section_names):
            btn = ctk.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, 
                                text=name, fg_color="transparent", text_color=("gray10", "gray90"), 
                                hover_color=("gray70", "gray30"), anchor="w", 
                                command=lambda n=name: self.select_frame(n))
            btn.grid(row=i+1, column=0, sticky="ew")
            self.nav_buttons[name] = btn
            
        # UI Scaling Option
        self.lbl_scaling = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.lbl_scaling.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(2, 10))
        self.scaling_optionemenu.set("100%")

        # Footer u Sidebar-u
        self.lbl_appearence = ctk.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.lbl_appearence.grid(row=12, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=13, column=0, padx=20, pady=(2, 10), sticky="s")
        self.appearance_mode_menu.set("Dark")
        
        # ASCII ART Footer
        self.lbl_ascii_footer = ctk.CTkLabel(self.sidebar_frame, text=self.ascii_signature_text,
                                             font=("Courier", 6), text_color="#2CC985", justify="left")
        self.lbl_ascii_footer.grid(row=14, column=0, padx=5, pady=(0, 10))


        # === 2. MAIN AREA (Desno) ===
        self.tools_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.tools_container.grid(row=8, column=0, sticky="nsew", padx=10, pady=10)
        self.sidebar_frame.grid_rowconfigure(8, weight=1) # Tools container expand

        # Preview Frame (Desno)
        self.frm_preview = ctk.CTkFrame(self, fg_color="transparent")
        self.frm_preview.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.lbl_image = ctk.CTkLabel(self.frm_preview, text="Dobrodošli u PyZ3R Lab v2.0", font=("Roboto", 24))
        self.lbl_image.pack(expand=True, fill="both")
        
        self.progress_bar = ctk.CTkProgressBar(self.frm_preview, mode="indeterminate", width=400)

        # Inicijalizacija Frameova za alate
        self.frames = {}
        for name in section_names:
            frame = ctk.CTkScrollableFrame(self.tools_container, fg_color="transparent") 
            self.frames[name] = frame
            
        # Pozivi setup funkcija
        self._setup_frame_main(self.frames["Glavno"])
        self._setup_frame_edit(self.frames["Edit"])
        self._setup_frame_effects(self.frames["Efekti"])
        self._setup_frame_export(self.frames["Export"])
        self._setup_frame_batch(self.frames["Batch"])

        # Odaberi prvi
        self.select_frame("Glavno")

    def select_frame(self, name):
        for btn in self.nav_buttons.values():
            btn.configure(fg_color="transparent")
        self.nav_buttons[name].configure(fg_color=("gray75", "gray25"))
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    # --- IMPLEMENTACIJA NOVIH METODA ZA FRAMEOVE ---
    def _setup_frame_main(self, parent):
        undo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        undo_frame.pack(fill="x", pady=(0, 10))
        self.btn_undo = ctk.CTkButton(undo_frame, text="⟲", width=50, command=self.undo, state="disabled", fg_color="gray")
        self.btn_undo.pack(side="left", padx=2, expand=True)
        self.btn_redo = ctk.CTkButton(undo_frame, text="⟳", width=50, command=self.redo, state="disabled", fg_color="gray")
        self.btn_redo.pack(side="right", padx=2, expand=True)
        
        ctk.CTkButton(parent, text="📂 Otvori", command=self.open_file).pack(pady=5, fill="x")
        ctk.CTkButton(parent, text="💾 Spremi", command=self.save_file, fg_color="green").pack(pady=5, fill="x")
        ctk.CTkButton(parent, text="↺ Reset", command=self.reset_image, fg_color="#C0392B").pack(pady=5, fill="x")
        
        ctk.CTkLabel(parent, text="--- INFO ---", font=("Roboto", 10)).pack(pady=10)
        self.lbl_info = ctk.CTkLabel(parent, text="", justify="left", font=("Consolas", 10), wraplength=200)
        self.lbl_info.pack(anchor="w")

    def _setup_frame_edit(self, parent):
        ctk.CTkLabel(parent, text="Rotacija", font=("Roboto", 14, "bold")).pack(pady=(10, 5))
        rot_frame = ctk.CTkFrame(parent, fg_color="transparent")
        rot_frame.pack(fill="x")
        ctk.CTkButton(rot_frame, text="⟲", width=60, command=lambda: self.rotate("left")).pack(side="left", padx=2, expand=True)
        ctk.CTkButton(rot_frame, text="⟳", width=60, command=lambda: self.rotate("right")).pack(side="right", padx=2, expand=True)
        ctk.CTkButton(parent, text="↔ Zrcali", command=self.flip_horizontal).pack(fill="x", pady=10)

    def _setup_frame_effects(self, parent):
        ctk.CTkLabel(parent, text="Filteri", font=("Roboto", 14, "bold")).pack(pady=(10, 5))
        self.filter_var = ctk.StringVar(value="Bez Filtera")
        ctk.CTkOptionMenu(parent, values=["Bez Filtera", "Crno-Bijelo", "Zamućenje (Blur)", "Konture", "Reljef (Emboss)", "Izoštravanje"],
                          variable=self.filter_var, command=self.apply_filter).pack(fill="x", pady=5)
        
        ctk.CTkLabel(parent, text="Svjetlina", font=("Roboto", 12)).pack(pady=(15, 0))
        self.slider_bright = ctk.CTkSlider(parent, from_=0.1, to=2.0, command=self.update_enhancements)
        self.slider_bright.set(1.0)
        self.slider_bright.pack(fill="x", pady=5)
        
        ctk.CTkLabel(parent, text="Kontrast", font=("Roboto", 12)).pack(pady=(10, 0))
        self.slider_contrast = ctk.CTkSlider(parent, from_=0.1, to=2.0, command=self.update_enhancements)
        self.slider_contrast.set(1.0)
        self.slider_contrast.pack(fill="x", pady=5)
        
        # Watermark
        ctk.CTkLabel(parent, text="Branding", font=("Roboto", 12)).pack(pady=(15, 0))
        ctk.CTkButton(parent, text="💧 Dodaj Vodeni Žig", command=self.add_watermark, fg_color="#2980B9").pack(fill="x", pady=5)

    def _setup_frame_export(self, parent):
        ctk.CTkLabel(parent, text="WebP Export", font=("Roboto", 14, "bold")).pack(pady=(10, 5))
        self.slider_quality = ctk.CTkSlider(parent, from_=1, to=100, number_of_steps=100)
        self.slider_quality.set(80)
        self.slider_quality.pack(fill="x", pady=5)
        self.lbl_quality_val = ctk.CTkLabel(parent, text="Kvaliteta: 80")
        self.lbl_quality_val.pack()
        self.slider_quality.configure(command=lambda val: self.lbl_quality_val.configure(text=f"Kvaliteta: {int(val)}"))
        
        ctk.CTkButton(parent, text="Konvertiraj", command=self.save_as_webp, fg_color="#D35400").pack(fill="x", pady=10)
        self.lbl_savings = ctk.CTkLabel(parent, text="", text_color="gray", wraplength=200)
        self.lbl_savings.pack(pady=5)
        
    def save_as_webp(self):
        if not self.processed_image:
            messagebox.showwarning("Upozorenje", "Nema slike za optimizaciju!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".webp",filetypes=[("WebP Image", "*.webp")])
        if file_path:
            try:
                quality_val = int(self.slider_quality.get())
                self.processed_image.save(file_path, "WEBP", quality=quality_val)
                original_size = os.path.getsize(self.file_path) if self.file_path and os.path.exists(self.file_path) else 0
                new_size = os.path.getsize(file_path)
                msg = f"Spremljeno! Size: {new_size/1024:.1f} KB"
                self.lbl_savings.configure(text=msg, text_color="#2CC985")
            except Exception as e:
                messagebox.showerror("Greška", str(e))

    def _setup_frame_batch(self, parent):
        ctk.CTkLabel(parent, text="Batch", font=("Roboto", 14, "bold")).pack(pady=(10, 5))
        self.batch_input_path = ctk.StringVar()
        ctk.CTkButton(parent, text="Odaberi Mapu", command=self.select_batch_input).pack(fill="x", pady=5)
        ctk.CTkEntry(parent, textvariable=self.batch_input_path, placeholder_text="Putanja...").pack(fill="x", pady=5)
        
        self.batch_resize_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(parent, text="Resize (2000px)", variable=self.batch_resize_var).pack(pady=10, anchor="w")
        self.batch_format_var = ctk.StringVar(value="WebP")
        ctk.CTkOptionMenu(parent, values=["WebP", "JPEG", "PNG"], variable=self.batch_format_var).pack(fill="x", pady=5)
        
        ctk.CTkButton(parent, text="Pokreni", command=self.run_batch_processing, fg_color="#E74C3C").pack(fill="x", pady=15)
        self.batch_progress = ctk.CTkProgressBar(parent)
        self.batch_progress.set(0)
        self.batch_progress.pack(fill="x", pady=5)
        self.lbl_batch_status = ctk.CTkLabel(parent, text="", wraplength=200)
        self.lbl_batch_status.pack()


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
            filename = os.path.basename(self.file_path)
            # Prikazujemo i veličinu datoteke u MB
            if os.path.exists(self.file_path):
                size_mb = os.path.getsize(self.file_path) / (1024 * 1024)
                size_txt = f"{size_mb:.2f} MB"
            else:
                size_txt = "N/A"
            self.lbl_info.configure(text=f"Datoteka: {filename}\nRezolucija: {self.processed_image.size}\nVeličina: {size_txt}")

    def reset_controls(self):
        """Resetira slidere i filtere na početne vrijednosti."""
        self.slider_bright.set(1.0)
        self.slider_contrast.set(1.0)
        self.filter_var.set("Bez Filtera")
        if hasattr(self, 'lbl_savings'):
             self.lbl_savings.configure(text="Rezultat: N/A", text_color="gray")

    # CLEANUP: Uklonjena stara definicija _setup_tab_export i _setup_tab_batch ako postoje dolje
    # U prethodnom koraku smo već definirali _setup_frame_export i _setup_frame_batch.
    # Provjeravamo da nema duplikata.
    
    # Dodajemo metodu za update Undo/Redo koja je obrisana greškom
    def _update_undo_redo_buttons(self):
        """Omogućuje/onemogućuje Undo/Redo gumbe ovisno o stanju stacka."""
        if hasattr(self, 'btn_undo'):
            state_undo = "normal" if self.history else "disabled"
            self.btn_undo.configure(state=state_undo)
            
        if hasattr(self, 'btn_redo'):
            state_redo = "normal" if self.redo_stack else "disabled"
            self.btn_redo.configure(state=state_redo)


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

    # --- UNDO / REDO LOGIKA ---
    
    def save_state(self):
        """Spremi trenutnu sliku u povijest PRIJE promjene."""
        if self.processed_image:
            self.history.append(self.processed_image.copy())
            if len(self.history) > self.max_history:
                self.history.pop(0) 
            self.redo_stack.clear() 
            self._update_undo_redo_buttons()

    def undo(self):
        if self.history:
            self.redo_stack.append(self.processed_image.copy())
            self.processed_image = self.history.pop()
            self._update_display()
            self._update_info()
            self._update_undo_redo_buttons()
    
    def redo(self):
        if self.redo_stack:
            self.history.append(self.processed_image.copy())
            self.processed_image = self.redo_stack.pop()
            self._update_display()
            self._update_info()
            self._update_undo_redo_buttons()

    def rotate(self, direction):
        if self.processed_image:
            self.save_state()
            angle = 90 if direction == "left" else -90
            self.processed_image = self.processed_image.rotate(angle, expand=True)
            self._update_display()
            self._update_info()

    def flip_horizontal(self):
        if self.processed_image:
            self.save_state()
            self.processed_image = ImageOps.mirror(self.processed_image)
            self._update_display()

    def apply_filter(self, choice):
        if not self.processed_image:
            return
        # Filteri
        self.save_state()
        img = self.processed_image.copy()
        
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
        self._update_display()

    def update_enhancements(self, _):
        if not self.processed_image:
            return
        
        enhancer = ImageEnhance.Brightness(self.processed_image)
        img = enhancer.enhance(self.slider_bright.get())
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(self.slider_contrast.get())
        
        display_w = self.frm_preview.winfo_width() if self.frm_preview.winfo_width() > 100 else 800
        if img.height > 0:
            target_h = int(display_w / (img.width / img.height))
            self.current_image = ctk.CTkImage(img, size=(display_w, target_h))
            self.lbl_image.configure(image=self.current_image)

    # --- BATCH CALLBACKS ---

    def add_watermark(self):
        if not self.processed_image: return

        # Kreiramo objekt za crtanje
        img_copy = self.processed_image.copy()
        draw = ImageDraw.Draw(img_copy)
        
        # Tekst i pozicija (dolje desno)
        text = "PyZ3R Edition"
        
        # Pokušaj naći neki font, inače koristi default
        try:
            # Za Windows često radi arial.ttf
            font = ImageFont.truetype("arial.ttf", 36) 
        except:
            font = ImageFont.load_default()

        # Izračunaj poziciju
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = img_copy.width - text_width - 20
        y = img_copy.height - text_height - 20
        
        # Crtanje teksta (s crnim obrubom za čitljivost)
        draw.text((x+2, y+2), text, font=font, fill="black") # Sjena
        draw.text((x, y), text, font=font, fill="#2CC985")   # Zeleni tekst
        
        self.save_state() # Spremi stanje prije izmjene (da radi Undo)
        self.processed_image = img_copy
        self._update_display()
        print("[INFO] Dodan vodeni žig.")

    def select_batch_input(self):
        path = filedialog.askdirectory()
        if path:
            self.batch_input_path.set(path)

    def run_batch_processing(self):
        input_dir = self.batch_input_path.get()
        if not input_dir or not os.path.exists(input_dir):
            messagebox.showwarning("Greška", "Odaberi valjanu izvornu mapu!")
            return
        threading.Thread(target=self._batch_worker, args=(input_dir,), daemon=True).start()

    def _batch_worker(self, input_dir):
        output_dir = os.path.join(input_dir, "Processed")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        target_format = self.batch_format_var.get()
        resize = self.batch_resize_var.get()
        
        supported = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
        files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported)]
        total = len(files)
        
        if total == 0:
            self.lbl_batch_status.configure(text="Nema slika u mapi!")
            return
            
        processed_count = 0
        total_saved_bytes = 0
        self.lbl_batch_status.configure(text=f"Obrađujem {total} slika...")
        
        try:
            for idx, filename in enumerate(files):
                img_path = os.path.join(input_dir, filename)
                img = Image.open(img_path)
                
                if resize:
                    MAX = 2000
                    if img.width > MAX or img.height > MAX:
                        img.thumbnail((MAX, MAX), Image.Resampling.LANCZOS)
                
                new_filename = os.path.splitext(filename)[0]
                save_kwargs = {}
                ext = ".png" # default
                
                if target_format == "WebP":
                    ext = ".webp"
                    save_kwargs = {"quality": 80, "method": 6}
                elif target_format == "JPEG":
                    ext = ".jpg"
                    img = img.convert("RGB")
                    save_kwargs = {"quality": 85}
                else:
                    ext = ".png"
                    save_kwargs = {"optimize": True}
                
                out_path = os.path.join(output_dir, new_filename + ext)
                img.save(out_path, **save_kwargs)
                
                orig_size = os.path.getsize(img_path)
                new_size = os.path.getsize(out_path)
                total_saved_bytes += (orig_size - new_size)
                
                processed_count += 1
                progress = processed_count / total
                self.batch_progress.set(progress)
                self.lbl_batch_status.configure(text=f"Obrađeno: {processed_count}/{total}")
                
            saved_mb = total_saved_bytes / (1024 * 1024)
            msg = f"Gotovo! Obrađeno {total} slika.\nUšteda prostora: {saved_mb:.2f} MB"
            self.lbl_batch_status.configure(text=msg, text_color="#2CC985")
            messagebox.showinfo("Batch Gotov", msg)
            
        except Exception as e:
            self.lbl_batch_status.configure(text=f"Greška: {str(e)}", text_color="red")
            print(f"Batch Error: {e}")


if __name__ == "__main__":
    app = PhotoshopApp()
    app.mainloop()
