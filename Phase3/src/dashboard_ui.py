import tkinter as tk
from tkinter import ttk
from studiengang import Studiengang


class DashboardUI:
    """Grafische Oberfläche zur Anzeige des Studienfortschritts.

    Beziehung zu Studiengang: Abhängigkeit. Die DashboardUI verwendet
    ein Studiengang-Objekt zur Anzeige, besitzt es aber nicht.
    """

    def __init__(self, studiengang: Studiengang):
        self.__studiengang = studiengang
        self.__fenster = tk.Tk()
        self.__fenster.title("Mein Studiums-Dashboard")
        self.__fenster.geometry("420x340")

    def zeige_fortschritt(self) -> None:
        """Zeigt die drei Hauptkennzahlen (Ziele) mit Fortschrittsbalken an."""
        titel = tk.Label(
            self.__fenster,
            text=self.__studiengang.get_name(),
            font=("Arial", 18, "bold")
        )
        titel.pack(pady=(20, 15))

        # --- Ziel 1: ECTS-Fortschritt ---
        fortschritt = self.__studiengang.get_fortschritt()
        tk.Label(self.__fenster, text="ECTS-Fortschritt", font=("Arial", 11)).pack(anchor="w", padx=30)
        balken1 = ttk.Progressbar(self.__fenster, length=350, maximum=100, value=fortschritt)
        balken1.pack(padx=30, pady=(2, 2))
        ects_absolviert = self.__studiengang.get_ects_gesamt_absolviert()
        tk.Label(self.__fenster, text=f"{fortschritt}% ({ects_absolviert}/180 ECTS)", font=("Arial", 10)).pack(anchor="e", padx=30)

        # --- Ziel 2: Notendurchschnitt ---
        notenschnitt = self.__studiengang.get_notenschnitt()
        noten_prozent = max(0, min(100, (4.0 - notenschnitt) / 3.0 * 100))
        tk.Label(self.__fenster, text="Notendurchschnitt", font=("Arial", 11)).pack(anchor="w", padx=30, pady=(12, 0))
        balken2 = ttk.Progressbar(self.__fenster, length=350, maximum=100, value=noten_prozent)
        balken2.pack(padx=30, pady=(2, 2))
        tk.Label(self.__fenster, text=f"{notenschnitt}", font=("Arial", 10)).pack(anchor="e", padx=30)

        # --- Ziel 3: Aktuelles Semester ---
        aktuelles_semester = self.__studiengang.get_aktuelles_semester()
        anzahl_semester = len(self.__studiengang.get_semester())
        if aktuelles_semester:
            semester_text = f"Semester {aktuelles_semester.get_nummer()} von {anzahl_semester}"
        else:
            semester_text = "Studium abgeschlossen!"
        tk.Label(self.__fenster, text="Aktuelles Semester", font=("Arial", 11)).pack(anchor="w", padx=30, pady=(12, 0))
        tk.Label(self.__fenster, text=semester_text, font=("Arial", 13, "bold")).pack(anchor="w", padx=30)

    def starten(self) -> None:
        """Startet die Tkinter-Hauptschleife (öffnet das Fenster)."""
        self.__fenster.mainloop()