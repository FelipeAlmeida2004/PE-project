import pandas as pd
from typing import List
from abc import ABC


class DictDataCollector(ABC):
    def __init__(self, path: str, sheet_name: str):
        self.dict_data = pd.read_excel(
            path,
            sheet_name=sheet_name,
        )
        self.list_fields = []
        self.removal_fields = []

    def print_head(self) -> None:
        print(self.dict_data.head(10))

    def print_fields(self) -> None:
        for i in self.list_fields:
            print(i)

    def remove_fields(self) -> List:
        self.list_fields = [
            field for field in self.list_fields if field not in self.removal_fields
        ]
        return self.list_fields

    def _extract_fields(self, start: int, end: int) -> List:
        return self.dict_data.iloc[:, 0].dropna().to_list()[start:end]

    def save_copy_fields(self) -> List:
        fields = self._extract_fields(2, -3)
        self.list_fields = fields.copy()
        self.remove_fields()
        return self.list_fields


class Participante(DictDataCollector):
    def __init__(self, path: str, sheet_name: str):
        super().__init__(path, sheet_name)
        self.removal_fields = [
            "DADOS DO LOCAL DE APLICAÇÃO DA PROVA",
            "DADOS DO QUESTIONÁRIO SOCIOECONÔMICO",
        ]

    def save_copy_fields(self) -> List:
        fields = self._extract_fields(2, -3)
        self.list_fields = fields.copy()
        self.remove_fields()
        return self.list_fields


class Notas(DictDataCollector):
    def __init__(self, path: str, sheet_name: str):
        super().__init__(path, sheet_name)
        self.removal_fields = [
            "DADOS DA ESCOLA",
            "DADOS DO LOCAL DE APLICAÇÃO DA PROVA",
            "DADOS DA PROVA OBJETIVA",
            "DADOS DA REDAÇÃO",
        ]

    def save_copy_fields(self) -> List:
        fields = self._extract_fields(2, -6)
        self.list_fields = fields.copy()
        self.remove_fields()
        return self.list_fields
