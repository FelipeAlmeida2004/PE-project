import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from typing import List, Optional, Union
from scipy import stats as scipy_stats

matplotlib.use("Agg")


class EstatisticaDescritiva:
    """
    Calcula e exporta estatísticas descritivas completas para uma ou mais
    variáveis quantitativas:
      - Tendência central: Média, Mediana, Moda
      - Dispersão: Variância, Desvio Padrão, Amplitude, IQR
      - Posição: Quartis (Q1, Q2, Q3) e Percentis arbitrários
      - Gráficos: Boxplot e Histograma lado a lado
    """

    def __init__(self, path: str, fields: Union[str, List[str]]):
        self.df = pd.read_csv(path, sep=";", encoding="latin-1")
        self.fields = [fields] if isinstance(fields, str) else list(fields)

    # ------------------------------------------------------------------ #
    #  Métricas individuais                                                #
    # ------------------------------------------------------------------ #
    def _serie(self, field: str) -> pd.Series:
        return self.df[field].dropna()

    def media(self, field: str) -> float:
        return round(float(self._serie(field).mean()), 4)

    def mediana(self, field: str) -> float:
        return round(float(self._serie(field).median()), 4)

    def moda(self, field: str) -> list:
        result = scipy_stats.mode(self._serie(field), keepdims=True)
        return [round(float(v), 4) for v in result.mode]

    def variancia(self, field: str, ddof: int = 1) -> float:
        """ddof=1 → amostral | ddof=0 → populacional"""
        return round(float(self._serie(field).var(ddof=ddof)), 4)

    def desvio_padrao(self, field: str, ddof: int = 1) -> float:
        return round(float(self._serie(field).std(ddof=ddof)), 4)

    def amplitude(self, field: str) -> float:
        s = self._serie(field)
        return round(float(s.max() - s.min()), 4)

    def quartis(self, field: str) -> dict:
        s = self._serie(field)
        return {
            "Q1 (25%)": round(float(s.quantile(0.25)), 4),
            "Q2 (50%) – Mediana": round(float(s.quantile(0.50)), 4),
            "Q3 (75%)": round(float(s.quantile(0.75)), 4),
        }

    def iqr(self, field: str) -> float:
        """Distância Interquartil (IQR = Q3 - Q1)"""
        s = self._serie(field)
        return round(float(s.quantile(0.75) - s.quantile(0.25)), 4)

    def percentis(self, field: str, percs: List[int] = None) -> dict:
        if percs is None:
            percs = [10, 25, 50, 75, 90, 95, 99]
        s = self._serie(field)
        return {f"P{p}": round(float(s.quantile(p / 100)), 4) for p in percs}

    # ------------------------------------------------------------------ #
    #  Resumo completo de um campo                                         #
    # ------------------------------------------------------------------ #
    def resumo(self, field: str) -> dict:
        s = self._serie(field)
        q = self.quartis(field)
        return {
            "Campo": field,
            "N": len(s),
            "Mínimo": round(float(s.min()), 4),
            "Máximo": round(float(s.max()), 4),
            "Amplitude": self.amplitude(field),
            "Média": self.media(field),
            "Mediana": self.mediana(field),
            "Moda": self.moda(field),
            "Variância (amostral)": self.variancia(field),
            "Desvio Padrão (amostral)": self.desvio_padrao(field),
            **q,
            "IQR (Q3 - Q1)": self.iqr(field),
        }

    def resumo_todos(self) -> List[dict]:
        return [self.resumo(f) for f in self.fields]

    # ------------------------------------------------------------------ #
    #  Exportações                                                         #
    # ------------------------------------------------------------------ #
    def save_csv(self, output_path: str = None) -> str:
        field_name = "_".join(self.fields)
        if output_path is None:
            output_path = (
                f"src/database/2024/ANALISES/descritiva_{field_name}.csv"
            )
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        rows = []
        for f in self.fields:
            r = self.resumo(f)
            r["Moda"] = str(r["Moda"])  # lista → string para CSV
            rows.append(r)

        pd.DataFrame(rows).to_csv(output_path, sep=";", encoding="utf-8-sig", index=False)
        return output_path

    def save_percentis_csv(self, output_path: str = None, percs: List[int] = None) -> str:
        field_name = "_".join(self.fields)
        if output_path is None:
            output_path = (
                f"src/database/2024/ANALISES/percentis_{field_name}.csv"
            )
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        rows = []
        for f in self.fields:
            p = self.percentis(f, percs)
            p["Campo"] = f
            rows.append(p)

        pd.DataFrame(rows).to_csv(output_path, sep=";", encoding="utf-8-sig", index=False)
        return output_path

    def save_boxplot(self, output_path: str = None, figsize: tuple = (10, 6)) -> str:
        field_name = "_".join(self.fields)
        if output_path is None:
            output_path = (
                f"src/database/2024/ANALISES/boxplot_{field_name}.png"
            )
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        data = [self._serie(f).values for f in self.fields]

        fig, ax = plt.subplots(figsize=figsize)
        bp = ax.boxplot(data, labels=self.fields, patch_artist=True, notch=False)

        colors = plt.cm.Set2.colors
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)

        ax.set_title("Boxplot – Distribuição das Variáveis", fontsize=14, fontweight="bold")
        ax.set_ylabel("Valores", fontsize=12)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        return output_path

    def save_histogramas(
        self, output_path: str = None, figsize: tuple = None
    ) -> str:
        """Histogramas de todos os campos lado a lado."""
        field_name = "_".join(self.fields)
        if output_path is None:
            output_path = (
                f"src/database/2024/ANALISES/histogramas_{field_name}.png"
            )
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        n = len(self.fields)
        cols = min(n, 3)
        rows = int(np.ceil(n / cols))
        if figsize is None:
            figsize = (6 * cols, 5 * rows)

        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        axes = np.array(axes).flatten()

        colors = plt.cm.Set2.colors
        for i, (field, ax) in enumerate(zip(self.fields, axes)):
            s = self._serie(field)
            ax.hist(s, bins="auto", edgecolor="black",
                    color=colors[i % len(colors)], alpha=0.8)
            ax.axvline(self.media(field), color="red", linestyle="--",
                       linewidth=1.5, label=f"Média: {self.media(field)}")
            ax.axvline(self.mediana(field), color="navy", linestyle="-.",
                       linewidth=1.5, label=f"Mediana: {self.mediana(field)}")
            ax.set_title(field, fontsize=12, fontweight="bold")
            ax.set_xlabel("Valores", fontsize=10)
            ax.set_ylabel("Frequência", fontsize=10)
            ax.legend(fontsize=8)
            ax.grid(axis="y", alpha=0.3)

        # Oculta eixos sobrando
        for ax in axes[n:]:
            ax.set_visible(False)

        plt.suptitle("Histogramas – Variáveis Quantitativas",
                     fontsize=14, fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        return output_path

    # ------------------------------------------------------------------ #
    #  Execução geral                                                      #
    # ------------------------------------------------------------------ #
    def execute(
        self,
        save_csv: bool = True,
        save_boxplot: bool = True,
        save_histogramas: bool = True,
        verbose: bool = True,
    ) -> dict:
        results = {}

        resumos = self.resumo_todos()
        results["resumos"] = resumos

        if verbose:
            for r in resumos:
                print(f"\n{'='*55}")
                print(f"  Estatísticas Descritivas – {r['Campo']}")
                print(f"{'='*55}")
                for k, v in r.items():
                    if k != "Campo":
                        print(f"  {k:<30} {v}")

        if save_csv:
            p = self.save_csv()
            results["csv_descritiva"] = p
            p2 = self.save_percentis_csv()
            results["csv_percentis"] = p2
            if verbose:
                print(f"\nCSV descritiva: {p}")
                print(f"CSV percentis:  {p2}")

        if save_boxplot:
            p = self.save_boxplot()
            results["boxplot_path"] = p
            if verbose:
                print(f"Boxplot salvo:  {p}")

        if save_histogramas:
            p = self.save_histogramas()
            results["histogramas_path"] = p
            if verbose:
                print(f"Histogramas:    {p}")

        return results