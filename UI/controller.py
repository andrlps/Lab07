import flet as ft

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.clean()
        self._mese = self._view.dd_mese.value
        valori = self._model.get_umidita_media(self._mese)
        self._view.lst_result.controls.append(
            ft.Text("Umidità media nel mese selezionato:"))
        i = 0
        for value in valori:
            self._view.lst_result.controls.append(
                ft.Text(f"{value['Localita']}: {value['avg(Umidita)']}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        self._view.lst_result.clean()
        self._mese = self._view.dd_mese.value
        valori = self._model.calcola_sequenza(self._mese)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo: {valori[1]}"))
        for risultato in valori[0]:
            self._view.lst_result.controls.append(ft.Text(f"[{risultato.localita} {risultato.data}] Umidità: {risultato.umidita}"))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)