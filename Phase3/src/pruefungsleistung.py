from abc import ABC, abstractmethod


class Pruefungsleistung(ABC):
    """Abstrakte Basisklasse für alle Prüfungsleistungen.

    Es wird bewusst keine direkte Instanz dieser Klasse erzeugt,
    da es in der Realität keine 'allgemeine' Prüfung gibt -
    jede Prüfung ist konkret entweder eine Klausur oder eine Projektarbeit.
    """

    def __init__(self, note: float):
        self.__note = note

    def get_note(self) -> float:
        return self.__note

    @abstractmethod
    def berechne_ergebnis(self) -> bool:
        """Muss von jeder Unterklasse implementiert werden."""
        pass

    def __str__(self) -> str:
        status = "bestanden" if self.berechne_ergebnis() else "nicht bestanden"
        return f"Note: {self.__note} ({status})"


class Klausur(Pruefungsleistung):
    """Konkrete Prüfungsleistung: Klausur, optional mit Prüfungsdatum."""

    def __init__(self, note: float, pruefungsdatum: str = None):
        super().__init__(note)
        self.__pruefungsdatum = pruefungsdatum

    def get_pruefungsdatum(self) -> str | None:
        return self.__pruefungsdatum

    def berechne_ergebnis(self) -> bool:
        return self.get_note() <= 4.0


class Projektarbeit(Pruefungsleistung):
    """Konkrete Prüfungsleistung: Projektarbeit, optional mit Abgabedatum."""

    def __init__(self, note: float, abgabedatum: str = None):
        super().__init__(note)
        self.__abgabedatum = abgabedatum

    def get_abgabedatum(self) -> str | None:
        return self.__abgabedatum

    def berechne_ergebnis(self) -> bool:
        return self.get_note() <= 4.0