import pandas as pd
from typing import List


class Participante:

    def __init__(self, path: str, sheet_name: str):
        self.dict_data = pd.read_excel(
            path,
            sheet_name=sheet_name,
        )

        self.list_fields = []

    def print_head(self) -> None:
        print(self.dict_data.head(10))

    def print_fields(self) -> None:
        for i in self.list_fields:
            print(i)

    # Salva os campos de dados do participante
    def save_copy_fields(self) -> List:
        participant_field = self.dict_data.iloc[:, 0].dropna().to_list()[2:-3]
        self.list_fields = participant_field.copy()

        return self.list_fields



class Notas:

    def __init__ (self, path: str, sheet_name: str):
        self.dict_data = pd.read_excel(
            path,
            sheet_name=sheet_name,
        )
        self.list_fields = []

    def print_head(self) -> None:
        print(self.dict_data.head(10))
    
    def print_fields(self) -> None:
        for i in self.list_fields:
            print(i)
    
    def save_copy_fields(self) -> List:
        result_field = self.dict_data.iloc[:, 0].dropna().to_list()[2:-6]
        self.list_fields = result_field.copy()

        return self.list_fields
    