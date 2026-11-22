import json
from datetime import date
from modul import Modul
from pruefungsleistung import Pruefungsart
from semester import Semester
from studiengang import Studiengang

NOTE_MIN = 1.0
NOTE_MAX = 5.0
MAX_SEMESTER = 6
MAX_MODULE_PRO_SEMESTER = 6


class DatenManager:
    """Lädt einen Studiengang aus einer JSON-Datei.

    Beziehung zu Studiengang: Abhängigkeit. Der DatenManager erzeugt ein
    Studiengang-Objekt, besitzt es aber nicht.

    Die JSON-Datei wird von Hand gepflegt. Deshalb wird sie beim Laden
    geprüft: Jedes Problem führt zu einem ValueError mit einer Meldung,
    die sagt, was in der Datei zu korrigieren ist.
    """

    def __init__(self, dateipfad: str):
        self._dateipfad = dateipfad

    def lade_daten(self) -> Studiengang:
        """Liest die JSON-Datei, prüft sie und baut die Objektstruktur auf."""
        daten = self._lese_json()
        if not isinstance(daten, dict):
            raise ValueError("Die Datei muss mit einem JSON-Objekt { ... } beginnen.")

        name = self._text(self._pflichtfeld(daten, "name", "Studiengang"), "Studiengang", "name")
        beginn = self._datum(self._pflichtfeld(daten, "beginn", "Studiengang"), "Studiengang", "beginn")
        semester_liste = self._pflichtfeld(daten, "semester", "Studiengang")
        if not isinstance(semester_liste, list) or not 1 <= len(semester_liste) <= MAX_SEMESTER:
            raise ValueError(f'Studiengang: "semester" muss eine Liste mit 1 bis {MAX_SEMESTER} Einträgen sein.')

        studiengang = Studiengang(name, beginn)
        for position, semester_daten in enumerate(semester_liste, start=1):
            studiengang.semester_hinzufuegen(self._baue_semester(semester_daten, position))
        return studiengang

    # ---------- Aufbau der Objekte ----------

    def _baue_semester(self, daten: dict, position: int) -> Semester:
        ort = f"Semester an Position {position}"
        nummer = self._ganzzahl(self._pflichtfeld(daten, "nummer", ort), ort, "nummer")
        ort = f"Semester {nummer}"
        module_liste = self._pflichtfeld(daten, "module", ort)
        if not isinstance(module_liste, list) or len(module_liste) > MAX_MODULE_PRO_SEMESTER:
            raise ValueError(f'{ort}: "module" muss eine Liste mit höchstens {MAX_MODULE_PRO_SEMESTER} Modulen sein.')

        semester = Semester(nummer)
        for i, modul_daten in enumerate(module_liste, start=1):
            semester.modul_hinzufuegen(self._baue_modul(modul_daten, f"{ort}, Modul {i}"))
        return semester

    def _baue_modul(self, daten: dict, ort: str) -> Modul:
        name = self._text(self._pflichtfeld(daten, "name", ort), ort, "name")
        ort = f'{ort} ("{name}")'
        pruefungsart = self._pruefungsart(self._pflichtfeld(daten, "pruefungsart", ort), ort)
        ects = Modul.STANDARD_ECTS
        if daten.get("ects") is not None:
            ects = self._ganzzahl(daten["ects"], ort, "ects")
        note = self._note(daten["note"], ort) if daten.get("note") is not None else None
        datum = self._datum(daten["datum"], ort, "datum") if daten.get("datum") is not None else None
        return Modul(name, pruefungsart, ects, note, datum)

    # ---------- Einlesen und Prüfen ----------

    def _lese_json(self):
        try:
            with open(self._dateipfad, "r", encoding="utf-8") as datei:
                return json.load(datei)
        except FileNotFoundError:
            raise ValueError(f'Die Datei "{self._dateipfad}" wurde nicht gefunden.')
        except json.JSONDecodeError as fehler:
            raise ValueError(f"Die Datei ist kein gültiges JSON (Zeile {fehler.lineno}, "
                             f"Spalte {fehler.colno}): {fehler.msg}.")
        except UnicodeDecodeError:
            raise ValueError("Die Datei muss im Format UTF-8 gespeichert sein.")
        except OSError as fehler:
            raise ValueError(f"Die Datei konnte nicht gelesen werden: {fehler.strerror}.")

    def _pflichtfeld(self, daten, schluessel: str, ort: str):
        if not isinstance(daten, dict) or daten.get(schluessel) is None:
            raise ValueError(f'{ort}: Das Feld "{schluessel}" fehlt.')
        return daten[schluessel]

    def _text(self, wert, ort: str, feld: str) -> str:
        if not isinstance(wert, str) or not wert.strip():
            raise ValueError(f'{ort}: "{feld}" muss ein nicht leerer Text sein.')
        return wert.strip()

    def _ganzzahl(self, wert, ort: str, feld: str) -> int:
        if isinstance(wert, bool) or not isinstance(wert, int) or wert <= 0:
            raise ValueError(f'{ort}: "{feld}" muss eine ganze Zahl größer als 0 sein.')
        return wert

    def _note(self, wert, ort: str) -> float:
        if isinstance(wert, bool) or not isinstance(wert, (int, float)) or not NOTE_MIN <= wert <= NOTE_MAX:
            raise ValueError(f'{ort}: "note" muss eine Zahl zwischen {NOTE_MIN} und {NOTE_MAX} sein '
                             f'(oder null, wenn noch keine Note vorliegt).')
        return float(wert)

    def _datum(self, wert, ort: str, feld: str) -> date:
        try:
            return date.fromisoformat(wert)
        except (TypeError, ValueError):
            raise ValueError(f'{ort}: "{feld}" ist kein gültiges Datum. '
                             f'Erwartet wird z. B. "2026-03-01" (Format JJJJ-MM-TT).')

    def _pruefungsart(self, wert, ort: str) -> Pruefungsart:
        try:
            return Pruefungsart[wert]
        except (KeyError, TypeError):
            raise ValueError(f'{ort}: Ungültige Prüfungsart. Erlaubt sind: KLAUSUR oder PROJEKTARBEIT.')
