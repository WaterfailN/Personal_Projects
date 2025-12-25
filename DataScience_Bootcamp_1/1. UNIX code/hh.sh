#!/bin/sh

# проверяю аргумент
if [ $# -eq 0 ]; then
    echo "Usage: $0 <vacancy_name>"
    exit 1
fi

VACANCY_NAME=$(echo "$1" | sed 's/ /%20/g')

EMAIL="timuribatullin009@gmail.com"

# запрос к API и сохранение результатов в файл
curl -s "https://api.hh.ru/vacancies?text=$VACANCY_NAME&per_page=20" \
  | jq '.' > hh.json

echo "Данные сохранены в hh.json (отформатировано)"
