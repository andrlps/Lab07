import copy

from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        self.costoOttimo = -1
        self.percorsoOttimo = []
        self.n_soluzioni = 0

    def get_umidita_media(self, mese):
        return MeteoDao.get_umidita_media(mese)

    def get_all_situazioni(self, mese):
        return MeteoDao.get_all_situazioni(mese)

    # mia soluzione
    def calcola_sequenza_ottima_mia(self, mese):
        sequenza = {'Torino': [], 'Milano': [], 'Genova':[]}
        mappa = {'Torino': 0, 'Milano': 0, 'Genova': 0}
        for el in self.get_all_situazioni(mese):
            sequenza[el.localita].append(el)
        self._ricorsione_mia([], None, sequenza, mappa, 0)

    def _ricorsione_mia(self, percorso, citta, sequenza, mappa, costo):
        if len(percorso) == 15 or costo > self.costoOttimo:
            print(costo)
            if costo < self.costoOttimo:
                self.costoOttimo = costo
                self.percorsoOttimo = percorso
        else:
            for i in range (len(percorso), 15):
                for city in ['Torino', 'Milano', 'Genova']:
                    if i == 0:
                        nuova_citta = city
                        mappa[nuova_citta] += 3
                        nuovo_costo = 0
                        for giorno in range(3):
                            percorso.append(sequenza[nuova_citta][giorno])
                            nuovo_costo += sequenza[nuova_citta][giorno].umidita
                        self._ricorsione_mia(percorso, nuova_citta, sequenza, mappa, nuovo_costo)
                        percorso = []
                        mappa[nuova_citta] -= 3
                    else:
                        if mappa[city] == 6:
                            continue
                        else:
                            if citta == city:
                                nuova_citta = city
                                nuovo_costo = costo + sequenza[nuova_citta][i].umidita
                                mappa[nuova_citta] += 1
                                percorso.append(sequenza[nuova_citta][i])
                                self._ricorsione_mia(percorso, nuova_citta, sequenza, mappa, nuovo_costo)
                                percorso.pop()
                                mappa[nuova_citta] -= 1
                            else:
                                aggiunti = 0
                                nuovo_costo = 100+costo
                                nuova_citta = city
                                for giorno in range(3):
                                    if len(percorso) == 7:
                                        break
                                    percorso.append(sequenza[nuova_citta][giorno])
                                    nuovo_costo += sequenza[nuova_citta][i].umidita
                                    aggiunti += 1
                                mappa[nuova_citta] += aggiunti
                                self._ricorsione_mia(percorso, nuova_citta, sequenza, mappa, nuovo_costo)
                                for val in range(aggiunti):
                                    percorso.pop()
                                mappa[nuova_citta] -= aggiunti

    # soluzione vista in aula
    def calcola_sequenza(self, mese):
        self.costoOttimo = -1
        self.percorsoOttimo = []
        self.n_soluzioni = 0
        situazioni = MeteoDao.get_all_situazioni(mese)
        self._ricorsione([], situazioni)
        return (self.percorsoOttimo, self.costoOttimo)

    def trova_possibili_step(self, parziale, lista_situazioni):
        giorno = len(parziale)+1
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati

    def is_admissible(self, candidate, parziale):
        # vincolo su 6 giorni
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidate.localita:
                counter += 1
        if counter >= 6:
            return False

        # vincolo sulla permanenza
        # 1) lunghezza di paziale < 3
        if len(parziale) == 0:
            return True
        if len(parziale) < 3:
            if candidate.localita != parziale[0].localita:
                return False

        # 2) le tre situazioni precedenti non sono tutte uguali
        else:
            if (parziale[-1].localita != parziale[-2].localita or
                parziale[-1].localita != parziale[-3].localita or
                parziale[-2].localita != parziale[-3].localita):
                if parziale[-1].localita != candidate.localita:
                    return False

        # ok
        return True

    def calcola_costo(self, parziale):
        costo = 0
        # 1) costo umidita
        for situazione in parziale:
            costo += situazione.umidita

        # 2) costo spostamento
        for i in range(len(parziale)):
            # se i due giorni precedenti non sono stato nella stessa citta in cui sono ora pago 100
            if i >= 2 and parziale[i-1].localita != parziale[i].localita or parziale[2].localita != parziale[i].localita:
                costo += 100

        return costo

    def _ricorsione(self, parziale, lista_situazioni):
        if len(parziale) == 15:
            self.n_soluzioni += 1
            costo = self.calcola_costo(parziale)
            if self.costoOttimo == -1 or costo < self.costoOttimo:
                self.costoOttimo = costo
                self.percorsoOttimo = copy.deepcopy(parziale)
        else:
            # cercare le città per il giorno che mi serve
            candidates = self.trova_possibili_step(parziale, lista_situazioni)
            # provo ad aggiungere una di queste città e vado avanti
            for candidate in candidates:
                # verifica_vincoli
                if self.is_admissible(candidate, parziale):
                    parziale.append(candidate)
                    self._ricorsione(parziale, lista_situazioni)
                    parziale.pop()

if __name__ == '__main__':
    my_model = Model()
    print(my_model.calcola_sequenza(2))