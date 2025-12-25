import requests
import sys
from bs4 import BeautifulSoup
import cProfile
import io
import pstats


def get_financial_data(ticker, field):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': 'en-US,en;q=0.9'
    }

    url = f"https://finance.yahoo.com/quote/{ticker}/financials"
    resp = requests.get(url, headers=headers)

    resp.raise_for_status()
    field_elem = BeautifulSoup(resp.content, 'html.parser').find_all('div', {'class': 'row lv-0 yf-t22klz'})

    for row in field_elem:
        div_title = row.find('div', {'class': 'rowTitle yf-t22klz'})
        attribute_title = div_title.get('title', '').strip()
        text_title = div_title.text
        if field == attribute_title or field == text_title:
            field_row = row
    return tuple([element.text.strip() for element in field_row.find_all('div', class_='column')])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: use './financial.py <ticker> <field>'. Example: ./financial.py MSFT 'Total Revenue'",
              file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1].upper()
    field = sys.argv[2]
    profiler = cProfile.Profile()

    profiler.enable()
    try:
        result = get_financial_data(ticker, field)
        print(result)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    profiler.disable()

    with open('profiling-tottime.txt', 'w') as f:
        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

        f.write(s.getvalue())
