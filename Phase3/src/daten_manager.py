import json
from modul import Modul
from pruefungsleistung import Pruefungsart
from semester import Semester
from studiengang import Studiengang


class DatenManager:
    """Speichert und lädt einen Studiengang in/aus einer JSON-Datei.

    Beziehung zu Studiengang: Abhängigkeit. Der DatenManager arbeitet
    mit einem Studiengang-Objekt, besitzt es aber nicht.
    """

    def __init__(self, dateipfad: str):
        self.__dateipfad = dateipfad

    def speichere_daten(self, studiengang: Studiengang) -> None:
        """Wandelt den Studiengang in ein Dictionary um und speichert es als JSON."""
        daten = {
            "name": studiengang.get_name(),
            "semester": []
        }

        for semester in studiengang.get_semester():
            semester_daten = {
                "nummer": semester.get_nummer(),
                "module": []
            }
            for modul in semester.get_module():
                modul_daten = {
                    "name": modul.get_name(),
                    "ects": modul.get_ects(),
                    "pruefungsart": modul.get_pruefungsart().name,
                    "note": modul.get_note(),
                    "datum": modul.get_datum()
                }
                semester_daten["module"].append(modul_daten)
            daten["semester"].append(semester_daten)

        with open(self.__dateipfad, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, indent=2, ensure_ascii=False)

    def lade_daten(self) -> Studiengang:
        """Liest die JSON-Datei und baut daraus die Objektstruktur auf."""
        with open(self.__dateipfad, "r", encoding="utf-8") as datei:
            daten = json.load(datei)

        studiengang = Studiengang(daten["name"])

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