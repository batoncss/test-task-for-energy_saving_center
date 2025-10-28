import pandas as pd
import json

class DebtProcessor:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file
        self.df = None
        self.aggregated = None

    def load_data(self):
        """Загрузка данных из Excel (первый лист)"""
        self.df = pd.read_excel(self.excel_file, sheet_name=0)
        # Проверка нужных колонок
        required_cols = ['РСО', 'Дебиторская задолженность на конец периода',
                         'Кредиторская задолженность на конец периода', 'Начислено за период']
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"В файле отсутствует колонка: {col}")

    def calculate_overdue(self):
        """Вычисление просроченной задолженности"""
        self.df['Просроченная задолженность'] = (
            self.df['Дебиторская задолженность на конец периода'] -
            self.df['Кредиторская задолженность на конец периода'] -
            self.df['Начислено за период']
        ).clip(lower=0)

    def aggregate_by_rso(self):
        """Агрегация по РСО"""
        self.aggregated = (
            self.df.groupby('РСО')['Просроченная задолженность']
            .sum()
            .reset_index()
        )

    def save_to_json(self, json_file: str):
        """Сохранение в JSON"""
        if self.aggregated is None:
            raise ValueError("Сначала нужно агрегировать данные")
        self.aggregated.to_json(json_file, orient='records', force_ascii=False, indent=4)

# --- Пример использования ---
if __name__ == "__main__":
    processor = DebtProcessor("data.xlsx")  # замените на свой файл
    processor.load_data()
    processor.calculate_overdue()
    processor.aggregate_by_rso()
    processor.save_to_json("data.json")
    print("JSON с агрегированными данными успешно создан!")
