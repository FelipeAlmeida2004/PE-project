import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from typing import List, Union, Optional, Tuple

matplotlib.use("Agg")


class Graficos:
    """
    Gera gráficos de barras, pizza e dispersão para o projeto ENEM.

    - Barras/Pizza → variáveis qualitativas (UF, Língua, Escolaridade, etc.)
    - Dispersão    → relação entre duas variáveis quantitativas (ex: nota CN × nota MT)
    """

    def __init__(self, path: str):
        self.df = pd.read_csv(path, sep=";", encoding="latin-1")
        self._out = "src/database/2024/ANALISES"

    def _ensure_dir(self, path: str) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    def _serie(self, field: str) -> pd.Series:
        return self.df[field].dropna()

    # ------------------------------------------------------------------ #
    #  Gráfico de Barras (qualitativo)                                     #
    # ------------------------------------------------------------------ #
    def barras(
        self,
        field: str,
        titulo: str = None,
        top_n: int = None,
        orientacao: str = "vertical",
        output_path: str = None,
        figsize: tuple = (12, 6),
        cor: str = "steelblue",
    ) -> str:
        """
        Parâmetros:
            field      → coluna do CSV
            top_n      → exibe somente os N valores mais frequentes
            orientacao → 'vertical' (bar) ou 'horizontal' (barh)
        """
        s = self._serie(field)
        freq = s.value_counts()
        perc = (freq / freq.sum() * 100).round(2)

        if top_n:
            freq = freq.head(top_n)
            perc = perc.head(top_n)

        if output_path is None:
            suf = f"_top{top_n}" if top_n else ""
            output_path = f"{self._out}/barras_{field}{suf}.png"
        self._ensure_dir(output_path)

        fig, ax = plt.subplots(figsize=figsize)
        titulo = titulo or f"Frequência – {field}"

        if orientacao == "horizontal":
            bars = ax.barh(freq.index.astype(str), perc.values, color=cor, edgecolor="white")
            ax.set_xlabel("Percentual (%)", fontsize=11)
            ax.set_ylabel(field, fontsize=11)
            # Rótulos nas barras
            for bar, val in zip(bars, perc.values):
                ax.text(
                    bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}%", va="center", fontsize=9
                )
        else:
            bars = ax.bar(freq.index.astype(str), perc.values, color=cor, edgecolor="white")
            ax.set_xlabel(field, fontsize=11)
            ax.set_ylabel("Percentual (%)", fontsize=11)
            ax.tick_params(axis="x", rotation=45)
            for bar, val in zip(bars, perc.values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    f"{val:.1f}%", ha="center", fontsize=9
                )

        ax.set_title(titulo, fontsize=14, fontweight="bold")
        ax.grid(axis="x" if orientacao == "horizontal" else "y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        return output_path

    # ------------------------------------------------------------------ #
    #  Gráfico de Pizza                                                    #
    # ------------------------------------------------------------------ #
    def pizza(
        self,
        field: str,
        titulo: str = None,
        top_n: int = None,
        output_path: str = None,
        figsize: tuple = (8, 8),
    ) -> str:
        s = self._serie(field)
        freq = s.value_counts()

        if top_n:
            outros = freq.iloc[top_n:].sum()
            freq = freq.head(top_n)
            if outros > 0:
                freq["Outros"] = outros

        perc = freq / freq.sum() * 100

        if output_path is None:
            suf = f"_top{top_n}" if top_n else ""
            output_path = f"{self._out}/pizza_{field}{suf}.png"
        self._ensure_dir(output_path)

        fig, ax = plt.subplots(figsize=figsize)
        titulo = titulo or f"Distribuição – {field}"
        wedges, texts, autotexts = ax.pie(
            perc.values,
            labels=perc.index.astype(str),
            autopct="%1.1f%%",
            startangle=90,
            colors=plt.cm.Set3.colors,
        )
        for t in autotexts:
            t.set_fontsize(9)
        ax.set_title(titulo, fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        return output_path

    # ------------------------------------------------------------------ #
    #  Diagrama de Dispersão                                               #
    # ------------------------------------------------------------------ #
    def dispersao(
        self,
        field_x: str,
        field_y: str,
        titulo: str = None,
        hue_field: str = None,
        output_path: str = None,
        figsize: tuple = (10, 7),
        amostra: int = None,
        linha_tendencia: bool = True,
    ) -> str:
        """
        field_x, field_y → variáveis nos eixos (ex: 'NU_NOTA_CN', 'NU_NOTA_MT')
        hue_field         → variável para colorir grupos (opcional, ex: 'TP_SEXO')
        amostra           → número de linhas a amostrar (evita scatter com milhões de pontos)
        linha_tendencia   → sobrepõe linha de regressão linear
        """
        cols = [field_x, field_y]
        if hue_field:
            cols.append(hue_field)

        sub = self.df[cols].dropna()
        if amostra and len(sub) > amostra:
            sub = sub.sample(amostra, random_state=42)

        if output_path is None:
            hue_suf = f"_por_{hue_field}" if hue_field else ""
            output_path = f"{self._out}/dispersao_{field_x}_x_{field_y}{hue_suf}.png"
        self._ensure_dir(output_path)

        fig, ax = plt.subplots(figsize=figsize)
        titulo = titulo or f"Dispersão – {field_x} × {field_y}"

        if hue_field:
            grupos = sub[hue_field].unique()
            colors = plt.cm.tab10.colors
            for i, grupo in enumerate(grupos):
                mask = sub[hue_field] == grupo
                ax.scatter(
                    sub.loc[mask, field_x],
                    sub.loc[mask, field_y],
                    label=str(grupo),
                    alpha=0.4,
                    s=10,
                    color=colors[i % len(colors)],
                )
            ax.legend(title=hue_field, fontsize=9)
        else:
            ax.scatter(sub[field_x], sub[field_y], alpha=0.3, s=8, color="steelblue")

        if linha_tendencia:
            x_vals = sub[field_x].values
            y_vals = sub[field_y].values
            coef = np.polyfit(x_vals, y_vals, 1)
            poly = np.poly1d(coef)
            x_line = np.linspace(x_vals.min(), x_vals.max(), 200)
            ax.plot(x_line, poly(x_line), color="red", linewidth=2,
                    linestyle="--", label=f"y = {coef[0]:.2f}x + {coef[1]:.2f}")
            corr = np.corrcoef(x_vals, y_vals)[0, 1]
            ax.text(
                0.05, 0.95, f"r = {corr:.3f}",
                transform=ax.transAxes, fontsize=11,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
            )
            ax.legend(fontsize=9)

        ax.set_title(titulo, fontsize=14, fontweight="bold")
        ax.set_xlabel(field_x, fontsize=12)
        ax.set_ylabel(field_y, fontsize=12)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        return output_path

    # ------------------------------------------------------------------ #
    #  Execução padrão para o ENEM                                        #
    # ------------------------------------------------------------------ #
    def execute_qualitativas(
        self,
        field: str,
        top_n: int = None,
        verbose: bool = True,
    ) -> dict:
        results = {}

        p_bar = self.barras(field, top_n=top_n, orientacao="horizontal")
        p_pie = self.pizza(field, top_n=top_n)

        results["barras"] = p_bar
        results["pizza"] = p_pie

        if verbose:
            print(f"Barras: {p_bar}")
            print(f"Pizza:  {p_pie}")

        return results

    def execute_dispersao(
        self,
        field_x: str,
        field_y: str,
        hue_field: str = None,
        amostra: int = 10_000,
        verbose: bool = True,
    ) -> dict:
        p = self.dispersao(field_x, field_y, hue_field=hue_field, amostra=amostra)
        if verbose:
            print(f"Dispersão: {p}")
        return {"dispersao": p}