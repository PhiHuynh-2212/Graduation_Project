class ColumnRenamer:
    def __init__(self, df):
        self.df = df

    def rename_columns(self, rename_map):
        """
        Đổi tên cột trong DataFrame theo từ điển ánh xạ.
        """
        return self.df.rename(columns=rename_map)
