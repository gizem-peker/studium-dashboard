import tkinter as tk
from tkinter import ttk
from studiengang import Studiengang


class DashboardUI:
    """Grafische Oberfläche: Übersicht über den Studienfortschritt und Modulsuche.

    Beziehung zu Studiengang: Abhängigkeit. Die DashboardUI verwendet
    ein Studiengang-Objekt zur Anzeige, besitzt es aber nicht.
    """

    def __init__(self, studiengang: Studiengang):
        self.__studiengang = studiengang
        self.__fenster = tk.Tk()
        self.__fenster.title("Mein Studiums-Dashboard")
        self.__fenster.geometry("460x560")
        self.__suchfeld = None
        self.__ergebnis_label = None

    def zeige_fortschritt(self) -> None:
        """Zeigt die drei Kennzahlen (Ziele) mit Fortschrittsbalken an."""
        tk.Label(
            self.__fenster,
            text=self.__studiengang.get_name(),
            font=("Arial", 18, "bold")
        ).pack(pady=(20, 15))

        # --- Ziel 1: ECTS-Fortschritt ---
        fortschritt = self.__studiengang.get_fortschritt()
        ects_absolviert = self.__studiengang.get_ects_gesamt_absolviert()
        ects_gesamt = self.__studiengang.get_gesamt_ects()
        tk.Label(self.__fenster, text="ECTS-Fortschritt", font=("Arial", 11)).pack(anchor="w", padx=30)
        ttk.Progressbar(self.__fenster, length=400, maximum=100, value=fortschritt).pack(padx=30, pady=(2, 2))
        tk.Label(self.__fenster, text=f"{fortschritt}% ({ects_absolviert}/{ects_gesamt} ECTS)",
                 font=("Arial", 10)).pack(anchor="e", padx=30)

        # --- Ziel 2: Notendurchschnitt ---
        notenschnitt = self.__studiengang.get_notenschnitt()
        if notenschnitt > 0:
            # Skala: 1,0 = voller Balken, 4,0 = leerer Balken
            noten_prozent = max(0, min(100, (4.0 - notenschnitt) / 3.0 * 100))
            noten_text = f"{notenschnitt}"
        else:
            noten_prozent = 0
            noten_text = "noch keine Note"
        tk.Label(self.__fenster, text="Notendurchschnitt", font=("Arial", 11)).pack(anchor="w", padx=30, pady=(12, 0))
        ttk.Progressbar(self.__fenster, length=400, maximum=100, value=noten_prozent).pack(padx=30, pady=(2, 2))
        tk.Label(self.__fenster, text=noten_text, font=("Arial", 10)).pack(anchor="e", padx=30)

        # --- Ziel 3: Aktuelles Semester ---
        aktuelles_semester = self.__studiengang.get_aktuelles_semester()
        anzahl_semester = len(self.__studiengang.get_semester())
        if aktuelles_semester:
            semester_text = f"Semester {aktuelles_semester.get_nummer()} von {anzahl_semester}"
        else:
            semester_text = "Studium abgeschlossen!"
        tk.Label(self.__fenster, text="Aktuelles Semester", font=("Arial", 11)).pack(anchor="w", padx=30, pady=(12, 0))
        tk.Label(self.__fenster, text=semester_text, font=("Arial", 13, "bold")).pack(anchor="w", padx=30)

    def zeige_suche(self) -> None:
        """Baut den Suchbereich auf: Eingabefeld, Button und Ergebnisanzeige."""
        rahmen = tk.Frame(self.__fenster)
        rahmen.pack(fill="x", padx=30, pady=(25, 0))

        tk.Label(rahmen, text="Modul suchen", font=("Arial", 11)).pack(anchor="w")

        zeile = tk.Frame(rahmen)
        zeile.pack(fill="x", pady=(2, 0))
        self.__suchfeld = tk.Entry(zeile, font=("Arial", 11))
        self.__suchfeld.pack(side="left", fill="x", expand=True)
        self.__suchfeld.bind("<Return>", lambda event: self.__fuehre_suche_aus())
        tk.Button(zeile, text="Suchen", command=self.__fuehre_suche_aus).pack(side="left", padx=(8, 0))

        self.__ergebnis_label = tk.Label(rahmen, text="", font=("Arial", 10),
                                         justify="left", anchor="w", wraplength=400)
        self.__ergebnis_label.pack(fill="x", pady=(10, 0))

    def __fuehre_suche_aus(self) -> None:
        """Sucht Module zum eingegebenen Text und zeigt die Details an."""
        suchtext = self.__suchfeld.get().strip()

        if not suchtext:
            # leeres Feld: nur die Übersicht bleibt sichtbar
            self.__ergebnis_label.config(text="")
            return

        treffer = self.__studiengang.suche_module(suchtext)
        if not treffer:
            self.__ergebnis_label.config(text=f'Kein Modul gefunden für "{suchtext}".')
            return

        texte = [self.__formatiere_modul(modul) for modul in treffer]
        self.__ergebnis_label.config(text="\n\n".join(texte))

    def __formatiere_modul(self, modul) -> str:
        """Erzeugt den Anzeigetext mit Status, Note und Datum eines Moduls."""
        note = modul.get_note()
        note_text = f"{note}" if note is not None else "noch keine Note"
        datum_text = modul.get_datum() or "kein Datum"
        return (f"{modul.get_name()} ({modul.get_ects()} ECTS)\n"
                f"Status: {modul.get_status().value}\n"
                f"Note: {note_text}\n"
                f"{modul.get_pruefungsart().value}, Datum: {datum_text}")

    def starten(self) -> None:
        """Startet die Tkinter-Hauptschleife (öffnet das Fenster)."""
        self.__fenster.mainloop()