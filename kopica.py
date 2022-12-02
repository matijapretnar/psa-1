from dataclasses import dataclass
from typing import List, TypeVar

V = TypeVar("V")

@dataclass
class MinKopica:
    _elementi: List[V]

    def __getitem__(self, i):
        return self._elementi[i]

    def __setitem__(self, i, x):
        self._elementi[i] = x

    def _zamenjaj(self, i, j):
        self[i], self[j] = self[j], self[i]

    def _indeks_starsa(self, i):
        if i > 0:
            return (i - 1) // 2
    
    def _indeks_levega_otroka(self, i):
        if 2 * i + 1 < len(self._elementi):
            return 2 * i + 1

    def _indeks_desnega_otroka(self, i):
        if 2 * i + 2 < len(self._elementi):
            return 2 * i + 2

    def _dvigni(self, i):
        i_stars = self._indeks_starsa(i)
        if i_stars is not None and self[i] < self[i_stars]:
            self._zamenjaj(i, i_stars)
            self._dvigni(i_stars)

    def _potopi(self, i):
        i_levi = self._indeks_levega_otroka(i)
        i_desni = self._indeks_desnega_otroka(i)
        if i_levi and i_desni and self[i] > self[i_desni] and self[i_levi] > self[i_desni]:
            # potopimo desno
            self._zamenjaj(i, i_desni)
            self._potopi(i_desni)
        elif i_levi and self[i] > self[i_levi]:
            # potopimo levo
            self._zamenjaj(i, i_levi)
            self._potopi(i_levi)

    def vstavi(self, x):
        self._elementi.append(x)
        self._dvigni(len(self._elementi) - 1)
    
    def odstrani_min(self):
        m = self[0]
        zadnji = self._elementi.pop()
        if self._elementi:
            self[0] = zadnji
            self._potopi(0)
        return m

    @classmethod
    def uredi(cls, sez):
        k = cls([])
        for x in sez:
            k.vstavi(x)
        urejen = []
        for _ in range(len(sez)):
            urejen.append(k.odstrani_min())
        return urejen
