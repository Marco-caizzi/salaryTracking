import os
import shutil
import sys
import re
import camelot
import tabula as tabula
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, \
    QApplication, QMessageBox, QComboBox

from windows.evolutionByPercentageOfSalaryGraphWindow import EvolutionByPercentageOfSalaryGraphWindow
from windows.impGananciasGraphWindow import ImpGananciasGraphWindow
from windows.salaryEvolutionGraphWindow import SalaryEvolutionGraphWindow
from db.salaryTracker import SalaryTracker


class RecibosMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_imp_ganancias = None
        self.statistics_combo = None
        self.window_metrics = None
        self.delete_button = None
        self.calcular_button = None
        self.file_list = None
        self.load_button = None
        self.update_button = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Recibos de sueldo")
        self.resize(500, 400)
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        self.file_list = QListWidget()
        self.file_list.doubleClicked.connect(self.open_selected_file)
        main_layout.addWidget(self.file_list)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.load_button = QPushButton("Cargar archivo")
        self.load_button.clicked.connect(self.load_file)
        button_layout.addWidget(self.load_button)
        button_layout.addSpacing(20)

        self.update_button = QPushButton("Actualizar")
        self.update_button.clicked.connect(self.update_list)
        button_layout.addWidget(self.update_button)
        button_layout.addSpacing(20)

        self.calcular_button = QPushButton("Procesar archivos")
        self.calcular_button.clicked.connect(self.process_files)
        button_layout.addWidget(self.calcular_button)
        button_layout.addSpacing(20)

        self.statistics_combo = QComboBox()
        self.statistics_combo.addItem("Evolución del sueldo")
        self.statistics_combo.addItem("Evolución del sueldo en porcentaje")
        self.statistics_combo.addItem("Imp.Ganancias X mes")
        self.statistics_combo.activated.connect(self.show_selected_statistics)
        button_layout.addWidget(self.statistics_combo)
        button_layout.addSpacing(20)

        self.delete_button = QPushButton("Eliminar archivo")
        self.delete_button.clicked.connect(self.delete_selected_file)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch(1)  # agregar espacio al final

        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.update_list()

    def show_selected_statistics(self, index):
        """Muestra la ventana de estadísticas seleccionada"""
        if index == 0:
            self.show_evolution_of_salary()
        elif index == 1:
            self.show_evolution_by_percentage_of_salary()
        elif index == 2:
            self.show_imp_ganancias()

    def show_evolution_of_salary(self):
        self.window_metrics = SalaryEvolutionGraphWindow()
        self.window_metrics.show()

    def show_evolution_by_percentage_of_salary(self):
        self.window_metrics = EvolutionByPercentageOfSalaryGraphWindow()
        self.window_metrics.show()

    def show_imp_ganancias(self):
        self.window_imp_ganancias = ImpGananciasGraphWindow()
        self.window_imp_ganancias.show()

    def open_selected_file(self):
        item = self.file_list.currentItem()
        if item is not None:
            item = item.text()
            file_path = os.path.join("../recibos", item)
            os.startfile(file_path)

    def delete_selected_file(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            return

        message_box = QMessageBox()
        message_box.setWindowTitle("Eliminar archivo")
        message_box.setIcon(QMessageBox.Question)
        message_box.setText("¿Está seguro que desea eliminar el archivo seleccionado?")
        message_box.setInformativeText(
            f"Se eliminará el/los archivo(s) seleccionado(s):\n\n{', '.join(item.text() for item in selected_items)}")
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        message_box.setDefaultButton(QMessageBox.Ok)

        if message_box.exec() == QMessageBox.Ok:
            for item in selected_items:
                file_path = os.path.join("../recibos", item.text())
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    QMessageBox.warning(self, 'Error', f'El archivo {file_path} no existe')
            self.update_list()

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
        except FileNotFoundError as e:
            QMessageBox.warning(self, 'Error', f'El archivo {file_path} no existe')
        except OSError as e:
            QMessageBox.warning(self, 'Error', f'Error al eliminar el archivo {file_path}: {str(e)}')

    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "PDF files (*.pdf)")
        if filename:
            # Verificar si el archivo ya existe en la carpeta de recibos
            if os.path.exists(os.path.join(os.getcwd(), "../recibos", os.path.basename(filename))):
                QMessageBox.critical(self, "Error", "El archivo ya ha sido cargado previamente")
            else:
                destination = os.path.join(os.getcwd(), "../recibos", os.path.basename(filename))
                shutil.copy(filename, destination)
                print("Archivo guardado en:", destination)
            self.update_list()

    def update_list(self):
        self.file_list.clear()
        for file_name in os.listdir(os.path.join(os.getcwd(), "../recibos")):
            if file_name.endswith(".pdf"):
                self.file_list.addItem(file_name)

    @staticmethod
    def process_files():
        recibos_path = os.path.join(os.getcwd(), "../recibos")
        recibos = os.listdir(recibos_path)
        for recibo in recibos:
            if recibo.endswith(".pdf"):
                pdf_path = os.path.join(recibos_path, recibo)
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
                print(f"Liquidation: {liquidation},CUIL: {cuil}, Apellido y Nombre: {surname_first_name}")
                tables = camelot.read_pdf(pdf_path, flavor='stream', table_areas=['34,536,564,202'], strip_text=' ')
                table_data = tables[0].data
                print(table_data)
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
                print(new_table_2)
                db = SalaryTracker("../db/database.db")
                db.storing_receipt_data(datos_pdf=new_table_2, month=recibo.split("_")[0],
                                        year=recibo.split("_")[1].split(".")[0])
        print("Procesamiento finalizado.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RecibosMainWindow()
    window.show()
    sys.exit(app.exec_())
