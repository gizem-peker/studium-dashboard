from daten_manager import DatenManager
from dashboard_ui import DashboardUI


class Application:
    """Einstiegspunkt des Programms: steuert den Ablauf.

    Die Application lädt mit dem DatenManager den Studiengang und startet
    damit die DashboardUI. Beide Klassen kennen sich nicht gegenseitig.
    Beziehung zu DatenManager und DashboardUI: Abhängigkeit (die Application
    erzeugt und verwendet sie, besitzt sie aber nicht dauerhaft).
    """

    def __init__(self, dateipfad: str):
        self._dateipfad = dateipfad

    def starten(self) -> None:
        """Lädt die Daten und öffnet das Dashboard.

        Ist die Datei fehlerhaft, wird die Meldung ausgegeben und das
        Programm beendet sich, ohne das Fenster zu öffnen.
        """
        try:
            studiengang = DatenManager(self._dateipfad).lade_daten()
        except ValueError as fehler:
            print("Die Daten konnten nicht geladen werden:")
            print(fehler)
            return

        dashboard = DashboardUI(studiengang)
        dashboard.zeige_fortschritt()
        dashboard.zeige_suche()
        dashboard.starten()
