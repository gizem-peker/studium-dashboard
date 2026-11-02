from enum import Enum


class Pruefungsart(Enum):
    """Mögliche Arten einer Prüfungsleistung (Enumeration)."""

    KLAUSUR = "Klausur"
    PROJEKTARBEIT = "Projektarbeit"


class Pruefungsleistung:
    """Prüfungsleistung eines Moduls.

    Beziehung zu Modul: Komposition. Die Prüfungsleistung wird im Modul
    selbst erzeugt und existiert nicht unabhängig davon.

    Eine Note ist nicht immer sofort vorhanden: note = None bedeutet,
    dass die Prüfung noch nicht bewertet wurde.
    """

    BESTEHENSGRENZE = 4.0  # Noten bis einschließlich 4,0 gelten als bestanden

    def __init__(self, pruefungsart: Pruefungsart, note: float | None = None,
                 datum: str | None = None):
        self.__pruefungsart = pruefungsart
        self.__note = note
        self.__datum = datum  # Format JJJJ-MM-TT, z. B. "2026-05-10"

    def get_pruefungsart(self) -> Pruefungsart:
        return self.__pruefungsart

    def get_note(self) -> float | None:
        return self.__note

    def get_datum(self) -> str | None:
        return self.__datum

    def ist_bestanden(self) -> bool:
        """True, wenn eine Note vorliegt und diese 4,0 oder besser ist."""
        return self.__note is not None and self.__note <= self.BESTEHENSGRENZE