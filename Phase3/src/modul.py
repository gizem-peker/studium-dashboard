from datetime import date
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

    def __init__(self, name: str, pruefungsart: Pruefungsart, ects: int = STANDARD_ECTS,
                 note: float | None = None, datum: date | None = None):
        self._name = name
        self._ects = ects
        # Komposition: die Prüfungsleistung entsteht zusammen mit dem Modul
        self._pruefungsleistung = Pruefungsleistung(pruefungsart, note, datum)

    @property
    def name(self) -> str:
        return self._name

    @property
    def ects(self) -> int:
        return self._ects

    # Die folgenden drei Properties reichen Werte der Prüfungsleistung weiter,
    # damit man von außen nicht über zwei Objekte gehen muss.
    @property
    def pruefungsart(self) -> Pruefungsart:
        return self._pruefungsleistung.pruefungsart

    @property
    def note(self) -> float | None:
        return self._pruefungsleistung.note

    @property
    def datum(self) -> date | None:
        return self._pruefungsleistung.datum

    def ermittle_status(self) -> ModulStatus:
        """Leitet den Status aus der Prüfungsleistung ab."""
        if self.note is None:
            return ModulStatus.OFFEN
        if self._pruefungsleistung.ist_bestanden():
            return ModulStatus.BESTANDEN
        return ModulStatus.NICHT_BESTANDEN
