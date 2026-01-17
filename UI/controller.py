import flet as ft
from UI.view import View
from database.dao import DAO
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.map={}

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        self.map=self._model.load_map(self.anno_selezionato)
        self._model.costruisci_grafo(self.anno_selezionato)

    def gestisci_selezione_squadra(self,e):
        valore = e.control.value
        self.squadra_selezionata = int(valore)

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""

        vicini=self._model.squadre_adiacenti(self.squadra_selezionata)
        self._view.txt_risultato.controls.clear()
        for v in vicini:
            print(f"{self.map[v[0]].team_code}({self.map[v[0]].name})--peso:{self.map[v[0]].salaryTot}")
            self._view.txt_risultato.controls.append(ft.Text(f"{self.map[v[0]].team_code}({self.map[v[0]].name})--peso:{self.map[v[0]].salaryTot}"))
        self._view.update()


    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        print("chiamo ricorsione")
        cammino=self._model.get_cammino(self.squadra_selezionata)
        self._view.txt_risultato.controls.clear()
        peso=self._model.calcola_peso(cammino)
        for v in range(len(cammino)):
            i=v+1
            id1=cammino[v][0]
            id2=cammino[i][0]
            self._view.txt_risultato.controls.append(ft.Text(f"{self.map[id1].team_code}({self.map[id1].name})-->{self.map[id2].team_code}({self.map[id2].name})--peso:{peso}"))
        self._view.update()

    """ Altri possibili metodi per gestire di dd_anno """""

    def get_selected_anno(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """
        valore = e.control.value
        self.anno_selezionato = int(valore)
        self.squadre = self._model.get_squadre(self.anno_selezionato)
        num_squadre=len(self.squadre)
        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"numero squadre: {num_squadre}"))
        for s in self.squadre:
           self._view.txt_out_squadre.controls.append(ft.Text(f" {s.team_code}({s.name})"))
        self._view.update()
        self.popola_dd_squadre()



    def popola_dd(self):
        self.anni = self._model.get_anni()
        for a in self.anni:
            self._view.dd_anno.options.append(ft.dropdown.Option(text=a))
        self._view.update()

    def popola_dd_squadre(self):
        for s in self.squadre:
            self._view.dd_squadra.options.append(ft.dropdown.Option(key=s.id,text=s.team_code))
        self._view.update()