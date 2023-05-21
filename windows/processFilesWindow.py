import os
import re
import camelot
import tabula
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QTreeView
from db.salaryTracker import SalaryTracker


# Clase que contiene la ventana en la cual se procesan los archivos PDF y se muestran los resultados en una tabla.
# Cada archivo PDF se procesa y se muestra en una fila de la tabla. En la ventana se muestra una tabla por cada archivo
# PDF y por cada archivo se genera un título que contiene: Liquidación, CUIL y Apellido y Nombre. Por ejemplo:
# Liquidación: ENERO_2023, CUIL: 20-12345678-9, Apellido y Nombre: Pérez Juan
# Luego del título se muestra una tabla con los datos del archivo PDF. Por ejemplo:
# CODIGO            CONCEPTO  CANTIDAD  HABERES  DESCUENTOS  NETO A PAGAR
# 100                 SUELDO    0.00   100,382.34      0.00       0.00
# 211   PAGODIASDEVACACIONES   21.00   100,014.24      0.00       0.00
# 241  DESC.DIASDEVACACIONES  -21.00  -100,967.64      0.00       0.00
# 530      GASTOSTELETRABAJO    0.00         0.00  1,800.00       0.00
# 801       JUBILACION11.00%    0.00         0.00      0.00  5,677.18
# 802   INSSJP-LEY190323.00%    0.00         0.00      0.00  5,002.87
# 804        OBRASOCIAL3.00%    0.00         0.00      0.00  5,002.87
# 920  IMPUESTOALASGANANCIAS    0.00         0.00      0.00  5,057.77
# 999               REDONDEO    0.00         0.00      0.00      -0.75
class FileProcessingWindow(QMainWindow):
    def __init__(self):
        # Inicializar la ventana principal de la aplicación y sus atributos principales
        super().__init__()
        self.model = None
        self.treeView = None
        self.init_ui()

    def init_ui(self):
        # Inicializar la interfaz gráfica de la ventana principal de la aplicación y sus atributos principales
        self.setWindowTitle("Procesar archivos PDF")
        self.resize(800, 600)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Liquidación', 'CUIL', 'Apellido y Nombre'])  # Titulos de las columnas
        self.treeView = QTreeView()
        self.treeView.setModel(self.model)
        self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setSortingEnabled(True)
        self.setCentralWidget(self.treeView)
        self.process_files()

    def process_files(self):
        pay_stubs_route = os.path.join(os.getcwd(), "../payStubs")
        pay_stubs = os.listdir(pay_stubs_route)
        for _ in pay_stubs:
            if _.endswith(".pdf"):
                pdf_path = os.path.join(pay_stubs_route, _)
                df = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, stream=True)
                data = df[0].values.tolist()[1:]
                liquidation = str(pdf_path.split("\\")[-1].split(".")[0])
                if type(data[6][4]) == str:
                    cuil = data[6][4].replace(" ", "")
                elif type(data[6][5]) == str:
                    cuil = data[6][5].replace(" ", "")
                else:
                    return "Error"
                surname_first_name = data[5][0].split(" ")[4] + " " + data[5][0].split(" ")[5] + data[5][0].split(" ")[
                    6]
                print(f"Liquidation: {liquidation}, CUIL: {cuil}, Apellido y Nombre: {surname_first_name}")
                tables = camelot.read_pdf(pdf_path, flavor='stream', table_areas=['34,536,564,202'], strip_text=' ')
                table_data = tables[0].data
                print(tables[0].df)
                new_table_2 = []
                for i in table_data:
                    new_table = []
                    for j in i:
                        if re.match(r'^[\d,.-]+$', j):
                            j = j.strip()
                            if j.startswith('-'):
                                j = j.replace(',', '')
                                j = -float(j[1:])
                            elif ',' in j:
                                j = j.replace(',', '')
                                j = float(j)
                            else:
                                j = float(j)
                            if j.is_integer():
                                j = int(j)
                            new_table.append(j)
                        else:
                            new_table.append(j)
                    new_table_2.append(new_table)

                db = SalaryTracker("../db/database.db")
                db.storing_receipt_data(datos_pdf=new_table_2, month=_.split("_")[0],
                                        year=_.split("_")[1].split(".")[0])
                self.add_pdf_to_table(liquidation, cuil, surname_first_name)
        print("Procesamiento finalizado.")

    def add_pdf_to_table(self, liquidation, cuil, surname_first_name):
        self.model.appendRow(
            [QStandardItem(liquidation), QStandardItem(cuil), QStandardItem(surname_first_name)])
        self.treeView.expandAll()
        self.treeView.resizeColumnToContents(0)
        self.treeView.resizeColumnToContents(1)
        self.treeView.resizeColumnToContents(2)
        self.treeView.sortByColumn(0, Qt.AscendingOrder)
