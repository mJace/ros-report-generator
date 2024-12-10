#!/bin/bash

# 合併 CSV 的目標檔案
output_file="merged.csv"

# 清空目標檔案（如果已存在）
> "$output_file"

# 標誌變量，用於處理第一個檔案的標題
header_written=false

# 遍歷當前目錄中的所有 CSV 檔案
for file in *.csv; do
    # 跳過輸出檔案自身
    if [ "$file" == "$output_file" ]; then
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

echo "CSV files merged into $output_file"
