import pandas as pd
from datetime import datetime

# Đọc dữ liệu
file_path = 'data.xlsx'
df = pd.read_excel(file_path, sheet_name='Form Responses 1')

# Loại bỏ các hàng thiếu dữ liệu ở bất kỳ cột nào
df.dropna(inplace=True)  # Xóa hàng có bất kỳ ô nào bị thiếu dữ liệu

# Chuyển đổi các cột phân loại thành số
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

# Xuất ra file xlsx mới
# df.to_excel('Data_encoded.xlsx', index=False)
today_str = datetime.today().strftime('%d%m')
output_filename = f'data_{today_str}_encoded.xlsx'
df.to_excel(output_filename, index=False)
