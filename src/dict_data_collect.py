import pandas as pd
from typing import List


class DictParticipante:

    def __init__(self, path: str, sheet_name: str):

        #TODO: utilizar path e sheet_name
        self.dict_data = dict_data = pd.read_excel(
            "src/database/2024/DICIONÁRIO/Dicionário_Microdados_Enem_2024.xlsx",
            sheet_name="PARTICIPANTES_2024",
        )

        self.list_fields = []

    def print_head(self) -> None:
        print(self.dict_data.head(10))

    def print_fields(self) -> None:
        for i in self.list_fields:
            print(i)

    # Salva os campos de dados do participante
    def save_copy_filds(self) -> List:
        col_1 = self.dict_data.iloc[:, 0].dropna().to_list()[2:-3]
        self.list_fields = col_1.copy()

        return self.list_fields
