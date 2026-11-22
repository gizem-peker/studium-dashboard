import os
from application import Application

# Die Datendatei liegt neben dieser Datei, egal von wo das Programm gestartet wird.
dateipfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meine_daten.json")

Application(dateipfad).starten()
