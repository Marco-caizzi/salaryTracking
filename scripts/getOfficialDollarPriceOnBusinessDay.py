from scripts.adjustDateToBusinessDate import adjust_date_to_business_date
from scripts.getNonWorkingDays import get_non_working_days
from scripts.getOfficialDollarRate import get_official_dollar_price


def get_official_dollar_price_on_business_day(date):
    """
    Get official dollar price for a given date.
    """

    non_working_days = get_non_working_days(2023)
    date_to_business_date = adjust_date_to_business_date(date, non_working_days)
    venta_dolar, compra_dolar = get_official_dollar_price(date_to_business_date)
    return date_to_business_date, venta_dolar, compra_dolar


fecha_consulta = "20/05/2023"
date_to_business_date, venta_dolar, compra_dolar = get_official_dollar_price_on_business_day(fecha_consulta)

if venta_dolar is not None and compra_dolar is not None:
    print(f"Precio de venta del dólar ({date_to_business_date}): {venta_dolar}")
    print(f"Precio de compra del dólar ({date_to_business_date}): {compra_dolar}")
