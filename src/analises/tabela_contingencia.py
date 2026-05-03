import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from scipy.stats import chi2_contingency
from typing import Optional

matplotlib.use("Agg")


class TabelaContingencia:
    """
    Tabela de contingência (cruzamento) entre duas variáveis qualitativas.
    
    Calcula:
      - Frequências absolutas e relativas
      - Teste Qui-quadrado (χ²) de independência
      - Heatmap de visualização
    
    Exemplo de uso:
        tc = TabelaContingencia(path, "TP_SEXO", "Q006")  # Sexo × Renda
        tc.execute()
    """

    def __init__(self, path: str, campo_linha: str, campo_coluna: str):
        self.df = pd.read_csv(path, sep=";", encoding="latin-1")
        self.campo_linha = campo_linha
        self.campo_coluna = campo_coluna
        self._out = "src/database/2024/ANALISES"

        sub = self.df[[campo_linha, campo_coluna]].dropna()
        self.crosstab_abs = pd.crosstab(
            sub[campo_linha], sub[campo_coluna], margins=True, margins_name="Total"
        )

    # ------------------------------------------------------------------ #
    #  Frequências                                                         #
    # ------------------------------------------------------------------ #
    def freq_absoluta(self) -> pd.DataFrame:
        """Frequências absolutas com totais marginais."""
        return self.crosstab_abs

    def freq_relativa_linha(self) -> pd.DataFrame:
        """% por linha (distribuição condicional à linha)."""
        abs_sem_total = self.crosstab_abs.iloc[:-1, :-1]
        rel = abs_sem_total.div(abs_sem_total.sum(axis=1), axis=0) * 100
        return rel.round(2)

    def freq_relativa_coluna(self) -> pd.DataFrame:
        """% por coluna (distribuição condicional à coluna)."""
        abs_sem_total = self.crosstab_abs.iloc[:-1, :-1]
        rel = abs_sem_total.div(abs_sem_total.sum(axis=0), axis=1) * 100
        return rel.round(2)

    def freq_relativa_total(self) -> pd.DataFrame:
        """% em relação ao total geral."""
        abs_sem_total = self.crosstab_abs.iloc[:-1, :-1]
        total = abs_sem_total.values.sum()
        return (abs_sem_total / total * 100).round(2)

    # ------------------------------------------------------------------ #
    #  Teste Qui-quadrado                                                  #
    # ------------------------------------------------------------------ #
    def qui_quadrado(self) -> dict:
        """
        Teste χ² de independência.
        H0: As variáveis são independentes.
        Se p < 0.05 → rejeita H0 → variáveis associadas.
        """
        obs = self.crosstab_abs.iloc[:-1, :-1].values
        chi2, p, dof, esperado = chi2_contingency(obs)
        return {
            "χ² estatística": round(chi2, 4),
            "p-valor": round(p, 6),
            "Graus de liberdade": dof,
            "Conclusão": (
                "Associação significativa (p < 0.05)"
                if p < 0.05
                else "Sem associação significativa (p ≥ 0.05)"
            ),
        }

    # ------------------------------------------------------------------ #
    #  Exportações                                                         #
    # ------------------------------------------------------------------ #
    def _nome(self) -> str:
        return f"{self.campo_linha}_x_{self.campo_coluna}"

    def save_csv(self, output_path: str = None) -> str:
        if output_path is None:
            output_path = f"{self._out}/contingencia_{self._nome()}.csv"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self.freq_absoluta().to_csv(output_path, sep=";", encoding="utf-8-sig", index=False)
        return output_path

    def save_heatmap(self, output_path: str = None, figsize: tuple = (12, 8)) -> str:
        if output_path is None:
            output_path = f"{self._out}/heatmap_{self._nome()}.png"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        data = self.freq_relativa_linha()

        fig, ax = plt.subplots(figsize=figsize)
        im = ax.imshow(data.values, cmap="YlOrRd", aspect="auto")
        plt.colorbar(im, ax=ax, label="% por linha")

        ax.set_xticks(range(len(data.columns)))
        ax.set_yticks(range(len(data.index)))
        ax.set_xticklabels(data.columns.astype(str), rotation=45, ha="right", fontsize=9)
        ax.set_yticklabels(data.index.astype(str), fontsize=9)

        # Anotações nas células
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                val = data.values[i, j]
                color = "white" if val > data.values.max() * 0.6 else "black"
                ax.text(j, i, f"{val:.1f}%", ha="center", va="center",
                        fontsize=8, color=color)

        ax.set_title(
            f"Tabela de Contingência – {self.campo_linha} × {self.campo_coluna}\n"
            f"(% por linha)",
            fontsize=13, fontweight="bold",
        )
        ax.set_xlabel(self.campo_coluna, fontsize=11)
        ax.set_ylabel(self.campo_linha, fontsize=11)
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
        save_heatmap: bool = True,
        verbose: bool = True,
    ) -> dict:
        results = {}
        chi2_result = self.qui_quadrado()
        results["qui_quadrado"] = chi2_result
        results["freq_absoluta"] = self.freq_absoluta()
        results["freq_relativa_linha"] = self.freq_relativa_linha()

        if verbose:
            print(f"\n{'='*60}")
            print(f"Tabela de Contingência – {self.campo_linha} × {self.campo_coluna}")
            print(f"{'='*60}")
            print("\nFrequências Absolutas:")
            print(self.freq_absoluta().to_string())
            print("\nFrequências Relativas por Linha (%):")
            print(self.freq_relativa_linha().to_string())
            print("\nTeste Qui-quadrado (χ²):")
            for k, v in chi2_result.items():
                print(f"  {k}: {v}")

        if save_csv:
            p = self.save_csv()
            results["csv_path"] = p
            if verbose:
                print(f"\nCSV salvo: {p}")

        if save_heatmap:
            p = self.save_heatmap()
            results["heatmap_path"] = p
            if verbose:
                print(f"Heatmap salvo: {p}")

        return results