import pandas as pd
from datetime import datetime

# Đọc dữ liệu
file_path = 'data.xlsx'
df = pd.read_excel(file_path, sheet_name='Form Responses 1')

# Loại bỏ các hàng thiếu dữ liệu ở bất kỳ cột nào
df.dropna(inplace=True)

# Xóa 4 cột đầu tiên
df = df.iloc[:, 4:]

# Đổi tên 33 cột còn lại
new_columns = [
    'Tuoi', 'GioiTinh', 'TrinhDoHocVan', 'NgheNghiep',
    'EB1', 'EB2', 'EB3', 'EB4',
    'EK1', 'EK2', 'EK3', 'EK4', 'EK5',
    'EC1', 'EC2', 'EC3',
    'GI1', 'GI2', 'GI3', 'GI4', 'GI5', 'GI6', 'GI7', 'GI8', 'GI9', 'GI10', 'GI11', 'GI12',
    'BL1', 'BL2', 'BL3', 'BL4', 'BL5'
]

if len(df.columns) != len(new_columns):
    raise ValueError(f"Số cột sau khi xóa (hiện có {len(df.columns)}) không khớp với danh sách tên cột mới (có {len(new_columns)}).")

df.columns = new_columns

# Mã hóa dữ liệu
gender_map = {'Nữ': 1, 'Nam': 2, 'Khác': 3}
education_map = {
    'Tốt nghiệp Cấp 3': 1,
    'Cao đẳng': 2,
    'Đại học': 3,
    'Sau đại học': 4
}
job_map = {
    'Nhân viên văn phòng': 1,
    'Sinh viên': 2,
    'Làm việc tự do (Freelance)': 3,
    'Kinh doanh': 4,
    'Khác': 5
}
age_map = {
    'Từ 18 đến 25 tuổi': 1,
    'Từ 26 đến 35 tuổi': 2,
    'Từ 36 đến 45 tuổi': 3
}
likert_map = {
    'Hoàn toàn không đồng ý': 1,
    'Không đồng ý': 2,
    'Trung lập': 3,
    'Đồng ý': 4,
    'Hoàn toàn đồng ý': 5
}

df['GioiTinh'] = df['GioiTinh'].map(gender_map)
df['TrinhDoHocVan'] = df['TrinhDoHocVan'].map(education_map)
df['NgheNghiep'] = df['NgheNghiep'].map(job_map)
df['Tuoi'] = df['Tuoi'].map(age_map)

for col in df.columns:
    if df[col].isin(likert_map.keys()).any():
        df[col] = df[col].map(likert_map)

# Xuất ra file xlsx mới kèm cả giờ phút
now_str = datetime.today().strftime('%d%m_%H%M')
output_filename = f'data_{now_str}_encoded.xlsx'
df.to_excel(output_filename, index=False)
# In ra thông báo hoàn thành
print(f"Dữ liệu đã được mã hóa và lưu vào file: {output_filename}")