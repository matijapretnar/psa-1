from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, Set, TypeVar
import networkx as nx
import matplotlib.pyplot as plt

V = TypeVar("V")


@dataclass
class Graf:
    sosedi: Dict[V, Set[V]]

    def obrnjen(self):
        sosedi_obrnjenega = defaultdict(set)
        for u, v in self.povezave():
            sosedi_obrnjenega[v].add(u)
        sosedi_obrnjenega = {u: sosedi_obrnjenega[u] for u in self.vozlisca()}
        return type(self)(sosedi_obrnjenega)

    def povezave(self):
        for u, vs in self.sosedi.items():
            for v in vs:
                yield u, v

    def vozlisca(self):
        return self.sosedi.keys()

    def narisi(self, oznaka=lambda v: v):
        omrezje = nx.Graph()
        omrezje.add_nodes_from(self.vozlisca())
        omrezje.add_edges_from(self.povezave())
        oznake = {u: oznaka(u) for u in self.vozlisca()}
        nx.draw_kamada_kawai(omrezje, labels=oznake, node_color="white")
        plt.show()

    def _razisci(self, v, oznacena, pripravi, pospravi):
        oznacena.add(v)
        pripravi(v)
        for w in self.sosedi[v]:
            if w not in oznacena:
                self._razisci(w, oznacena, pripravi, pospravi)
        pospravi(v)

    def dfs(
        self,
        pripravi=lambda u: None,
        pospravi=lambda u: None,
        zacni_raziskovanje=lambda u: None,
    ):
        oznacena = set()
        for v in self.vozlisca():
            if v not in oznacena:
                zacni_raziskovanje(v)
                self._razisci(v, oznacena, pripravi, pospravi)

    def komponente_za_povezanost(self):
        komponente = {}
        stevec_komponent = [0]

        def zacni_raziskovanje(v):
            stevec_komponent[0] += 1

        def pripravi(v):
            komponente[v] = stevec_komponent[0]

        self.dfs(pripravi=pripravi, zacni_raziskovanje=zacni_raziskovanje)
        return komponente

    def pred_in_po_oznake(self):
        pred_oznake = {}
        po_oznake = {}
        korak = [1]

        def pripravi(v):
            pred_oznake[v] = korak[0]
            korak[0] += 1

        def pospravi(v):
            po_oznake[v] = korak[0]
            korak[0] += 1

        self.dfs(pripravi=pripravi, pospravi=pospravi)
        return pred_oznake, po_oznake

    def razisci_z_eksplicitnim_skladom(self, v):
        oznacena = set()
        raziskujemo = [v]
        while raziskujemo:
            u = raziskujemo.pop()
            oznacena.add(u)
            for w in self.sosedi[u]:
                if w not in oznacena:
                    raziskujemo.append(w)
        return oznacena

    def bfs(self, v):
        oznacena = {v}
        raziskujemo = [v]
        while raziskujemo:
            u = raziskujemo.pop(0)
            for w in self.sosedi[u]:
                if w not in oznacena:
                    raziskujemo.append(w)
                    oznacena.add(w)
        return oznacena

    def razdalje(self, v):
        razdalje = {v: 0}
        raziskujemo = [v]
        while raziskujemo:
            u = raziskujemo.pop(0)
            for w in self.sosedi[u]:
                if w not in razdalje:
                    raziskujemo.append(w)
                    razdalje[w] = razdalje[u] + 1
        return razdalje


@dataclass
class UsmerjenGraf(Graf):
    def narisi(self, oznaka=lambda v: v):
        omrezje = nx.DiGraph()
        omrezje.add_nodes_from(self.vozlisca())
        omrezje.add_edges_from(self.povezave())
        oznake = {u: oznaka(u) for u in self.vozlisca()}
        nx.draw_kamada_kawai(omrezje, labels=oznake, node_color="white")
        plt.show()

    def krepko_povezane_komponente(self):
        obrnjen = self.obrnjen()
        oznacena = set()
        komponente = {}
        indeks_komponente = 0
        _, po_oznake = obrnjen.pred_in_po_oznake()
        for u in sorted(self.vozlisca(), key=lambda u: po_oznake[u], reverse=True):
            if u not in oznacena:
                indeks_komponente += 1

                def pripravi(v):
                    komponente[v] = indeks_komponente

                self._razisci(u, oznacena, pripravi=pripravi, pospravi=lambda u: None)
        return komponente

    def kvocientni_graf(self):
        komponente_vozlisc = self.krepko_povezane_komponente()
        vozlisca_komponent = defaultdict(set)
        for vozlisce, komponenta in komponente_vozlisc.items():
            vozlisca_komponent[komponenta].add(vozlisce)
        imena_komponent = {
            komponenta: "".join(str(vozlisce) for vozlisce in sorted(vozlisca))
            for komponenta, vozlisca in vozlisca_komponent.items()
        }
        sosedi_v_kvocientnem = defaultdict(set)
        for u, v in self.povezave():
            komponenta_u = imena_komponent[komponente_vozlisc[u]]
            komponenta_v = imena_komponent[komponente_vozlisc[v]]
            if komponenta_u != komponenta_v:
                sosedi_v_kvocientnem[komponenta_u].add(komponenta_v)
        return DAG({u: sosedi_v_kvocientnem[u] for u in imena_komponent.values()})


class DAG(UsmerjenGraf):
    def topoloska_ureditev(self):
        sklad = []

        def pospravi(v):
            sklad.append(v)

        self.dfs(pospravi=pospravi)
        sklad.reverse()
        return sklad
