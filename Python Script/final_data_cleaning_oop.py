import pandas as pd
import numpy as np

file_list = [
    r'C:\FPT Polytechnic\Project Tự Làm\Điểm thi thpt 2020 - 2024\diem_thi_2020_2021.csv',
    r'C:\FPT Polytechnic\Project Tự Làm\Điểm thi thpt 2020 - 2024\diem_thi_thpt_2022.csv',
    r'C:\FPT Polytechnic\Project Tự Làm\Điểm thi thpt 2020 - 2024\diem_thi_thpt_2023.csv',
    r'C:\FPT Polytechnic\Project Tự Làm\Điểm thi thpt 2020 - 2024\diem_thi_thpt_2024.csv' 
]

df_national_examination_board = pd.read_excel(
    r"C:\FPT Polytechnic\Project Tự Làm\Điểm thi thpt 2020 - 2024\danh_sach_hoi_dong_thi.xlsx"
)

class NationalHighSchoolExamScore:
    def __init__(self, file_paths, df_national_examination_board):
        self.file_paths = file_paths
        self.dataframes = []
        self.df_national_examination_board = df_national_examination_board

    def read_data(self):
        for path in self.file_paths:
            try:
                df = pd.read_csv(path)
                self.dataframes.append((path, df))
                print(f"Read file: {path}")
            except Exception as e:
                print(f"Error reading file {path}: {e}")

    def check_data(self):
        if not self.dataframes:
            print("No data available")
            return

        for path, df in self.dataframes:
            print(f"\n Check data: {path}")
            print(f"Row numbers: {df.shape[0]}, Column numbers: {df.shape[1]}")
            print("Columns:", list(df.columns))
            print("Duplicate Values:", df.duplicated().sum())
            print("-" * 60)

    def remove_duplicate(self):
        for i, (path, df) in enumerate(self.dataframes):
            before = len(df)
            df = df.drop_duplicates()
            self.dataframes[i] = (path, df)
            print(f"Removed {before - len(df)} duplicate rows from: {path}")

    def drop_specific_columns(self, drop_map):
        for i, (path, df) in enumerate(self.dataframes):
            for key, columns in drop_map.items():
                if key in path:
                    df = df.drop(columns=[col for col in columns if col in df.columns], errors='ignore')
                    self.dataframes[i] = (path, df)

    def rename_columns(self, rename_map):
        for i, (path, df) in enumerate(self.dataframes):
            for key, renames in rename_map.items():
                if key in path:
                    df = df.rename(columns={k: v for k, v in renames.items() if k in df.columns})
                    self.dataframes[i] = (path, df)

    def add_column_code_year(self):
        for i, (path, df) in enumerate(self.dataframes):
            if 'code' not in df.columns and 'sbd' in df.columns:
                df['code'] = df['sbd'].astype(str).apply(lambda x: int(x[:2]) if len(x) == 8 else int(x[:1]))
                print(f" Added 'code' to file: {path}")
            if 'year' not in df.columns:
                df['year'] = 2022 + i - 1  
                print(f"Added 'year' = {2022 + i - 1} to file: {path}")
            self.dataframes[i] = (path, df)

    def reorder_all_columns(self):
        desired_order = [
            'sbd', 'toan', 'ngu_van', 'vat_li', 'hoa_hoc', 'sinh_hoc',
            'lich_su', 'dia_li', 'gdcd', 'ngoai_ngu', 'code', 'year'
        ]
        for i, (path, df) in enumerate(self.dataframes):
            ordered_cols = [col for col in desired_order if col in df.columns]
            df = df[ordered_cols + [col for col in df.columns if col not in ordered_cols]]
            self.dataframes[i] = (path, df)

    def concat_all(self):
        all_dfs = [df for _, df in self.dataframes]
        df_concat = pd.concat(all_dfs, ignore_index=True)
        print(f"📦 Total merged rows: {len(df_concat)}")
        return df_concat

    def add_column_khtn_khxh_khoia_khoib_khoic_khoid(self, df):
        df['khtn'] = df[['vat_li', 'hoa_hoc', 'sinh_hoc']].sum(axis=1, skipna=False)
        df['khtn'] = df['khtn'].where(df[['vat_li', 'hoa_hoc', 'sinh_hoc']].notnull().all(axis=1))

        df['khxh'] = df[['lich_su', 'dia_li', 'gdcd']].sum(axis=1, skipna=False)
        df['khxh'] = df['khxh'].where(df[['lich_su', 'dia_li', 'gdcd']].notnull().all(axis=1))

        df['khoi_a'] = df[['toan', 'vat_li', 'hoa_hoc']].sum(axis=1, skipna=False)
        df['khoi_a'] = df['khoi_a'].where(df[['toan', 'vat_li', 'hoa_hoc']].notnull().all(axis=1))

        df['khoi_b'] = df[['toan', 'hoa_hoc', 'sinh_hoc']].sum(axis=1, skipna=False)
        df['khoi_b'] = df['khoi_b'].where(df[['toan', 'hoa_hoc', 'sinh_hoc']].notnull().all(axis=1))

        df['khoi_c'] = df[['ngu_van', 'lich_su', 'dia_li']].sum(axis=1, skipna=False)
        df['khoi_c'] = df['khoi_c'].where(df[['ngu_van', 'lich_su', 'dia_li']].notnull().all(axis=1))

        df['khoi_d'] = df[['toan', 'ngu_van', 'ngoai_ngu']].sum(axis=1, skipna=False)
        df['khoi_d'] = df['khoi_d'].where(df[['toan', 'ngu_van', 'ngoai_ngu']].notnull().all(axis=1))

        print(" Success add columns: khtn, khxh, group A-D")
        return df


