import pandas as pd

class CodeYearAdder:
    def __init__(self, df):
        self.df = df

    def add_code_and_year(self, code_column="code", year_column="year", code="VN", year=2025):
        """
        Thêm hai cột: code và year vào DataFrame hiện tại.
        """
        self.df[code_column] = code
        self.df[year_column] = year
        return self.df
