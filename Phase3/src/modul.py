from enum import Enum
from pruefungsleistung import Pruefungsart, Pruefungsleistung


class ModulStatus(Enum):
    """Mögliche Zustände eines Moduls (Enumeration)."""

    OFFEN = "offen"
    BESTANDEN = "bestanden"
    NICHT_BESTANDEN = "nicht bestanden"


class Modul:
    """Ein Modul innerhalb eines Semesters.

    Beziehung zu Pruefungsleistung: Komposition (1 zu 1). Die Prüfungs-
    leistung wird hier im Konstruktor erzeugt und gehört fest zum Modul.
    """

    STANDARD_ECTS = 5  # Ein Modul hat im Studium in der Regel 5 ECTS

    def __init__(self, name: str, pruefungsart: Pruefungsart, ects: int = 5,
                 note: float | None = None, datum: str | None = None):
        self.__name = name
        self.__ects = ects
        # Komposition: die Prüfungsleistung entsteht zusammen mit dem Modul
        self.__pruefungsleistung = Pruefungsleistung(pruefungsart, note, datum)

    def get_name(self) -> str:
        return self.__name

    def get_ects(self) -> int:
        return self.__ects

    def get_pruefungsart(self) -> Pruefungsart:
        return self.__pruefungsleistung.get_pruefungsart()

    def get_note(self) -> float | None:
        return self.__pruefungsleistung.get_note()

    def get_datum(self) -> str | None:
        return self.__pruefungsleistung.get_datum()

    def get_status(self) -> ModulStatus:
        """Leitet den Status aus der Prüfungsleistung ab."""
        if self.get_note() is None:
            return ModulStatus.OFFEN
        if self.__pruefungsleistung.ist_bestanden():
            return ModulStatus.BESTANDEN
        return ModulStatus.NICHT_BESTANDEN