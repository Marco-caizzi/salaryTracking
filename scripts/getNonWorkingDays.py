import re
import requests
import json
from bs4 import BeautifulSoup


def get_non_working_days(year):
    url = f"https://www.argentina.gob.ar/interior/feriados-nacionales-{year}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"No se pudo acceder a la página. Código de estado: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    script_content = soup.find('script', src=False, string=lambda text: 'const' in text)
    matches = re.findall(r'{\s*"date":\s*".*?",\s*"label":\s*".*?",\s*"type":\s*".*?"\s*}', str(script_content))
    holidays_list = [json.loads(match) for match in matches]

    return holidays_list
