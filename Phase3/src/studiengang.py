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
        self.__name = name
        self.__beginn = beginn
        self.__gesamt_ects = gesamt_ects
        self.__zielnote = zielnote
        self.__semester = []

    def get_name(self) -> str:
        return self.__name

    def get_beginn(self) -> date:
        return self.__beginn

    def get_gesamt_ects(self) -> int:
        return self.__gesamt_ects

    def get_zielnote(self) -> float:
        return self.__zielnote

    def semester_hinzufuegen(self, semester: Semester) -> None:
        self.__semester.append(semester)

    def get_semester(self) -> list:
        return self.__semester

    def get_ects_gesamt_absolviert(self) -> int:
        return sum(s.get_ects_absolviert() for s in self.__semester)

    def get_fortschritt(self) -> float:
        """Prozentualer ECTS-Fortschritt (Ziel 1: Zeitplan)."""
        return round(self.get_ects_gesamt_absolviert() / self.__gesamt_ects * 100, 1)

    def get_soll_ects(self, stichtag: date | None = None) -> int:
        """ECTS, die laut Plan bis zum Stichtag erreicht sein sollen (Ziel 1).

        Plan: ein Modul pro Monat. Gezählt werden die Kalendermonate seit dem
        Beginnmonat. Ohne Angabe gilt das heutige Datum.
        """
        stichtag = stichtag or date.today()
        monate = (stichtag.year - self.__beginn.year) * 12 + stichtag.month - self.__beginn.month
        monate = max(0, monate)
        return min(monate * Modul.STANDARD_ECTS, self.__gesamt_ects)

    def ist_im_zeitplan(self, stichtag: date | None = None) -> bool:
        """True, wenn mindestens so viele ECTS erreicht sind wie geplant (Ziel 1)."""
        return self.get_ects_gesamt_absolviert() >= self.get_soll_ects(stichtag)

    def get_geplanten_abschluss(self) -> date:
        """Geplanter Abschluss: Beginn plus 6 Monate pro Semester (Ziel 1)."""
        monate_gesamt = self.__beginn.month - 1 + len(self.__semester) * 6
        return date(self.__beginn.year + monate_gesamt // 12, monate_gesamt % 12 + 1, 1)

    def get_notenschnitt(self) -> float:
        """Notendurchschnitt über alle bestandenen Module (Ziel 2).

        Gibt 0.0 zurück, solange noch kein Modul bestanden wurde.
        """
        noten = []
        for semester in self.__semester:
            for modul in semester.get_module():
                if modul.get_status() == ModulStatus.BESTANDEN:
                    noten.append(modul.get_note())
        if not noten:
            return 0.0
        return round(sum(noten) / len(noten), 2)

    def get_aktuelles_semester(self):
        """Erstes noch nicht abgeschlossenes Semester (Ziel 3)."""
        for semester in self.__semester:
            if not semester.is_abgeschlossen():
                return semester
        return None  # alle Semester abgeschlossen

    def get_semester_uebersicht(self) -> list:
        """Liste mit Nummer, Status und ECTS pro Semester."""
        uebersicht = []
        for semester in self.__semester:
            status = "abgeschlossen" if semester.is_abgeschlossen() else "laufend"
            uebersicht.append((semester.get_nummer(), status, semester.get_ects_absolviert()))
        return uebersicht

    def suche_module(self, suchtext: str) -> list:
        """Sucht Module, deren Name den Suchtext enthält.

        Groß- und Kleinschreibung wird ignoriert. Bei leerem Suchtext
        wird eine leere Liste zurückgegeben.
        """
        suchtext = suchtext.strip().lower()
        if not suchtext:
            return []
        treffer = []
        for semester in self.__semester:
            for modul in semester.get_module():
                if suchtext in modul.get_name().lower():
                    treffer.append(modul)
        return treffer

    def __str__(self) -> str:
        aktuelles = self.get_aktuelles_semester()
        semester_info = f"Semester {aktuelles.get_nummer()}" if aktuelles else "Studium abgeschlossen"
        return (f"Studiengang: {self.__name}\n"
                f"Fortschritt: {self.get_fortschritt()}% "
                f"({self.get_ects_gesamt_absolviert()}/{self.__gesamt_ects} ECTS)\n"
                f"Notendurchschnitt: {self.get_notenschnitt()}\n"
                f"Aktuell: {semester_info}")