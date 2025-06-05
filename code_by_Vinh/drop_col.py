class ColumnDropper:
    def __init__(self, df):
        self.df = df

    def drop(self, columns_to_drop):
        """
        Xoá các cột được chỉ định khỏi DataFrame.
        """
        return self.df.drop(columns=columns_to_drop, axis=1)
