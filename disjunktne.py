from dataclasses import dataclass
from typing import Iterable, TypeVar, Dict

Val = TypeVar("Val")


@dataclass
class _Vozlisce:
    rang: int
    stars: Val


@dataclass
class DisjunktneMnozice:
    _vozlisca: Dict[Val, _Vozlisce]
    kompresija: bool = True

    @classmethod
    def singletoni(cls, sez: Iterable[Val]):
        return cls(_vozlisca={x: _Vozlisce(rang=0, stars=x) for x in sez})

    def _rang(self, x):
        return self._vozlisca[x].rang

    def _stars(self, x):
        return self._vozlisca[x].stars

    def _poisci_s_kompresijo(self, x: Val):
        vozlisce = self._vozlisca[x]
        if vozlisce.stars != x:
            vozlisce.stars = self._poisci_s_kompresijo(vozlisce.stars)
        return vozlisce.stars

    def _poisci_brez_kompresije(self, x: Val):
        vozlisce = self._vozlisca[x]
        if vozlisce.stars != x:
            return self.poisci(vozlisce.stars)
        else:
            return x

    def poisci(self, x):
        if self.kompresija:
            return self._poisci_s_kompresijo(x)
        else:
            return self._poisci_brez_kompresije(x)

    def zdruzi(self, x, y):
        p_x = self.poisci(x)
        p_y = self.poisci(y)
        if p_x != p_y:
            if self._rang(p_x) < self._rang(p_y):
                self._vozlisca[p_x].stars = p_y
            elif self._rang(p_x) > self._rang(p_y):
                self._vozlisca[p_y].stars = p_x
            else:
                assert self._rang(p_x) == self._rang(p_y)
                self._vozlisca[p_y].stars = p_x
                self._vozlisca[p_x].rang += 1
