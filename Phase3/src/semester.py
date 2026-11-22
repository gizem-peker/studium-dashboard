from modul import Modul, ModulStatus


class Semester:
    """Ein Semester mit mehreren Modulen.

    Beziehung zu Modul: Komposition. Die Module werden im Semester
    verwaltet und existieren nicht unabhängig davon.
    """

    def __init__(self, nummer: int, ects_ziel: int = 30):
        self._nummer = nummer
        self._ects_ziel = ects_ziel
        self._module = []

    @property
    def nummer(self) -> int:
        return self._nummer

    @property
    def ects_ziel(self) -> int:
        return self._ects_ziel

    @property
    def module(self) -> list:
        """Kopie der Modulliste (so kann von außen nichts hinzugefügt werden)."""
        return list(self._module)

    def modul_hinzufuegen(self, modul: Modul) -> None:
        self._module.append(modul)

    def summiere_ects(self) -> int:
        """Summiert die ECTS aller bestandenen Module."""
        return sum(m.ects for m in self._module
                   if m.ermittle_status() == ModulStatus.BESTANDEN)

    def zaehle_bestandene_module(self) -> int:
        """Anzahl der bereits bestandenen Module im Semester (Ziel 3)."""
        return sum(1 for m in self._module
                   if m.ermittle_status() == ModulStatus.BESTANDEN)

    def berechne_geplante_module(self) -> int:
        """Anzahl der geplanten Module (ECTS-Ziel / ECTS pro Modul)."""
        return self._ects_ziel // Modul.STANDARD_ECTS

    def ist_abgeschlossen(self) -> bool:
        return self.summiere_ects() >= self._ects_ziel
