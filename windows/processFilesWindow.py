import os
import re
import camelot
import tabula
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QTreeView
from db.salaryTracker import SalaryTracker


# Clase que contiene la ventana que permite procesar los archivos PDF y mostrar los resultados en una tabla
class FileProcessingWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PDF Processor")

        # create a table to display the output
        self.table = QTreeView(self)
        self.setCentralWidget(self.table)
        # Crear el modelo de la vista
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["File", "Liquidation", "CUIL", "Apellido y Nombre", "Data"])
        self.table.setModel(self.model)

        # process the PDF files and display the output in the table
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
                # insert the processed data into the table
                item = QStandardItem(_)
                item.appendRow([QStandardItem(liquidation), QStandardItem(cuil), QStandardItem(surname_first_name),
                                QStandardItem(str(table_data))])
                self.model.appendRow(item)

            # Ajustar el tamaño de la columna para que los contenidos se muestren correctamente
            self.table.resizeColumnToContents(0)

        print("Procesamiento finalizado.")
