from dozent import Dozent
from pruefungsleistung import Pruefungsleistung


class Modul:
    """Repräsentiert ein Modul innerhalb eines Semesters.

    Beziehungen:
    - Komposition zu Pruefungsleistung: Die Prüfungsleistung wird im
      Modul selbst verwaltet und existiert nicht unabhängig davon.
    - Aggregation zu Dozent: Der Dozent wird von außen übergeben und
      existiert unabhängig vom Modul weiter.
    """

    def __init__(self, name: str, dozent: Dozent, ects: int = 5):
        self.__name = name
        self.__ects = ects
        self.__dozent = dozent
        self.__pruefung = None

    def get_name(self) -> str:
        return self.__name

    def get_ects(self) -> int:
        return self.__ects

    def get_dozent(self) -> Dozent:
        return self.__dozent

    def pruefung_eintragen(self, pruefung: Pruefungsleistung) -> None:
        self.__pruefung = pruefung

    def hat_pruefung(self) -> bool:
        return self.__pruefung is not None

    def get_status(self) -> str:
        if not self.hat_pruefung():
            return "offen"
        return "bestanden" if self.__pruefung.berechne_ergebnis() else "nicht bestanden"

    def get_note(self):
        if self.hat_pruefung():
            return self.__pruefung.get_note()
        return None

    def __str__(self) -> str:
        return f"{self.__name} ({self.__ects} ECTS) - {self.get_status()} - Dozent: {self.__dozent.get_name()}"