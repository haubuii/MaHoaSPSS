import pandas as pd
from datetime import datetime

# Đọc dữ liệu
file_path = "dataBanHien.xlsx"
df = pd.read_excel(file_path)

# Xóa 2 cột đầu tiên
df = df.iloc[:, 2:]

# Đổi tên các cột còn lại
new_columns = [
    "Gender", "Age", "Mar", "Dept", "Inc", "Pos", "Exp", "Maj",
    "AF1", "AF2", "AF3", "AF4",
    "IE1", "IE2", "IE3", "IE4",
    "PR1", "PR2", "PR3", "PR4",
    "IC1", "IC2", "IC3", "IC4",
    "RC1", "RC2", "RC3", "RC4",
    "EE1", "EE2", "EE3", "EE4", "EE5", "EE6", "EE7",
    "JS1", "JS2", "JS3", "JS4",
    "TI1", "TI2", "TI3", "Size"
]

if len(df.columns) != len(new_columns):
    raise ValueError(
        f"Số cột sau khi xóa (hiện có {len(df.columns)}) không khớp với danh sách tên cột mới (có {len(new_columns)})."
    )

df.columns = new_columns

# Xác định các cột cần mã hóa
columns_to_encode = new_columns[8:-1]  # từ AF1 đến TI3

# Chỉ loại bỏ các hàng thiếu dữ liệu trong các cột Likert (AF1 đến TI3)
df.dropna(subset=columns_to_encode, inplace=True)

# Mã hóa dữ liệu Likert
likert_map = {
    "Hoàn toàn không đồng ý": 1,
    "Không đồng ý": 2,
    "Không đồng ý cũng không phản đối": 3,
    "Đồng ý": 4,
    "Hoàn toàn đồng ý": 5,
}

for col in columns_to_encode:
    df[col] = df[col].map(likert_map)

if df[columns_to_encode].isnull().any().any():
    print("⚠️ Cảnh báo: Có giá trị chưa được mã hóa (nằm ngoài các lựa chọn Likert đã định nghĩa).")

# Xuất ra file xlsx mới kèm cả giờ phút và ngày tháng
now_str = datetime.today().strftime("%Hh%M_%d-%m-%Y")
output_filename = f"dataBanHien_{now_str}.xlsx"
df.to_excel(output_filename, index=False)
print(f"Dữ liệu đã được mã hóa và lưu vào file: {output_filename}")