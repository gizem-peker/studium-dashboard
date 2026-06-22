class Dozent:
    """Repräsentiert einen Dozenten, der ein oder mehrere Module unterrichtet.

    Beziehung zu Modul: Aggregation.
    Ein Dozent existiert unabhängig von einem konkreten Modul und kann
    mehrere Module unterrichten oder auch ganz ohne zugewiesenes Modul
    existieren (z. B. neu eingestellt, noch kein Modul zugeteilt).
    """

    def __init__(self, name: str):
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def __str__(self) -> str:
        return f"Dozent: {self.__name}"