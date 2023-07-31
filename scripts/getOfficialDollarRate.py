import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_official_dollar_price(date):
    url = f"https://www.bna.com.ar/Cotizador/HistoricoPrincipales?id=billetes&fecha={date}&filtroEuro=0&filtroDolar=1"
    headers = {
        'Accept': '*/*',
    }

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        html_response = response.text
        soup = BeautifulSoup(html_response, 'html.parser')

        tabla_dolar = soup.find('div', id='tablaDolar')
        elementos_td = tabla_dolar.find_all('td', class_='dest')

        if len(elementos_td) >= 2:
            precio_venta = elementos_td[0].text.strip()
            precio_compra = elementos_td[1].text.strip()

            return float(precio_venta.replace(',', '.')), float(precio_compra.replace(',', '.'))
        else:
            print("No se encontró la información del precio del dólar en la página.")
    else:
        print(f"Error al obtener la página. Código de respuesta: {response.status_code}")
    return None, None
