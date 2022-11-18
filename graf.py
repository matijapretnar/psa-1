from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, Set, TypeVar
import networkx as nx
import matplotlib.pyplot as plt
# from deque import Deque

V = TypeVar("V")

@dataclass
class Graf:
    sosedi: Dict[V, Set[V]]
    usmerjen: bool = False

    def obrnjen(self):
        sosedi_obrnjenega = defaultdict(set)
        for u, v in self.povezave():
            sosedi_obrnjenega[v].add(u)
        sosedi_obrnjenega = {u: sosedi_obrnjenega[u] for u in self.vozlisca()}
        return Graf(sosedi_obrnjenega, usmerjen=self.usmerjen)

    def povezave(self):
        for u, vs in self.sosedi.items():
            for v in vs:
                yield u, v

    def vozlisca(self):
        return self.sosedi.keys()

    def narisi(self, oznaka=lambda v: v):
        if self.usmerjen:
            omrezje = nx.DiGraph()
        else:
            omrezje = nx.Graph()
        omrezje.add_nodes_from(self.vozlisca())
        omrezje.add_edges_from(self.povezave())
        oznake = {u: oznaka(u) for u in self.vozlisca()}
        nx.draw_spring(omrezje, labels=oznake)
        plt.show()

    def _razisci(self, v, oznacena, pripravi, pospravi):
        oznacena.add(v)
        pripravi(v)
        for w in self.sosedi[v]:
            if w not in oznacena:
                self._razisci(w, oznacena, pripravi, pospravi)
        pospravi(v)

    def dfs(self, pripravi=lambda u: None, pospravi=lambda u: None, zacni_raziskovanje=lambda u: None):
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
    
    def topoloska_ureditev(self):
        sklad = []
        def pospravi(v):
            sklad.append(v)
        self.dfs(pospravi=pospravi)
        sklad.reverse()
        return sklad
    
    def krepko_povezane_komponente(self):
        obrnjen = self.obrnjen()
        oznacena = set()
        komponente = {}
        indeks_komponente = 0
        for u in obrnjen.topoloska_ureditev():
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
        imena_komponent = {komponenta: "".join(str(vozlisce) for vozlisce in sorted(vozlisca)) for komponenta, vozlisca in vozlisca_komponent.items()}
        sosedi_v_kvocientnem = defaultdict(set)
        for u, v in self.povezave():
            komponenta_u = imena_komponent[komponente_vozlisc[u]]
            komponenta_v = imena_komponent[komponente_vozlisc[v]]
            if komponenta_u != komponenta_v:
                sosedi_v_kvocientnem[komponenta_u].add(komponenta_v)
        return Graf({u: sosedi_v_kvocientnem[u] for u in imena_komponent}, usmerjen=True)
            

    def bfs(self, v):
        oznacena = {v}
        raziskujemo = [v]
        while raziskujemo:
            u = raziskujemo.pop(0)
            print(u)
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

g = Graf({
        "A": {"B", "C", "D"},
        "B": {"A", "E", "F"},
        "C": {"A", "F"},
        "D": {"A", "G", "H"},
        "E": {"B", "I", "J"},
        "F": {"B", "C"},
        "G": {"D", "H"},
        "H": {"D", "G"},
        "I": {"E", "J"},
        "J": {"E", "I"},
        "K": {"L"},
        "L": {"K"}
    }
)

# g.narisi()
komponente = g.komponente_za_povezanost()
pred_oznake, po_oznake = g.pred_in_po_oznake()
# g.narisi(oznaka=komponente.get)
# g.narisi(oznaka=lambda v: f"{v}: {pred_oznake[v]}/{po_oznake[v]}")

u = Graf({
    "A": {"B", "C", "F"},
    "B": {"E"},
    "C": {"D"},
    "D": {"A"},
    "E": {"F", "G", "H"},
    "F": {"B", "G"},
    "G": {},
    "H": {"G"},
}, usmerjen=True)
# u.narisi()
# pred_oznake, po_oznake = u.pred_in_po_oznake()
# u.narisi(oznaka=lambda v: f"{v}: {pred_oznake[v]}/{po_oznake[v]}")

dag = Graf({
    "A": {"C"},
    "B": {"A", "D"},
    "C": {"E", "F"},
    "D": {"C"},
    "E": {},
    "F": {},
}, usmerjen=True)
# print(dag.topoloska_ureditev())
# dag.narisi()

kpk = Graf({
    "A": {"B"},
    "B": {"C", "D", "E"},
    "C": {"F"},
    "D": set(),
    "E": {"B", "F", "G"},
    "F": {"C", "H"},
    "G": {"H", "J"},
    "H": {"K"},
    "I": {"G"},
    "J": {"I"},
    "K": {"L"},
    "L": {"J"},
}, usmerjen=True)
komponente = kpk.krepko_povezane_komponente()
# kpk.narisi(oznaka=lambda v: f"{v}: {komponente[v]}")
# kpk.kvocientni_graf().narisi()

# dag.obrnjen().narisi()

# g.bfs("A")
razdalje = g.razdalje("H")
g.narisi(oznaka=lambda v: razdalje.get(v, "∞"))