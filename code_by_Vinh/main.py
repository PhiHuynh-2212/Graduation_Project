# main.py

from read_csv import DataReader
from check_data import DataChecker
from drop_columns import ColumnDropper
from rename_columns import ColumnRenamer
from merge_table import TableMerger
from add_column_code_year import CodeYearAdder
from remove_duplicates import DuplicateRemover

def main():
    # 1. Đọc dữ liệu
    reader = DataReader("duong_dan_file.csv")
    df = reader.read()

    # 2. Kiểm tra dữ liệu
    checker = DataChecker(df)
    checker.show_info()
    checker.show_missing_values()

    # 3. Xoá cột không cần thiết
    dropper = ColumnDropper(df)
    df = dropper.drop(columns_to_drop=["column1", "column2"])

    # 4. Đổi tên cột
    renamer = ColumnRenamer(df)
    df = renamer.rename_columns({"old_name": "new_name"})

    # 5. Gộp dữ liệu với bảng khác
    merger = TableMerger(df)
    df = merger.merge_with("duong_dan_file_khac.csv")

    # 6. Thêm cột mã và năm
    adder = CodeYearAdder(df)
    df = adder.add_code_and_year()

    # 7. Xoá dòng trùng lặp
    remover = DuplicateRemover(df)
    df = remover.remove_duplicates()

    # 8. Xuất kết quả
    df.to_csv("output.csv", index=False)
    print("Xử lý dữ liệu hoàn tất!")

if __name__ == "__main__":
    main()
