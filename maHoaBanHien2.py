import pandas as pd
from datetime import datetime

# Đọc dữ liệu
file_path = "dataBanHien.xlsx"
df = pd.read_excel(file_path)

# Loại bỏ các hàng thiếu dữ liệu ở bất kỳ cột nào
df.dropna(inplace=True)

# Xóa 3 cột đầu tiên và cột cuối cùng
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

# Mapping cố định cho thang Likert
fixed_mapping = {
    "Hoàn toàn không đồng ý": 1,
    "Không đồng ý": 2,
    "Không đồng ý cũng không phản đối": 3,
    "Đồng ý": 4,
    "Hoàn toàn đồng ý": 5,
}

label_maps = {}

# Xác định vị trí cột AF1 để biết từ đâu dùng mapping cố định
likert_start_idx = df.columns.get_loc("AF1")

for idx, col in enumerate(df.columns):
    unique_values = list(df[col].dropna().unique())
    if len(unique_values) == 0:
        print(f"⚠️ Cảnh báo: Cột {col} chỉ có NaN, bỏ qua.")
        continue

    if idx >= likert_start_idx:
        # Từ AF1 trở đi: dùng mapping Likert cố định
        mapping = fixed_mapping
        print(f"ℹ️ Cột {col} được mã hoá bằng mapping cố định Likert.")
    else:
        # Trước AF1: tự động mã hoá
        mapping = {v: i + 1 for i, v in enumerate(unique_values)}
        print(f"ℹ️ Cột {col} được mã hoá bằng mapping tự động.")

    df[col] = df[col].map(mapping)
    label_maps[col] = mapping

# Xuất ra file xlsx mới kèm cả giờ phút và ngày tháng theo định dạng yêu cầu
now_str = datetime.today().strftime("%Hh%M_%d-%m-%Y")
output_filename = f"dataBanHien_{now_str}.xlsx"
df.to_excel(output_filename, index=False)
# In ra thông báo hoàn thành
print(f"Dữ liệu đã được mã hóa và lưu vào file: {output_filename}")
