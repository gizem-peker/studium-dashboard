import json
from datetime import date
from modul import Modul
from pruefungsleistung import Pruefungsart
from semester import Semester
from studiengang import Studiengang


class DatenManager:
    """Lädt einen Studiengang aus einer JSON-Datei.

    Beziehung zu Studiengang: Abhängigkeit. Der DatenManager arbeitet
    mit einem Studiengang-Objekt, besitzt es aber nicht.
    """

    def __init__(self, dateipfad: str):
        self.__dateipfad = dateipfad

    def lade_daten(self) -> Studiengang:
        """Liest die JSON-Datei und baut daraus die Objektstruktur auf."""
        with open(self.__dateipfad, "r", encoding="utf-8") as datei:
            daten = json.load(datei)

        studiengang = Studiengang(daten["name"], self.__lese_beginn(daten))

        for semester_daten in daten["semester"]:
            semester = Semester(semester_daten["nummer"])
            for modul_daten in semester_daten["module"]:
                modul = Modul(
                    name=modul_daten["name"],
                    pruefungsart=self.__lese_pruefungsart(modul_daten),
                    ects=modul_daten.get("ects", 5),
                    note=modul_daten.get("note"),    # fehlt oder null = noch nicht bewertet
                    datum=modul_daten.get("datum")
                )
                semester.modul_hinzufuegen(modul)
            studiengang.semester_hinzufuegen(semester)

        return studiengang

    def __lese_pruefungsart(self, modul_daten: dict) -> Pruefungsart:
        """Wandelt den Text aus der JSON-Datei in eine Pruefungsart um.

        Die JSON-Datei wird von Hand gepflegt, daher gibt es bei einem
        Tippfehler eine verständliche Fehlermeldung.
        """
        try:
            return Pruefungsart[modul_daten["pruefungsart"]]
        except KeyError:
            raise ValueError(
                f"Ungültige Prüfungsart bei Modul '{modul_daten.get('name')}'. "
                f"Erlaubt sind: KLAUSUR oder PROJEKTARBEIT."
            )

    def __lese_beginn(self, daten: dict) -> date:
        """Liest den Studienbeginn (Format JJJJ-MM-TT) aus der JSON-Datei."""
        try:
            return date.fromisoformat(daten["beginn"])
        except (KeyError, TypeError, ValueError):
            raise ValueError(
                'Ungültiger oder fehlender Studienbeginn. Erwartet wird ein Eintrag '
                'wie "beginn": "2026-03-01" (Format JJJJ-MM-TT).'
            )