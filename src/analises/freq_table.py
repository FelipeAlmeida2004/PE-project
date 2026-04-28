import pandas as pd
from typing import Union, List
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Use backend que não requer display


class FrequencyTable:

    def __init__(self, path: str, fields: Union[str, List[str]]):
        self.df = pd.read_csv(path, sep=";", encoding="latin-1")

        if isinstance(fields, str):
            self.fields = [fields]
        else:
            self.fields = fields if isinstance(fields, list) else list(fields)

    def get_frequency(self) -> Union[pd.Series, pd.DataFrame]:
        if len(self.fields) == 1:
            field = self.fields[0]
            data = self.df[field].dropna()
            return data.value_counts().sort_index()
        else:
            data = self.df[self.fields].dropna()
            return data.value_counts().sort_index()

    def get_frequency_percentage(self) -> Union[pd.Series, pd.DataFrame]:
        freq = self.get_frequency().dropna()
        return (freq / freq.sum() * 100).round(2)

    def save_frequency_to_csv(self, output_path: str = None) -> str:
        if output_path is None:
            field_name = "_".join(self.fields)
            output_path = f"src/database/2024/ANALISES/frequencia_{field_name}.csv"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        freq_data = []

        if len(self.fields) == 1:
            field = self.fields[0]
            freq = self.get_frequency()
            perc = self.get_frequency_percentage()

            for value, count in freq.items():
                freq_data.append(
                    {
                        "campo": field,
                        "valor": value,
                        "frequencia_absoluta": int(count),
                        "frequencia_percentual": perc[value],
                    }
                )
        else:
            freq = self.get_frequency()
            perc = self.get_frequency_percentage()

            for value, count in freq.items():
                freq_data.append(
                    {
                        "campos": "_".join(self.fields),
                        "valor": str(value),
                        "frequencia_absoluta": int(count),
                        "frequencia_percentual": perc[value],
                    }
                )

        df_freq = pd.DataFrame(freq_data)
        df_freq.to_csv(output_path, sep=";", encoding="latin-1", index=False)

        return output_path

    def save_plot(
        self, output_path: str = None, plot_type: str = "bar", figsize: tuple = (12, 6)
    ) -> str:

        if output_path is None:
            field_name = "_".join(self.fields)
            output_path = (
                f"src/database/2024/ANALISES/plot_{field_name}_{plot_type}.png"
            )

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        freq_percentage = self.get_frequency_percentage()

        fig, ax = plt.subplots(figsize=figsize)

        if plot_type == "bar":
            freq_percentage.plot(kind="bar", ax=ax, color="steelblue")
            ax.set_title(
                f"Frequência - {', '.join(self.fields)}", fontsize=14, fontweight="bold"
            )
            ax.set_xlabel("Valores", fontsize=12)
            ax.set_ylabel("Percentual (%)", fontsize=12)
            ax.grid(axis="y", alpha=0.3)

        elif plot_type == "barh":
            freq_percentage.plot(kind="barh", ax=ax, color="coral")
            ax.set_title(
                f"Frequência - {', '.join(self.fields)}", fontsize=14, fontweight="bold"
            )
            ax.set_xlabel("Percentual (%)", fontsize=12)
            ax.set_ylabel("Valores", fontsize=12)
            ax.grid(axis="x", alpha=0.3)

        elif plot_type == "pie":
            freq_percentage.plot(kind="pie", ax=ax, autopct="%1.1f%%")
            ax.set_title(
                f"Distribuição - {', '.join(self.fields)}",
                fontsize=14,
                fontweight="bold",
            )
            ax.set_ylabel("")

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return output_path

    def execute(
        self,
        plot_type: str = "bar",
        save_csv: bool = True,
        save_plot: bool = True,
        verbose: bool = True,
    ) -> dict:

        results = {}
        frequency = self.get_frequency()
        frequency_percentage = self.get_frequency_percentage()

        results["frequency"] = frequency
        results["frequency_percentage"] = frequency_percentage
        results["csv_path"] = None
        results["plot_path"] = None

        if verbose:
            print("Frequência absoluta:")
            print(frequency)
            print("\nFrequência em percentual:")
            print(frequency_percentage)

        if save_csv:
            csv_path = self.save_frequency_to_csv()
            results["csv_path"] = csv_path
            if verbose:
                print(f"\nSalvando tabela em CSV...")
                print(f"CSV criado: {csv_path}")

        if save_plot:
            plot_path = self.save_plot(plot_type=plot_type)
            results["plot_path"] = plot_path
            if verbose:
                print(f"Gráfico de {plot_type} criado: {plot_path}")

        return results
