from datetime import date
from enum import Enum


class Pruefungsart(Enum):
    """Mögliche Arten einer Prüfungsleistung (Enumeration)."""

    KLAUSUR = "Klausur"
    PROJEKTARBEIT = "Projektarbeit"


class Pruefungsleistung:
    """Prüfungsleistung eines Moduls.

    Beziehung zu Modul: Komposition. Die Prüfungsleistung wird im Modul
    selbst erzeugt und existiert nicht unabhängig davon.

    Note und Datum sind optional: note = None bedeutet, dass die Prüfung
    noch nicht bewertet wurde.
    """

    BESTEHENSGRENZE = 4.0  # Noten bis einschließlich 4,0 gelten als bestanden

    def __init__(self, pruefungsart: Pruefungsart, note: float | None = None,
                 datum: date | None = None):
        # Ein einfacher Unterstrich bedeutet: nur für die Klasse selbst gedacht.
        # Von außen wird über die Properties (nur lesend) zugegriffen.
        self._pruefungsart = pruefungsart
        self._note = note
        self._datum = datum

    @property
    def pruefungsart(self) -> Pruefungsart:
        return self._pruefungsart

    @property
    def note(self) -> float | None:
        return self._note

    @property
    def datum(self) -> date | None:
        return self._datum

    def ist_bestanden(self) -> bool:
        """True, wenn eine Note vorliegt und diese 4,0 oder besser ist."""
        return self._note is not None and self._note <= self.BESTEHENSGRENZE
