from tkinter import ttk
import tkinter as tk
from pyswip import Prolog
from tkinter import messagebox

class KierunkiApp:
    def __init__(self, root, master):
        self.root = root
        self.master = master
        self.root.title("Dopasowanie kierunków studiów")
        self.master.configure(bg="#e6f0ff")
        
        # Ustawienie minimalnego rozmiaru okna
        self.root.minsize(1000, 700)
        
        # Stylizacja przycisków
        style = ttk.Style()
        style.configure('TNotebook', background="#e6f0ff")
        style.configure('TNotebook.Tab', background="#cce0ff", padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', '#4a90e2')], foreground=[('selected', 'white')])
        
        # Inicjalizacja zmiennych
        self.zainteresowania = [
            'programowanie', 'technologie', 'logiczne_myslenie', 'matematyka',
            'fizyka', 'eksperymentowanie', 'czytanie', 'pisanie', 'dyskusje',
            'medycyna', 'ekonomia', 'finanse', 'biotechnologia', 'psychologia',
            'sztuczna_inteligencja', 'robotyka', 'inżynieria', 'prawo',
            'sztuka', 'muzyka', 'języki_obce', 'socjologia', 'filozofia',
            'zarządzanie', 'marketing', 'geologia', 'architektura',
            'gry_komputerowe', 'badania', 'człowiek', 'nauka', 'innowacje',
            'zwierzęta', 'budownictwo', 'kosmos', 'analiza'
        ]

        self.przedmioty = [
            'matematyka', 'fizyka', 'chemia', 'biologia', 'filozofia', 'historia',
            'geografia', 'informatyka', 'psychologia', 'ekonomia', 'prawo',
            'sztuka', 'języki_obce', 'zarządzanie', 'statystyka', 'logika',
            'elektronika', 'mechanika', 'anatomia', 'socjologia', 'angielski',
            'wos', 'polski'
        ]

        self.cechy = [
            'logiczne_myslenie', 'kreatywność', 'dokładność', 'ciekawość',
            'krytyczne_myslenie', 'analiza_danych', 'analityczne_myslenie',
            'komunikatywność', 'cierpliwość', 'odpowiedzialność', 'wytrwałość',
            'zdolności_organizacyjne', 'umiejętność_pracy_w_zespole',
            'samodzielność', 'adaptacyjność', 'empatia', 'otwartość_na_nowe',
            'systematyczność', 'abstrakcyjne_myslenie', 'przestrzenne_myslenie',
            'obserwacja', 'odporność_na_stres', 'elokwencja', 'przedsiębiorczość'
        ]

        self.style = [
            'praktyka', 'samodzielna_nauka', 'analiza_teoretyczna', 'projekty',
            'laboratoria', 'czytanie', 'rozmowy', 'praca_w_zespole', 'seminaria',
            'warsztaty', 'prezentacje', 'eksperymenty', 'programowanie',
            'rozwiązywanie_problemów', 'dyskusje_debaty', 'teoria',
            'case_studies', 'pamięciowa', 'symulacje', 'obliczenia', 'debata',
            'analiza'
        ]

        self.check_vars = {}
        
        # Utwórz system kart
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Stwórz ramki dla każdej kategorii
        style.configure('Bold.TFrame', background="#f0f6ff", borderwidth=2, relief="solid")

        self.zainteresowania_frame = ttk.Frame(self.notebook, style='Bold.TFrame')
        self.przedmioty_frame = ttk.Frame(self.notebook, style='Bold.TFrame')
        self.cechy_frame = ttk.Frame(self.notebook, style='Bold.TFrame')
        self.style_frame = ttk.Frame(self.notebook, style='Bold.TFrame')
        self.podsumowanie_frame = ttk.Frame(self.notebook, style='Bold.TFrame')
        self.wyniki_frame = ttk.Frame(self.notebook, style='Bold.TFrame')
        
        # Dodaj karty do notebooka

        self.notebook.add(self.zainteresowania_frame, text='1. Zainteresowania')
        self.notebook.add(self.przedmioty_frame, text='2. Przedmioty')
        self.notebook.add(self.cechy_frame, text='3. Cechy')
        self.notebook.add(self.style_frame, text='4. Style nauki')
        self.notebook.add(self.podsumowanie_frame, text='5. Podsumowanie', state='disabled')
        self.notebook.add(self.wyniki_frame, text='6. Wyniki', state='disabled')
        
        # Utwórz checkboxy
        self.create_checkboxes()
        
        # Przyciski nawigacyjne
        self.nav_frame = tk.Frame(self.master, bg="#e6f0ff")
        self.nav_frame.pack(pady=10, fill='x')
        
        self.prev_btn = tk.Button(self.nav_frame, text="← Poprzedni", command=self.prev_step,
                                 bg="#4a90e2", fg="white", font=("Arial", 10, "bold"),
                                 relief="raised", bd=2, state='disabled')
        self.prev_btn.pack(side='left', padx=5)
        
        self.next_btn = tk.Button(self.nav_frame, text="Następny →", command=self.next_step,
                                 bg="#4a90e2", fg="white", font=("Arial", 10, "bold"),
                                 relief="raised", bd=2)
        self.next_btn.pack(side='left', padx=5)
        
        self.analizuj_btn = tk.Button(self.nav_frame, text="Analizuj", command=self.analizuj,
                                     bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                                     relief="raised", bd=2)
        self.analizuj_btn.pack_forget()
        
        self.reset_btn = tk.Button(self.nav_frame, text="Rozpocznij od nowa", command=self.reset,
                                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                                  relief="raised", bd=2)
        self.reset_btn.pack_forget()
        
        # Inicjalizacja Prologa
        self.prolog = Prolog()
        self.prolog.consult("rekomendacje.pl")
        
        # Utwórz podsumowanie
        self.create_summary()
        
    def create_checkboxes(self):
        categories = [
            ('Zainteresowania', self.zainteresowania, self.zainteresowania_frame),
            ('Przedmioty', self.przedmioty, self.przedmioty_frame),
            ('Cechy', self.cechy, self.cechy_frame),
            ('Style nauki', self.style, self.style_frame)
        ]
        
        for category_name, items, frame in categories:
            # Kontener na checkboxy z przewijaniem
            container = tk.Frame(frame, bg="#f0f6ff")
            container.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Canvas i scrollbar
            canvas = tk.Canvas(container, bg="#f0f6ff", highlightthickness=0)
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#f0f6ff")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e, canvas=canvas: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Pole wyszukiwania
            search_frame = tk.Frame(scrollable_frame, bg="#f4f6f8")
            search_frame.pack(fill='x', pady=(0, 10))
            
            search_label = tk.Label(search_frame, text="Wyszukaj:", bg="#f4f6f8", font=("Arial", 9, "bold"))
            search_label.pack(side='left', padx=(0, 5))
            
            search_var = tk.StringVar()
            search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 9), bg="#ffffff", fg="#2c3e50",  # białe pole, granatowy tekst
    relief="solid", borderwidth=1)
            search_entry.pack(side='left', fill='x', expand=True)
            
            search_entry.bind('<KeyRelease>', lambda e, items=items, scrollable_frame=scrollable_frame, category_name=category_name: 
                             self.filter_checkboxes(e, items, scrollable_frame, category_name))
            
            # Checkboxy w kolumnach
            self.create_category_checkboxes(category_name, items, scrollable_frame)
            
    def create_category_checkboxes(self, category_name, items, parent_frame):
        # Usuń stare checkboxy jeśli istnieją
        for widget in parent_frame.winfo_children():
            if widget.winfo_class() == 'Frame' and widget != parent_frame.winfo_children()[0]:
                widget.destroy()
        
        # Utwórz nowe checkboxy
        columns = 3
        row_frame = None
        
        for index, item in enumerate(items):
            if index % columns == 0:
                row_frame = tk.Frame(parent_frame, bg="#283593")
                row_frame.pack(fill='x', padx=5, pady=2)
            
            var = tk.IntVar()
            cb = tk.Checkbutton(
                row_frame, text=item, variable=var,
                bg="#e8ecf1", fg="#2c3e50", activebackground="#d0e6f9",
                activeforeground="#2c3e50", font=("Arial", 9, "bold"),
                selectcolor="#B0C4DE", relief="flat",
                padx=10, pady=3
            )
            cb.pack(side='left', fill='x', expand=True)
            self.check_vars[item] = var
            
    def filter_checkboxes(self, event, items, parent_frame, category_name):
        search_term = event.widget.get().lower()
        filtered_items = [item for item in items if search_term in item.lower()]
        self.create_category_checkboxes(category_name, filtered_items, parent_frame)
        
    def create_summary(self):
        # Nagłówek
        tk.Label(self.podsumowanie_frame, text="Podsumowanie Twoich wyborów", 
                font=("Arial", 14, "bold"), bg="#f4f6f8", fg="#2c3e50").pack(pady=10)
        
        # Ramka na podsumowanie
        self.summary_container = tk.Frame(self.podsumowanie_frame, bg="#f0f6ff")
        self.summary_container.pack(fill='both', expand=True, padx=20, pady=10)
        
    def update_summary(self):
        # Wyczyść poprzednie podsumowanie
        for widget in self.summary_container.winfo_children():
            widget.destroy()
        
        # Zbierz zaznaczone opcje
        selected_zainteresowania = [item for item in self.zainteresowania if self.check_vars[item].get() == 1]
        selected_przedmioty = [item for item in self.przedmioty if self.check_vars[item].get() == 1]
        selected_cechy = [item for item in self.cechy if self.check_vars[item].get() == 1]
        selected_style = [item for item in self.style if self.check_vars[item].get() == 1]
        
        # Wyświetl podsumowanie
        categories = [
            ("Zainteresowania", selected_zainteresowania),
            ("Przedmioty", selected_przedmioty),
            ("Cechy", selected_cechy),
            ("Style nauki", selected_style)
        ]
        
        for category, items in categories:
            frame = tk.Frame(self.summary_container, bg="#f0f6ff")
            frame.pack(fill='x', pady=5)
            
            tk.Label(frame, text=f"{category}:", font=("Arial", 11, "bold"), 
                    bg="#f0f6ff", fg="#003366").pack(anchor='w')
            
            if items:
                text = ", ".join(items)
                tk.Label(frame, text=text, font=("Arial", 10), 
                        bg="#f0f6ff", fg="#003366", wraplength=800, justify='left').pack(anchor='w')
            else:
                tk.Label(frame, text="Brak wybranych opcji", font=("Arial", 10, "italic"), 
                        bg="#f0f6ff", fg="#666666").pack(anchor='w')
    
    def next_step(self):
        current = self.notebook.index(self.notebook.select())
        
        # Sprawdź czy użytkownik wybrał przynajmniej jedną opcję
        if current == 0:
            selected = [item for item in self.zainteresowania if self.check_vars[item].get() == 1]
            if not selected:
                messagebox.showwarning("Ostrzeżenie", "Proszę wybrać przynajmniej jedno zainteresowanie.")
                return
        elif current == 1:
            selected = [item for item in self.przedmioty if self.check_vars[item].get() == 1]
            if not selected:
                messagebox.showwarning("Ostrzeżenie", "Proszę wybrać przynajmniej jeden przedmiot.")
                return
        elif current == 2:
            selected = [item for item in self.cechy if self.check_vars[item].get() == 1]
            if not selected:
                messagebox.showwarning("Ostrzeżenie", "Proszę wybrać przynajmniej jedną cechę.")
                return
        elif current == 3:
            selected = [item for item in self.style if self.check_vars[item].get() == 1]
            if not selected:
                messagebox.showwarning("Ostrzeżenie", "Proszę wybrać przynajmniej jeden styl nauki.")
                return
        
        if current < 4:  # Jeśli nie jesteśmy na ostatniej karcie przed wynikami
            self.notebook.select(current + 1)
            
            # Aktualizuj podsumowanie jeśli przechodzimy na tę kartę
            if current + 1 == 4:
                self.update_summary()
                self.next_btn.pack_forget()
                self.analizuj_btn.pack(side='left', padx=5)
        
        # Aktywuj przycisk "Wstecz" jeśli nie jesteśmy na pierwszej karcie
        if current + 1 > 0:
            self.prev_btn.config(state='normal')
    
    def prev_step(self):
        current = self.notebook.index(self.notebook.select())
        if current > 0:
            self.notebook.select(current - 1)
            
            # Ukryj przycisk "Analizuj" jeśli wracamy z podsumowania
            if current == 4:
                self.analizuj_btn.pack_forget()
                self.next_btn.pack(side='left', padx=5)
                self.reset_btn.pack_forget()
            
            # Ukryj przycisk "Wstecz" jeśli jesteśmy na pierwszej karcie
            if current - 1 == 0:
                self.prev_btn.config(state='disabled')
    
    def analizuj(self):
        # Zbierz zaznaczone opcje
        zainteresowania = [item for item in self.zainteresowania if self.check_vars[item].get() == 1]
        przedmioty = [item for item in self.przedmioty if self.check_vars[item].get() == 1]
        cechy = [item for item in self.cechy if self.check_vars[item].get() == 1]
        style = [item for item in self.style if self.check_vars[item].get() == 1]
        
        # Przygotuj zapytanie do Prologa
        query = f"top5_dopasowania({zainteresowania}, {przedmioty}, {cechy}, {style}, Top5)."
        
        try:
            results = list(self.prolog.query(query, maxresult=1))
            
            if results:
                top5 = results[0]['Top5']
                if isinstance(top5, list):
                    # Upewnij się, że mamy 5 wyników
                    while len(top5) < 5:
                        top5.append(['Brak dopasowania', 0])
                    
                    # Wyświetl wyniki
                    self.show_results(top5)
                    
                    # Przejdź do wyników
                    self.notebook.tab(5, state='normal')
                    self.notebook.select(5)
                    self.analizuj_btn.pack_forget()
                    self.reset_btn.pack(side='left', padx=5)
                else:
                    messagebox.showerror("Błąd", "Nieprawidłowy format wyników z Prologa.")
            else:
                messagebox.showerror("Błąd", "Nie udało się uzyskać wyników.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas analizy: {str(e)}")
    
    def show_results(self, top5):
        # Wyczyść poprzednie wyniki
        for widget in self.wyniki_frame.winfo_children():
            widget.destroy()
        
        # Nagłówek
        tk.Label(self.wyniki_frame, text="Twoje najlepsze dopasowania", 
                font=("Arial", 14, "bold"), bg="#f0f6ff", fg="#003366").pack(pady=10)
        
        # Kontener na wyniki
        results_container = tk.Frame(self.wyniki_frame, bg="#f0f6ff")
        results_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Wyświetl wyniki
        for i, (kierunek, wynik) in enumerate(top5):
            wynik_zaokraglony = round(wynik, 2)
            
            # Kontener dla pojedynczego wyniku
            result_frame = tk.Frame(results_container, bg="#e6f0ff", bd=1, relief="solid")
            result_frame.pack(fill='x', pady=5)
            
            # Numer i nazwa kierunku
            tk.Label(result_frame, text=f"{i+1}. {kierunek}", 
                    font=("Arial", 12, "bold"), bg="#e6f0ff", fg="#003366").pack(anchor='w', padx=10, pady=5)
            
            # Pasek postępu
            progress_frame = tk.Frame(result_frame, bg="#e6f0ff")
            progress_frame.pack(fill='x', padx=10, pady=(0, 10))
            
            # Tło paska
            progress_bg = tk.Frame(progress_frame, bg="#d9e6ff", height=20)
            progress_bg.pack(fill='x')
            
            # Pasek wypełnienia
            fill_width = min(int(wynik_zaokraglony * 3), 300)  # Skalowanie do szerokości
            fill = tk.Frame(progress_bg, bg="#4a90e2", height=20, width=fill_width)
            fill.pack(side='left')
            
            # Etykieta z procentami
            tk.Label(progress_bg, text=f"{wynik_zaokraglony}%", 
                    font=("Arial", 10), bg="#d9e6ff", fg="#003366").pack(side='right', padx=5)
    
    def reset(self):
        # Wyczyść wszystkie checkboxy
        for var in self.check_vars.values():
            var.set(0)
        
        # Wróć do pierwszej karty
        self.notebook.select(0)
        self.prev_btn.config(state='disabled')
        self.next_btn.pack(side='left', padx=5)
        self.analizuj_btn.pack_forget()
        self.reset_btn.pack_forget()
        
        # Wyłącz karty podsumowania i wyników
        self.notebook.tab(4, state='disabled')
        self.notebook.tab(5, state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x750")
    root.configure(bg="#e6f0ff")
    
    # Główna ramka
    main_frame = tk.Frame(root, bg="#e6f0ff")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    app = KierunkiApp(root, main_frame)
    
    root.mainloop()