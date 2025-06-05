class DuplicateRemover:
    def __init__(self, df):
        self.df = df

    def remove_duplicates(self):
        """
        Xoá các dòng bị trùng lặp trong DataFrame.
        """
        return self.df.drop_duplicates()
