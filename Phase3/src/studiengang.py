from datetime import date
from modul import Modul, ModulStatus
from semester import Semester


class Studiengang:
    """Der gesamte Studiengang mit allen Semestern.

    Beziehung zu Semester: Komposition. Die Semester werden im
    Studiengang verwaltet und existieren nicht unabhängig davon.
    """

    def __init__(self, name: str, beginn: date, gesamt_ects: int = 180,
                 zielnote: float = 2.0):
        self._name = name
        self._beginn = beginn
        self._gesamt_ects = gesamt_ects
        self._zielnote = zielnote
        self._semester = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def beginn(self) -> date:
        return self._beginn

    @property
    def gesamt_ects(self) -> int:
        return self._gesamt_ects

    @property
    def zielnote(self) -> float:
        return self._zielnote

    @property
    def semester(self) -> list:
        """Kopie der Semesterliste."""
        return list(self._semester)

    def semester_hinzufuegen(self, semester: Semester) -> None:
        self._semester.append(semester)

    # ---------------- Ziel 1: Zeitplan ----------------

    def summiere_ects(self) -> int:
        """Summe der ECTS aller bestandenen Module."""
        return sum(s.summiere_ects() for s in self._semester)

    def berechne_fortschritt(self) -> float:
        """Prozentualer ECTS-Fortschritt."""
        return round(self.summiere_ects() / self._gesamt_ects * 100, 1)

    def berechne_soll_ects(self, stichtag: date | None = None) -> int:
        """ECTS, die laut Plan bis zum Stichtag erreicht sein sollen.

        Plan: ein Modul pro Monat. Gezählt werden nur vollständig vergangene
        Monate seit dem Studienbeginn (bei Beginn am 15. März zählt der erste
        Monat erst ab dem 15. April). Ohne Angabe gilt das heutige Datum.
        """
        stichtag = stichtag or date.today()
        monate = (stichtag.year - self._beginn.year) * 12 + stichtag.month - self._beginn.month
        if stichtag.day < self._beginn.day:
            monate -= 1  # der angefangene Monat ist noch nicht vollständig
        monate = max(0, monate)
        return min(monate * Modul.STANDARD_ECTS, self._gesamt_ects)

    def ist_im_zeitplan(self, stichtag: date | None = None) -> bool:
        """True, wenn mindestens so viele ECTS erreicht sind wie geplant."""
        return self.summiere_ects() >= self.berechne_soll_ects(stichtag)

    def berechne_verzoegerung_ects(self, stichtag: date | None = None) -> int:
        """Wie viele ECTS fehlen zum Plan? 0, wenn man im Zeitplan liegt."""
        return max(0, self.berechne_soll_ects(stichtag) - self.summiere_ects())

    def berechne_geplanten_abschluss(self) -> date:
        """Geplanter Abschluss: Beginn plus 6 Monate pro Semester (nur Monat und Jahr)."""
        monate_gesamt = self._beginn.month - 1 + len(self._semester) * 6
        return date(self._beginn.year + monate_gesamt // 12, monate_gesamt % 12 + 1, 1)

    # ---------------- Ziel 2: Notendurchschnitt ----------------

    def berechne_notenschnitt(self) -> float | None:
        """Notendurchschnitt über alle bestandenen Module.

        Gibt None zurück, solange noch kein Modul bestanden wurde.
        """
        noten = []
        for semester in self._semester:
            for modul in semester.module:
                if modul.ermittle_status() == ModulStatus.BESTANDEN:
                    noten.append(modul.note)
        if not noten:
            return None
        return round(sum(noten) / len(noten), 2)

    # ---------------- Ziel 3: Semester ----------------

    def ermittle_aktuelles_semester(self) -> Semester | None:
        """Erstes noch nicht abgeschlossenes Semester (None, wenn alle abgeschlossen sind)."""
        for semester in self._semester:
            if not semester.ist_abgeschlossen():
                return semester
        return None

    # ---------------- Suche ----------------

    def suche_module(self, suchtext: str) -> list:
        """Sucht Module, deren Name den Suchtext enthält.

        Groß- und Kleinschreibung wird ignoriert. Bei leerem Suchtext
        wird eine leere Liste zurückgegeben.
        """
        suchtext = suchtext.strip().lower()
        if not suchtext:
            return []
        treffer = []
        for semester in self._semester:
            for modul in semester.module:
                if suchtext in modul.name.lower():
                    treffer.append(modul)
        return treffer
