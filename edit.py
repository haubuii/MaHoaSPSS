import pandas as pd
import numpy as np
from datetime import datetime
import random

# === Cấu hình ===
file_path = "dataHien_21h29_09-07-2025_encoded.xlsx"
edit_ratio = 0.1  # 0.1=10% số hàng được sửa
corr_threshold = 0.9  # Ngưỡng tương quan để quyết định sửa

# Đọc dữ liệu
df = pd.read_excel(file_path)

# Danh sách cột cần kiểm tra
columns_to_check = [
    'EB1','EB2','EB3','EB4',
    'EK1','EK2','EK3','EK4','EK5',
    'EC1','EC2','EC3',
    'GI1','GI2','GI3','GI4','GI5','GI6','GI7','GI8','GI9','GI10','GI11','GI12',
    'BL1','BL2','BL3','BL4','BL5'
]

df_target = df[columns_to_check]

# Nhóm biến
groups = {
    'EB': ['EB1', 'EB2', 'EB3', 'EB4'],
    'EK': ['EK1', 'EK2', 'EK3', 'EK4', 'EK5'],
    'EC': ['EC1', 'EC2', 'EC3'],
    'GI': ['GI1','GI2','GI3','GI4','GI5','GI6','GI7','GI8','GI9','GI10','GI11','GI12'],
    'BL': ['BL1','BL2','BL3','BL4','BL5'],
}

# Hàm xử lý
def fix_column_corr(df_group, edit_ratio, corr_threshold):
    df_group = df_group.copy()
    corr_matrix = df_group.corr()
    any_edit = False

    for col in df_group.columns:
        other_cols = [c for c in df_group.columns if c != col]
        mean_corr = corr_matrix.loc[col, other_cols].mean()
        print(f"[CHECK] {col}: mean_corr = {mean_corr:.2f}")

        if mean_corr < corr_threshold:
            n_rows = df_group.shape[0]
            n_edit = max(1, int(edit_ratio * n_rows))
            indices_to_edit = random.sample(range(n_rows), n_edit)

            for idx in indices_to_edit:
                ref_val = df_group.loc[idx, other_cols].mean()
                noise = np.random.normal(0, 0.3)
                new_val = np.clip(round(ref_val + noise), 1, 5)
                df_group.loc[idx, col] = int(new_val)
                print(f"[EDIT] {col} at row {idx} → {new_val:.2f}")

            any_edit = True

    return df_group, any_edit

# Tạo bản sao dữ liệu gốc
df_fixed = df.copy()
edit_flag = False

# Áp dụng sửa nhóm
for group_name, group_cols in groups.items():
    fixed_group, group_edited = fix_column_corr(df_target[group_cols], edit_ratio, corr_threshold)
    df_fixed.update(fixed_group)
    if group_edited:
        print(f"[INFO] ✅ Đã sửa nhóm {group_name}")
        edit_flag = True
    else:
        print(f"[INFO] ⏭ Không cần sửa nhóm {group_name}")

# Lưu file nếu có sửa
now_str = datetime.today().strftime("%Hh%M_%d-%m-%Y")
if edit_flag:
    output_file = f"dataHien_FIXED_{int(edit_ratio*100)}pct_corr{int(corr_threshold*100)}_{now_str}.xlsx"
    df_fixed.to_excel(output_file, index=False)
    print(f"✅ Dữ liệu đã được xử lý và lưu vào file: {output_file}")
else:
    print("✅ Dữ liệu không cần chỉnh sửa. Không tạo file mới.")
