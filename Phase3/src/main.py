from daten_manager import DatenManager
from dashboard_ui import DashboardUI

dm = DatenManager("meine_daten.json")
studiengang = dm.lade_daten()

ui = DashboardUI(studiengang)
ui.zeige_fortschritt()
ui.zeige_suche()
ui.starten()