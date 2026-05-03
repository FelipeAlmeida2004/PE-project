import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from typing import List, Optional

matplotlib.use("Agg")


class FrequencyTableContinua:
    """
    Tabela de frequência para variáveis quantitativas contínuas.
    Agrupa os dados em classes (intervalos) e calcula frequências.
    """

    def __init__(self, path: str, field: str, n_classes: int = None):
        self.df = pd.read_csv(path, sep=";", encoding="latin-1")
        self.field = field
        self.data = self.df[field].dropna()
        self.n_classes = n_classes or self._sturges()

    # ------------------------------------------------------------------ #
    #  Regra de Sturges: k = 1 + 3.322 * log10(n)                        #
    # ------------------------------------------------------------------ #
    def _sturges(self) -> int:
        n = len(self.data)
        return int(np.ceil(1 + 3.322 * np.log10(n)))

    def _amplitude_total(self) -> float:
        return self.data.max() - self.data.min()

    def _amplitude_classe(self) -> float:
        return self._amplitude_total() / self.n_classes

    def get_table(self) -> pd.DataFrame:
        """
        Retorna DataFrame com:
        - Classe (intervalo)
        - fi  (frequência absoluta)
        - fr  (frequência relativa %)
        - fac (frequência absoluta acumulada)
        - frc (frequência relativa acumulada %)
        - xi  (ponto médio da classe)
        """
        h = self._amplitude_classe()
        vmin = self.data.min()
        vmax = self.data.max()

        bins = np.arange(vmin, vmax + h, h)
        # Garante que o último bin cobre o valor máximo
        bins[-1] = vmax + 1e-9

        labels = [
            f"[{bins[i]:.2f} – {bins[i+1]:.2f})"
            for i in range(len(bins) - 1)
        ]

        cut = pd.cut(self.data, bins=bins, labels=labels, right=False)
        fi = cut.value_counts().sort_index()

        n = fi.sum()
        fr = (fi / n * 100).round(2)
        fac = fi.cumsum()
        frc = fr.cumsum().round(2)
        xi = [(bins[i] + bins[i + 1]) / 2 for i in range(len(bins) - 1)]

        table = pd.DataFrame(
            {
                "Classe": labels,
                "xi (Ponto Médio)": [round(x, 2) for x in xi],
                "fi (Freq. Absoluta)": fi.values,
                "fr (Freq. Relativa %)": fr.values,
                "Fac (Freq. Abs. Acum.)": fac.values,
                "Frc (Freq. Rel. Acum. %)": frc.values,
            }
        )
        return table

    def save_csv(self, output_path: str = None) -> str:
        if output_path is None:
            output_path = (
                f"src/database/2024/ANALISES/frequencia_continua_{self.field}.csv"
            )
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self.get_table().to_csv(output_path, sep=";", encoding="utf-8-sig", index=False)
        return output_path

    def save_histogram(self, output_path: str = None, figsize: tuple = (12, 6)) -> str:
        if output_path is None:
            output_path = (
                f"src/database/2024/ANALISES/histograma_{self.field}.png"
            )
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        h = self._amplitude_classe()
        bins = np.arange(self.data.min(), self.data.max() + h, h)

        fig, ax = plt.subplots(figsize=figsize)
        ax.hist(self.data, bins=bins, edgecolor="black", color="steelblue", alpha=0.8)
        ax.set_title(
            f"Histograma – {self.field}", fontsize=14, fontweight="bold"
        )
        ax.set_xlabel(self.field, fontsize=12)
        ax.set_ylabel("Frequência Absoluta", fontsize=12)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        return output_path

    def execute(
        self,
        save_csv: bool = True,
        save_plot: bool = True,
        verbose: bool = True,
    ) -> dict:
        results = {}
        table = self.get_table()
        results["table"] = table

        if verbose:
            print(f"\n{'='*60}")
            print(f"Tabela de Frequência – {self.field}")
            print(f"n = {len(self.data)} | k = {self.n_classes} classes")
            print(f"{'='*60}")
            print(table.to_string(index=False))

        if save_csv:
            path = self.save_csv()
            results["csv_path"] = path
            if verbose:
                print(f"\nCSV salvo: {path}")

        if save_plot:
            path = self.save_histogram()
            results["plot_path"] = path
            if verbose:
                print(f"Histograma salvo: {path}")

        return results