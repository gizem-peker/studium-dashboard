import json
from dozent import Dozent
from modul import Modul
from pruefungsleistung import Klausur
from semester import Semester
from studiengang import Studiengang


class DatenManager:
    """Speichert und lädt einen Studiengang in/aus einer JSON-Datei.

    Beziehung zu Studiengang: Abhängigkeit. Der DatenManager arbeitet
    mit einem Studiengang-Objekt, besitzt es aber nicht.
    """

    def __init__(self, dateipfad: str):
        self.__dateipfad = dateipfad

    def speichere_daten(self, studiengang) -> None:
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
                    "dozent": modul.get_dozent().get_name(),
                    "note": modul.get_note()
                }
                semester_daten["module"].append(modul_daten)
            daten["semester"].append(semester_daten)

        with open(self.__dateipfad, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, indent=2, ensure_ascii=False)
        print(f"Daten gespeichert in {self.__dateipfad}")

    def lade_daten(self):
        """Liest die JSON-Datei und baut daraus die Objektstruktur wieder auf."""
        with open(self.__dateipfad, "r", encoding="utf-8") as datei:
            daten = json.load(datei)

        studiengang = Studiengang(daten["name"])

        for semester_daten in daten["semester"]:
            semester = Semester(semester_daten["nummer"])
            for modul_daten in semester_daten["module"]:
                dozent = Dozent(modul_daten["dozent"])
                modul = Modul(modul_daten["name"], dozent, modul_daten["ects"])
                if modul_daten["note"] is not None:
                    modul.pruefung_eintragen(Klausur(modul_daten["note"]))
                semester.modul_hinzufuegen(modul)
            studiengang.semester_hinzufuegen(semester)

        return studiengang