def main():
    data = NationalHighSchoolExamScore(file_list, df_national_examination_board)
    
    data.read_data()
    data.check_data()

    data.remove_duplicate()
    data.check_data()
    
    data.drop_specific_columns({
        "2020_2021": ["Tên", "Ngày Sinh", "Giới tính", "province"],
        "2023": ["ma_ngoai_ngu"],
        "2024": ["ma_ngoai_ngu"]
    })
    data.check_data()


    data.rename_columns({
        "2020_2021": {
            "SBD": "sbd", "Toán": "toan", "Văn": "ngu_van", "Ngoại Ngữ": "ngoai_ngu",
            "Lý": "vat_li", "Hoá": "hoa_hoc", "Sinh": "sinh_hoc",
            "Lịch Sử": "lich_su", "Địa Lý": "dia_li", "GDCD": "gdcd", "Year": "year"
        }
    })
    data.check_data()

    data.add_column_code_year()
    data.check_data(

    )
    data.reorder_all_columns()
    data.check_data()

    df_national_high_school_exam_score = data.concat_all()
    df_national_high_school_exam_score = data.add_column_khtn_khxh_khoia_khoib_khoic_khoid(df_national_high_school_exam_score)
    df_national_high_school_exam_score = df_national_high_school_exam_score.drop(columns=['province'], errors='ignore')

    df_national_high_school_exam_score.to_csv(r"C:\FPT Polytechnic\Project Tự Làm\Điểm thi thpt 2020 - 2024\processed.csv",index=False,encoding='utf-8-sig')

    df_national_high_school_exam_score.info()


    df_national_examination_board.rename(columns={
    "Mã hội đồng": "code",
    "Tên hội đồng thi": "national examination board",
    "Tên Tỉnh": "province"
    }, inplace=True)


    
    df_national_examination_board.to_csv(r"C:\FPT Polytechnic\Graduation_Project\Data\Processed\national_examination_board.csv", index=False)
    df_region_of_vietnam = pd.read_excel(r"C:\FPT Polytechnic\Graduation_Project\Data\Raw\Regions_of_VietNam.xlsx")
    df_national_examination_board_transform = pd.merge(df_national_examination_board, df_region_of_vietnam, how="left", left_on='province', right_on='Province')
    df_national_examination_board_transform.info()
    df_national_examination_board_transform.drop(columns='Province', inplace=True)
    df_national_examination_board_transform.rename(columns={'Regions': 'regions'}, inplace=True)
    df_national_examination_board_transform.to_csv(r'C:\FPT Polytechnic\Graduation_Project\Data\Processed\national_examination_board_transform.csv', index=False)
    df_national_high_school_exam_score.info()


if __name__ == "__main__":
    main()
