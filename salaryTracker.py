import sqlite3


class SalaryTracker:
    def __init__(self, db_path):
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

    def is_month_year_loaded(self, month: str, year: str) -> bool:
        self.cursor.execute(
            """
            SELECT EXISTS(SELECT 1 FROM months_years_loaded WHERE month = ? AND year = ?);
            """,
            (month, year)
        )
        result = self.cursor.fetchone()[0]
        return bool(result)
