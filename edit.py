import pandas as pd
import numpy as np
from datetime import datetime
import random
import re
import os

# === Nhập tên file Excel từ bàn phím và kiểm tra tồn tại ===
while True:
    input_file = input("Nhập tên file Excel (.xlsx) cần sửa số liệu (mặc định = data_encoded.xlsx): ").strip()
    file_path = input_file if input_file else "data_encoded.xlsx"

    if os.path.exists(file_path):
        print(f"✅ Đã tìm thấy file: {file_path}")
        break
    else:
        print(f"❌ File không tồn tại: {file_path}. Vui lòng nhập lại.")

# === Cấu hình ===
max_edits_per_row = 1  # Mỗi dòng chỉ được sửa tối đa 1 lần

# === Nhập từ bàn phím (có mặc định) ===
try:
    input_ratio = input("Nhập tỷ lệ dòng cần sửa (mặc định = 0.1 (10%)): ").strip()
    edit_ratio = float(input_ratio) if input_ratio else 0.1

    if not (0 <= edit_ratio <= 1):
        raise ValueError("Giới hạn không hợp lệ.")

    print(f"✅ Tỷ lệ sửa được sử dụng: {edit_ratio:.2f} ({int(edit_ratio * 100)}%)")
except:
    edit_ratio = 0.1
    print("⚠️ Không hợp lệ. Dùng mặc định edit_ratio = 0.1 (10%)")

try:
    input_corr_min = input("Nhập ngưỡng tương quan thấp nhất (mặc định = 0.65): ").strip()
    input_corr_max = input("Nhập ngưỡng tương quan cao nhất (mặc định = 0.9): ").strip()
    corr_min = float(input_corr_min) if input_corr_min else 0.65
    corr_max = float(input_corr_max) if input_corr_max else 0.9

    if not (0 <= corr_min <= corr_max <= 1):
        raise ValueError("Giới hạn không hợp lệ.")

    corr_range = (corr_min, corr_max)
    print(f"✅ Ngưỡng tương quan được sử dụng: từ {corr_min:.2f} đến {corr_max:.2f}")
except:
    corr_range = (0.65, 0.9)
    print("⚠️ Không hợp lệ. Dùng mặc định corr_range = (0.65, 0.9)")

# === Đọc dữ liệu và xác định các cột cần kiểm tra ===
df = pd.read_excel(file_path)

# Tìm các cột có dạng: chữ + số (VD: EB1, GI12)
columns_to_check = [col for col in df.columns if re.match(r'^[A-Z]+[0-9]+$', str(col))]
df_target = df[columns_to_check]

# Tự động gom nhóm biến theo tiền tố chữ
groups = {}
for col in columns_to_check:
    prefix = re.match(r'^([A-Z]+)', col).group(1)
    groups.setdefault(prefix, []).append(col)

# In ra thông tin nhóm cột
print("\n[INFO] Các nhóm cột được xác định:")
for group_name, group_cols in groups.items():
    print(f"  - Nhóm {group_name}: {', '.join(group_cols)}")

# === Tạo biến trung bình đại diện nhóm ===
print("\n[INFO] Tạo biến trung bình cho từng nhóm...")
for group_name, group_cols in groups.items():
    new_col_name = f"{group_name}_mean"
    df[new_col_name] = df[group_cols].mean(axis=1)
    print(f"  ➕ Đã thêm cột: {new_col_name}")

# === Hàm xử lý tương quan nhóm ===
def fix_column_corr(df_group, edit_ratio, corr_range):
    df_group = df_group.copy()
    n_rows = df_group.shape[0]
    row_edit_count = {i: 0 for i in range(n_rows)}
    any_edit = False

    for col in df_group.columns:
        col_threshold = round(random.uniform(*corr_range), 2)

        other_cols = [c for c in df_group.columns if c != col]
        corr_matrix = df_group[other_cols + [col]].corr()
        mean_corr = corr_matrix.loc[col, other_cols].mean()
        print(f"[CHECK] {col}: mean_corr = {mean_corr:.2f} (threshold = {col_threshold})")

        if mean_corr < col_threshold:
            n_edit = max(1, int(edit_ratio * n_rows))
            editable_indices = [i for i, cnt in row_edit_count.items() if cnt < max_edits_per_row]
            if len(editable_indices) < n_edit:
                n_edit = len(editable_indices)

            indices_to_edit = random.sample(editable_indices, n_edit)

            for idx in indices_to_edit:
                old_val = df_group.loc[idx, col]
                ref_val = df_group.loc[idx, other_cols].mean()
                noise = np.random.normal(0, 0.3)
                new_val = int(np.clip(round(ref_val + noise), 1, 5))
                df_group.loc[idx, col] = new_val
                row_edit_count[idx] += 1
                print(f"[EDIT] {col} tại dòng {idx+1}: {old_val} → {new_val}")
            any_edit = True

    return df_group, any_edit

# === Bắt đầu xử lý ===
df_fixed = df.copy()
edit_flag = False

for group_name, group_cols in groups.items():
    print(f"\n[PROCESS] Xử lý nhóm {group_name}")
    fixed_group, group_edited = fix_column_corr(df_target[group_cols], edit_ratio, corr_range)
    df_fixed.update(fixed_group)

    if group_edited:
        print(f"[INFO] ✅ Đã sửa nhóm {group_name}")
        edit_flag = True
    else:
        print(f"[INFO] ⏭ Không cần sửa nhóm {group_name}")

# === Tạo lại các biến trung bình vào df_fixed sau chỉnh sửa ===
for group_name, group_cols in groups.items():
    new_col_name = f"{group_name}_mean"
    df_fixed[new_col_name] = df_fixed[group_cols].mean(axis=1)

# === Xuất file nếu có chỉnh sửa ===
now_str = datetime.today().strftime("%Hh%M_%d-%m-%Y")
if edit_flag:
    output_file = f"dataHien_FIXED_{int(edit_ratio*100)}pct_RANDOMcorr_{now_str}.xlsx"
    df_fixed.to_excel(output_file, index=False)
    print(f"\n✅ Dữ liệu đã được xử lý và lưu vào file: {output_file}")
else:
    print("\n✅ Dữ liệu không cần chỉnh sửa. Không tạo file mới.")

# === Giữ cửa sổ mở ===
input("\n⏳ Nhấn Enter để thoát...")
