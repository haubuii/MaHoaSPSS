import pandas as pd

# Đọc file gốc
df = pd.read_excel("dataBanHien.xlsx", sheet_name="Form Responses 1")

# Loại bỏ các hàng thiếu dữ liệu ở bất kỳ cột nào
df.dropna(inplace=True)

# Xóa 4 cột đầu tiên
df = df.iloc[:, 4:]

# Tạo tên cột mới
new_col_names = [
    "Age", "Mar", "Dept", "Inc", "Pos", "Exp", "Maj",
    "AF1", "AF2", "AF3", "AF4",
    "IE1", "IE2", "IE3", "IE4",
    "PR1", "PR2", "PR3", "PR4",
    "IC1", "IC2", "IC3", "IC4",
    "RC1", "RC2", "RC3", "RC4",
    "EE1", "EE2", "EE3", "EE4", "EE5", "EE6", "EE7",
    "JS1", "JS2", "JS3", "JS4",
    "TI1", "TI2", "TI3",
    "Size"
]

# Đổi tên cột
df_filtered.columns = new_col_names

# Ghi file kết quả
df_filtered.to_excel("/mnt/data/encoded_cleaned_for_spss.xlsx", index=False)
print("Đã lưu file: encoded_cleaned_for_spss.xlsx")
