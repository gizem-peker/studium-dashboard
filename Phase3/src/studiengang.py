from semester import Semester


class Studiengang:
    """Repräsentiert den gesamten Studiengang mit allen Semestern.

    Beziehung zu Semester: Komposition. Die Semester werden im
    Studiengang verwaltet und existieren nicht unabhängig davon.
    """

    def __init__(self, name: str, gesamt_ects: int = 180):
        self.__name = name
        self.__gesamt_ects = gesamt_ects
        self.__semester = []

    def get_name(self) -> str:
        return self.__name

    def semester_hinzufuegen(self, semester: Semester) -> None:
        self.__semester.append(semester)

    def get_semester(self) -> list:
        return self.__semester

    def get_ects_gesamt_absolviert(self) -> int:
        return sum(s.get_ects_absolviert() for s in self.__semester)

    def get_fortschritt(self) -> float:
        """Gibt den prozentualen ECTS-Fortschritt zurück (Ziel 1: Zeitplan)."""
        return round(self.get_ects_gesamt_absolviert() / self.__gesamt_ects * 100, 1)

    def get_notenschnitt(self) -> float:
        """Berechnet den Notendurchschnitt über alle bestandenen Module (Ziel 2)."""
        noten = []
        for semester in self.__semester:
            for modul in semester.get_module():
                if modul.get_status() == "bestanden":
                    noten.append(modul.get_note())
        if not noten:
            return 0.0
        return round(sum(noten) / len(noten), 2)

    def get_aktuelles_semester(self):
        """Gibt das erste noch nicht abgeschlossene Semester zurück (Ziel 3: Zeitplan)."""
        for semester in self.__semester:
            if not semester.is_abgeschlossen():
                return semester
        return None

    def get_semester_uebersicht(self) -> list:
        """Gibt eine Liste mit Status pro Semester zurück, z.B. für die Anzeige."""
        uebersicht = []
        for semester in self.__semester:
            status = "abgeschlossen" if semester.is_abgeschlossen() else "laufend"
            uebersicht.append((semester.get_nummer(), status, semester.get_ects_absolviert()))
        return uebersicht

    def __str__(self) -> str:
        aktuelles = self.get_aktuelles_semester()
        semester_info = f"Semester {aktuelles.get_nummer()}" if aktuelles else "Studium abgeschlossen"
        return (f"Studiengang: {self.__name}\n"
                f"Fortschritt: {self.get_fortschritt()}% "
                f"({self.get_ects_gesamt_absolviert()}/{self.__gesamt_ects} ECTS)\n"
                f"Notendurchschnitt: {self.get_notenschnitt()}\n"
                f"Aktuell: {semester_info}")