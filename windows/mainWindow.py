import os
import shutil
import sys
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, \
    QApplication, QMessageBox, QComboBox
from windows.evolutionByPercentageOfSalaryGraphWindow import EvolutionByPercentageOfSalaryGraphWindow
from windows.impGananciasGraphWindow import ImpGananciasGraphWindow
from windows.processFilesWindow import FileProcessingWindow
from windows.salaryEvolutionGraphWindow import SalaryEvolutionGraphWindow


# Clase que contiene la ventana principal de la aplicación, la cual permite cargar archivos, procesarlos y mostrar los
# resultados en una tabla y en gráficos. Además, permite eliminar archivos y actualizar la lista de archivos. También
# permite mostrar las estadísticas de los archivos procesados.
class MainWindow(QMainWindow):
    def __init__(self):
        # Inicializar la ventana principal de la aplicación y sus atributos principales
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
        # Inicializar la interfaz gráfica de la ventana principal de la aplicación y sus atributos principales
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
        self.calcular_button.clicked.connect(self.show_PDF_processor_window)
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
        # Mostrar las estadísticas seleccionadas en el combo box
        if index == 0:
            self.show_evolution_of_salary()
        elif index == 1:
            self.show_evolution_by_percentage_of_salary()
        elif index == 2:
            self.show_imp_ganancias()

    def show_evolution_of_salary(self):
        # Mostrar la evolución del sueldo en un gráfico
        self.window_metrics = SalaryEvolutionGraphWindow()
        self.window_metrics.show()

    def show_evolution_by_percentage_of_salary(self):
        # Mostrar la evolución del sueldo en porcentaje en un gráfico
        self.window_metrics = EvolutionByPercentageOfSalaryGraphWindow()
        self.window_metrics.show()

    def show_imp_ganancias(self):
        # Mostrar el impuesto a las ganancias en un gráfico
        self.window_imp_ganancias = ImpGananciasGraphWindow()
        self.window_imp_ganancias.show()

    def show_PDF_processor_window(self):
        # Mostrar la ventana de procesamiento de archivos
        self.window_metrics = FileProcessingWindow()
        self.window_metrics.show()

    def open_selected_file(self):
        # Abrir el archivo seleccionado en la lista de archivos de recibos de sueldo
        item = self.file_list.currentItem()
        if item is not None:
            item = item.text()
            file_path = os.path.join("../payStubs", item)
            os.startfile(file_path)

    def delete_selected_file(self):
        # Eliminar el archivo seleccionado en la lista de archivos de recibos de sueldo
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            return

        message_box = QMessageBox(self)
        message_box.setWindowTitle("Eliminar archivo")
        message_box.setIcon(QMessageBox.Icon.Question)
        message_box.setText("¿Está seguro que desea eliminar el archivo seleccionado?")
        message_box.setInformativeText(
            f"Se eliminará el/los archivo(s) seleccionado(s):\n\n{', '.join(item.text() for item in selected_items)}")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        message_box.setDefaultButton(QMessageBox.StandardButton.Ok)

        if message_box.exec() == QMessageBox.StandardButton.Ok:
            for item in selected_items:
                file_path = os.path.join("../payStubs", item.text())
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    QMessageBox.warning(self, 'Error', f'El archivo {file_path} no existe')
            self.update_list()

    def load_file(self):
        # Cargar un archivo de recibo de sueldo
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "PDF files (*.pdf)")
        if filename:
            # Verificar si el archivo ya existe en la carpeta de payStubs
            if os.path.exists(os.path.join(os.getcwd(), "../payStubs", os.path.basename(filename))):
                QMessageBox.critical(self, "Error", "El archivo ya ha sido cargado previamente")
            else:
                destination = os.path.join(os.getcwd(), "../payStubs", os.path.basename(filename))
                shutil.copy(filename, destination)
                print("Archivo guardado en:", destination)
            self.update_list()

    def update_list(self):
        # Actualizar la lista de archivos de recibos de sueldo
        self.file_list.clear()
        for file_name in os.listdir(os.path.join(os.getcwd(), "../payStubs")):
            if file_name.endswith(".pdf"):
                self.file_list.addItem(file_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
