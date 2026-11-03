from modul import Modul, ModulStatus


class Semester:
    """Ein Semester mit mehreren Modulen.

    Beziehung zu Modul: Komposition. Die Module werden im Semester
    verwaltet und existieren nicht unabhängig davon.
    """

    def __init__(self, nummer: int, ects_ziel: int = 30):
        self.__nummer = nummer
        self.__ects_ziel = ects_ziel
        self.__module = []

    def get_nummer(self) -> int:
        return self.__nummer

    def modul_hinzufuegen(self, modul: Modul) -> None:
        self.__module.append(modul)

    def get_module(self) -> list:
        return self.__module

    def get_ects_ziel(self) -> int:
        return self.__ects_ziel

    def get_geplante_module(self) -> int:
        """Anzahl der Module, die im Semester geplant sind (ECTS-Ziel / ECTS pro Modul)."""
        return self.__ects_ziel // Modul.STANDARD_ECTS

    def get_bestandene_module(self) -> int:
        """Anzahl der bereits bestandenen Module im Semester (Ziel 3)."""
        return sum(1 for m in self.__module if m.get_status() == ModulStatus.BESTANDEN)

    def get_ects_absolviert(self) -> int:
        """Summiert die ECTS aller bestandenen Module."""
        return sum(m.get_ects() for m in self.__module
                   if m.get_status() == ModulStatus.BESTANDEN)

    def is_abgeschlossen(self) -> bool:
        return self.get_ects_absolviert() >= self.__ects_ziel

    def __str__(self) -> str:
        return f"Semester {self.__nummer}: {self.get_ects_absolviert()}/{self.__ects_ziel} ECTS"