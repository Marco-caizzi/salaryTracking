import sqlite3


class SalaryTracker:
    def __init__(self, db_path=None):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect_to_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close_db_connection(self):
        self.conn.close()

    def create_months_years_loaded_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS months_years_loaded (
                id INTEGER PRIMARY KEY,
                month TEXT NOT NULL,
                year TEXT NOT NULL
            );
            """
        )

    def create_salary_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS salary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_month_year INTEGER,
                codigo TEXT,
                descripcion_del_concepto TEXT,
                unidad INTEGER,
                haberes_con_aporte REAL,
                haberes_sin_aporte REAL,
                descuentos REAL,
                FOREIGN KEY (id_month_year) REFERENCES months_years_loaded(id)
            );
            """
        )

    def storing_receipt_data(self, datos_pdf, month, year):
        self.connect_to_db()

        # Insert month and year to months_years_loaded table
        self.create_months_years_loaded_table()

        # Check if month and year already loaded
        if self.is_month_year_loaded(month, year):
            print(f"Data for {month} {year} has already been loaded")
            return

        self.cursor.execute(
            """
            INSERT INTO months_years_loaded (month, year)
            VALUES (?, ?);
            """,
            (month, year)
        )
        month_year_id = self.cursor.lastrowid

        # Insert receipt data with month_year_id to salary table
        self.create_salary_table()
        for receipt_data in datos_pdf:
            self.cursor.execute(
                """
                INSERT INTO salary (id_month_year, codigo,descripcion_del_concepto,unidad, haberes_con_aporte,haberes_sin_aporte,descuentos)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (month_year_id, receipt_data[0], receipt_data[1], receipt_data[2], receipt_data[3], receipt_data[4],
                 receipt_data[5])
            )
        self.conn.commit()
        self.close_db_connection()

    def is_month_year_loaded(self, month: str, year: str) -> bool:
        self.cursor.execute(
            """
            SELECT EXISTS(SELECT 1 FROM months_years_loaded WHERE month = ? AND year = ?);
            """,
            (month, year)
        )
        result = self.cursor.fetchone()[0]
        return bool(result)

    def get_salary_data(self):
        self.connect_to_db()
        # Obtener los datos
        self.cursor.execute(
            "SELECT month, haberes_con_aporte FROM salary s,months_years_loaded myl "
            "WHERE s.id_month_year= myl.id"
            " AND codigo = 100 "
            " AND year = 2023"
            " AND descripcion_del_concepto= 'SUELDO'")
        lista = self.cursor.fetchall()

        # Procesar los datos
        lista = self.process_data(lista)

        # Cerrar la conexión a la base de datos
        self.close_db_connection()

        return lista

    @staticmethod
    def process_data(lista):
        # Convertir los meses a su representación numérica correspondiente
        month_num = {"ENERO": "01", "FEBRERO": "02", "MARZO": "03", "ABRIL": "04", "MAYO": "05", "JUNIO": "06",
                     "JULIO": "07", "AGOSTO": "08", "SEPTIEMBRE": "09", "OCTUBRE": "10", "NOVIEMBRE": "11",
                     "DICIEMBRE": "12"}
        data = [(month_num[month], salary) for month, salary in lista]

        # Ordenar los datos en función del mes numérico
        data = sorted(data, key=lambda x: x[0])

        # Convertir los meses numéricos a su representación textual correspondiente
        month_name = {v: k for k, v in month_num.items()}
        data = [(month_name[month], salary) for month, salary in data]

        return data

    def get_month_year(self, month_year_id):
        self.cursor.execute(
            """
            SELECT month, year FROM months_years_loaded WHERE id = ?;
            """,
            (month_year_id,)
        )
        month, year = self.cursor.fetchone()
        return month, year
