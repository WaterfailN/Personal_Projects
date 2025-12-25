#!/bin/sh

INPUT_FILE="$1"
OUTPUT_FILE="hh.csv"

# проверка на существование файла
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File $INPUT_FILE not found!"
    exit 1
fi 

jq -r -f filter.jq "$INPUT_FILE" > "$OUTPUT_FILE"

echo "Данные преобразованы в $OUTPUT_FILE"
