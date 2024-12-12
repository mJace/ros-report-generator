#!/bin/bash

# 合併 CSV 的目標檔案
output_file="merged.csv"
sorted_output_file="sorted_merged.csv"

# 清空目標檔案（如果已存在）
> "$output_file"
> "$sorted_output_file"

# 標誌變量，用於處理第一個檔案的標題
header_written=false

# 遍歷當前目錄中的所有 CSV 檔案
for file in *.csv; do
    # 跳過輸出檔案自身
    if [ "$file" == "$output_file" ] || [ "$file" == "$sorted_output_file" ]; then
        continue
    fi

    echo "Processing $file..."
    if ! $header_written; then
        # 如果尚未寫入標題，寫入第一個檔案的標題
        head -n 1 "$file" >> "$output_file"
        header_written=true
    fi
    # 跳過標題行，寫入其餘內容
    tail -n +2 "$file" >> "$output_file"
done

# 排序合併後的檔案
# 使用 awk 找出 interval_start 所在的列
header=$(head -n 1 "$output_file")
column_number=$(echo "$header" | awk -F',' '{for(i=1;i<=NF;i++) if($i=="interval_start") print i}')

if [ -z "$column_number" ]; then
    echo "Error: 'interval_start' column not found"
    exit 1
fi

# 保留標題行，對其餘行按 interval_start 排序
(head -n 1 "$output_file" && tail -n +2 "$output_file" | sort -t',' -k"$column_number"n) > "$sorted_output_file"

echo "CSV files merged and sorted into $sorted_output_file"