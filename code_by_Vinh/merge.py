import pandas as pd

class TableMerger:
    def __init__(self, df):
        self.df = df

    def merge_with(self, other_df, on=None, how="inner"):
        """
        Gộp với DataFrame khác dựa trên cột `on`.
        """
        return pd.merge(self.df, other_df, on=on, how=how)
