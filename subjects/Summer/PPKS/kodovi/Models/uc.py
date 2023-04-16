import math
import pickle

class Ucenik:
    def __init__(self, ime_ucenika):
        self.ime_ucenika = ime_ucenika
        self.predmeti = {}

    def unesi_ocjenu(self, ocjena, predmet, datum_unosa):
        if predmet not in self.predmeti:
            self.predmeti[predmet] = []
        self.predmeti[predmet].append({"ocjena": ocjena, "datum_unosa": datum_unosa})

    def prosjek_predmet(self, predmet):
        if predmet not in self.predmeti:
            return 0
        ukupni_zbroj_ocjena = sum(entry["ocjena"] for entry in self.predmeti[predmet])
        return ukupni_zbroj_ocjena / len(self.predmeti[predmet])

    def predmeti_rank(self):
        lista_predmeta = list(self.predmeti.keys())
        lista_predmeta.sort(key=lambda predmet: self.prosjek_predmet(predmet), reverse=True)
        return lista_predmeta

    def globalni_prosjek(self):
        prosjek_zbroja_predmeta = 0
        broj_predmeta = 0
        broj_svih_ocjena = 0
        zbroj_svih_ocjena = 0

        for predmet, entries in self.predmeti.items():
            prosjek_zbroja_predmeta += self.prosjek_predmet(predmet)
            broj_predmeta += 1
            for entry in entries:
                zbroj_svih_ocjena += entry["ocjena"]
                broj_svih_ocjena += 1
        prosjek_po_predmetu = prosjek_zbroja_predmeta / broj_predmeta if broj_predmeta > 0 else 0
        prosjek_svih_ocjena = zbroj_svih_ocjena / broj_svih_ocjena if broj_svih_ocjena > 0 else 0

        return prosjek_po_predmetu, prosjek_svih_ocjena
class Ucenik:
    def __init__(self, ime_ucenika):
        self.ime_ucenika = ime_ucenika
        self.predmeti = {}

    def unesi_ocjenu(self, ocjena, predmet, datum_unosa):
        if predmet not in self.predmeti:
            self.predmeti[predmet] = []
        self.predmeti[predmet].append({"ocjena": ocjena, "datum_unosa": datum_unosa})

    def prosjek_predmet(self, predmet):
        if predmet not in self.predmeti:
            return 0
        ukupni_zbroj_ocjena = sum(entry["ocjena"] for entry in self.predmeti[predmet])
        return ukupni_zbroj_ocjena / len(self.predmeti[predmet])

    def predmeti_rank(self):
        lista_predmeta = list(self.predmeti.keys())
        lista_predmeta.sort(key=lambda predmet: self.prosjek_predmet(predmet), reverse=True)
        return lista_predmeta

    def globalni_prosjek(self):
        prosjek_zbroja_predmeta = 0
        broj_predmeta = 0
        broj_svih_ocjena = 0
        zbroj_svih_ocjena = 0

        for predmet, entries in self.predmeti.items():
            prosjek_zbroja_predmeta += self.prosjek_predmet(predmet)
            broj_predmeta += 1
            for entry in entries:
                zbroj_svih_ocjena += entry["ocjena"]
                broj_svih_ocjena += 1
        prosjek_po_predmetu = prosjek_zbroja_predmeta / broj_predmeta if broj_predmeta > 0 else 0
        prosjek_svih_ocjena = zbroj_svih_ocjena / broj_svih_ocjena if broj_svih_ocjena > 0 else 0

        return prosjek_po_predmetu, prosjek_svih_ocjena


class UcenikPlus(Ucenik):
    def __init__(self, ime_ucenika):
        super().__init__(ime_ucenika)

    def prosjek_predmet(self, predmet):
        klasicni_prosjek = super().prosjek_predmet(predmet)
        zaokruzeni_prosjek = math.ceil(klasicni_prosjek)
        return zaokruzeni_prosjek

    def globalni_prosjek(self):
        p1, p2 = super().globalni_prosjek()
        return math.ceil(p1), math.ceil(p2)




class Razred:
    def __init__(self, ime_razreda, lista_ucenika):
        self.ime_razreda = ime_razreda
        self.lista_ucenika = lista_ucenika

    def ucenici_rank(self, predmet):
        return sorted(self.lista_ucenika, key=lambda ucenik: ucenik.prosjek_predmet(predmet), reverse=True)

    def save(self, file_path):
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    def load(cls, file_path):
        with open(file_path, "rb") as file:
            return pickle.load(file)