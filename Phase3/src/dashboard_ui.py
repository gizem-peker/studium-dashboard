import tkinter as tk
from tkinter import ttk
from studiengang import Studiengang


class DashboardUI:
    """Grafische Oberfläche: Übersicht über den Studienfortschritt und Modulsuche.

    Die Oberfläche stellt nur dar und verarbeitet die Sucheingabe. Alle
    Berechnungen (Fortschritt, Notenschnitt, Zeitplan, Suche) machen die
    Domain-Klassen.

    Beziehung zu Studiengang: Abhängigkeit. Die DashboardUI verwendet
    ein Studiengang-Objekt zur Anzeige, besitzt es aber nicht.
    """

    MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
              "August", "September", "Oktober", "November", "Dezember"]

    def __init__(self, studiengang: Studiengang):
        self._studiengang = studiengang
        self._fenster = tk.Tk()
        self._fenster.title("Mein Studiums-Dashboard")
        self._fenster.geometry("460x660")
        self._suchfeld = None
        self._ergebnis_label = None

    @staticmethod
    def _zahl(wert: float) -> str:
        """Zahl mit deutschem Dezimalkomma (1.75 -> 1,75)."""
        return str(wert).replace(".", ",")

    def zeige_fortschritt(self) -> None:
        """Zeigt die drei Kennzahlen (Ziele) mit Fortschrittsbalken an."""
        sg = self._studiengang
        tk.Label(self._fenster, text=sg.name, font=("Arial", 18, "bold")).pack(pady=(20, 15))

        # --- Ziel 1: ECTS-Fortschritt und Zeitplan ---
        ects_absolviert = sg.summiere_ects()
        fortschritt = sg.berechne_fortschritt()
        tk.Label(self._fenster, text="ECTS-Fortschritt", font=("Arial", 11)).pack(anchor="w", padx=30)
        ttk.Progressbar(self._fenster, length=400, maximum=100, value=fortschritt).pack(padx=30, pady=(2, 2))
        tk.Label(self._fenster, text=f"{fortschritt}% ({ects_absolviert}/{sg.gesamt_ects} ECTS)",
                 font=("Arial", 10)).pack(anchor="e", padx=30)

        soll_ects = sg.berechne_soll_ects()
        if sg.ist_im_zeitplan():
            zeitplan_text = f"Im Zeitplan (Soll bis heute: {soll_ects} ECTS)"
            zeitplan_farbe = "#2e7d32"
        else:
            zeitplan_text = (f"Verzögerung: {sg.berechne_verzoegerung_ects()} ECTS hinter dem Plan "
                             f"(Soll bis heute: {soll_ects} ECTS)")
            zeitplan_farbe = "#c62828"
        tk.Label(self._fenster, text=zeitplan_text, font=("Arial", 10, "bold"), fg=zeitplan_farbe,
                 justify="left", wraplength=400).pack(anchor="w", padx=30, pady=(4, 0))
        abschluss = sg.berechne_geplanten_abschluss()
        tk.Label(self._fenster, text=f"Geplanter Abschluss: {self.MONATE[abschluss.month - 1]} {abschluss.year}",
                 font=("Arial", 10)).pack(anchor="w", padx=30)

        # --- Ziel 2: Notendurchschnitt ---
        notenschnitt = sg.berechne_notenschnitt()
        if notenschnitt is not None:
            # Skala für den Balken: 1,0 = voll, 4,0 = leer
            noten_prozent = max(0, min(100, (4.0 - notenschnitt) / 3.0 * 100))
            noten_text = self._zahl(notenschnitt)
        else:
            noten_prozent = 0
            noten_text = "noch keine Note"
        tk.Label(self._fenster, text=f"Notendurchschnitt (Ziel: ≤ {self._zahl(sg.zielnote)})",
                 font=("Arial", 11)).pack(anchor="w", padx=30, pady=(12, 0))
        ttk.Progressbar(self._fenster, length=400, maximum=100, value=noten_prozent).pack(padx=30, pady=(2, 2))
        tk.Label(self._fenster, text=noten_text, font=("Arial", 10)).pack(anchor="e", padx=30)

        # --- Ziel 3: Aktuelles Semester und Modulfortschritt ---
        semester = sg.ermittle_aktuelles_semester()
        tk.Label(self._fenster, text="Aktuelles Semester", font=("Arial", 11)).pack(anchor="w", padx=30, pady=(12, 0))
        if semester:
            semester_text = f"Semester {semester.nummer} von {len(sg.semester)}"
        else:
            semester_text = "Studium abgeschlossen!"
        tk.Label(self._fenster, text=semester_text, font=("Arial", 13, "bold")).pack(anchor="w", padx=30)

        if semester:
            bestanden = semester.zaehle_bestandene_module()
            geplant = semester.berechne_geplante_module()
            modul_prozent = bestanden / geplant * 100 if geplant else 0
            ttk.Progressbar(self._fenster, length=400, maximum=100, value=modul_prozent).pack(padx=30, pady=(4, 2))
            tk.Label(self._fenster,
                     text=f"{bestanden} von {geplant} Modulen bestanden "
                          f"({semester.summiere_ects()}/{semester.ects_ziel} ECTS)",
                     font=("Arial", 10)).pack(anchor="e", padx=30)

    def zeige_suche(self) -> None:
        """Baut den Suchbereich auf: Eingabefeld, Button und Ergebnisanzeige."""
        rahmen = tk.Frame(self._fenster)
        rahmen.pack(fill="x", padx=30, pady=(25, 0))

        tk.Label(rahmen, text="Modul suchen", font=("Arial", 11)).pack(anchor="w")

        zeile = tk.Frame(rahmen)
        zeile.pack(fill="x", pady=(2, 0))
        self._suchfeld = tk.Entry(zeile, font=("Arial", 11))
        self._suchfeld.pack(side="left", fill="x", expand=True)
        self._suchfeld.bind("<Return>", lambda event: self._fuehre_suche_aus())
        tk.Button(zeile, text="Suchen", command=self._fuehre_suche_aus).pack(side="left", padx=(8, 0))

        self._ergebnis_label = tk.Label(rahmen, text="", font=("Arial", 10),
                                        justify="left", anchor="w", wraplength=400)
        self._ergebnis_label.pack(fill="x", pady=(10, 0))

    def starten(self) -> None:
        """Startet die Tkinter-Hauptschleife (öffnet das Fenster)."""
        self._fenster.mainloop()

    def _fuehre_suche_aus(self) -> None:
        """Gibt den Suchtext an den Studiengang weiter und zeigt die Treffer an."""
        suchtext = self._suchfeld.get().strip()
        if not suchtext:
            self._ergebnis_label.config(text="")  # leeres Feld: nur die Übersicht bleibt
            return

        treffer = self._studiengang.suche_module(suchtext)
        if not treffer:
            self._ergebnis_label.config(text=f'Kein Modul gefunden für "{suchtext}".')
            return
        self._ergebnis_label.config(text="\n\n".join(self._formatiere_modul(m) for m in treffer))

    def _formatiere_modul(self, modul) -> str:
        """Erzeugt den Anzeigetext mit Status, Note und Datum eines Moduls."""
        note_text = self._zahl(modul.note) if modul.note is not None else "noch keine Note"
        datum_text = modul.datum.strftime("%d.%m.%Y") if modul.datum else "kein Datum"
        return (f"{modul.name} ({modul.ects} ECTS)\n"
                f"Status: {modul.ermittle_status().value}\n"
                f"Note: {note_text}\n"
                f"{modul.pruefungsart.value}, Datum: {datum_text}")
