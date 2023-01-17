from dataclasses import dataclass
from typing import List, TypeVar

Val = TypeVar("Val")
Index = int


@dataclass
class Kopica:
    _elementi: List[Val]

    def __getitem__(self, i: Index) -> Val:
        return self._elementi[i]

    def __setitem__(self, i: Index, x: Val) -> None:
        self._elementi[i] = x

    def _zamenjaj(self, i: Index, j: Index) -> None:
        self[i], self[j] = self[j], self[i]

    def _indeks_starsa(self, i: Index) -> (Index | None):
        if i > 0:
            return (i - 1) // 2

    def _indeks_levega_otroka(self, i: Index) -> (Index | None):
        if 2 * i + 1 < len(self._elementi):
            return 2 * i + 1

    def _indeks_desnega_otroka(self, i: Index) -> (Index | None):
        if 2 * i + 2 < len(self._elementi):
            return 2 * i + 2

    def _dvigni(self, i: Index) -> None:
        i_stars = self._indeks_starsa(i)
        if i_stars is not None and self._mora_biti_visje(i, i_stars):
            self._zamenjaj(i, i_stars)
            self._dvigni(i_stars)

    def _potopi(self, i: Index) -> None:
        i_levi = self._indeks_levega_otroka(i)
        i_desni = self._indeks_desnega_otroka(i)
        if (
            i_levi
            and i_desni
            and self._mora_biti_visje(i_desni, i)
            and self._mora_biti_visje(i_desni, i_levi)
        ):
            # potopimo desno
            self._zamenjaj(i, i_desni)
            self._potopi(i_desni)
        elif i_levi and self._mora_biti_visje(i_levi, i):
            # potopimo levo
            self._zamenjaj(i, i_levi)
            self._potopi(i_levi)

    def vstavi(self, x: Val) -> None:
        self._elementi.append(x)
        self._dvigni(len(self._elementi) - 1)

    def odstrani_vrh(self) -> None:
        m = self[0]
        zadnji = self._elementi.pop()
        if self._elementi:
            self[0] = zadnji
            self._potopi(0)
        return m


@dataclass
class MinKopica(Kopica):
    def _mora_biti_visje(self, i: Index, j: Index) -> bool:
        return self[i] < self[j]

    @classmethod
    def uredi(cls, sez: List[Val]) -> List[Val]:
        k = cls([])
        for x in sez:
            k.vstavi(x)
        urejen = []
        for _ in range(len(sez)):
            urejen.append(k.odstrani_vrh())
        return urejen


@dataclass
class MaxKopica(Kopica):
    def _mora_biti_visje(self, i: Index, j: Index) -> bool:
        return self[i] > self[j]
