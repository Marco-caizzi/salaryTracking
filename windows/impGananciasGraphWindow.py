import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow
from db.salaryTracker import SalaryTracker


class ImpGananciasGraphWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph_widget = None
        self.st = SalaryTracker('../db/database.db')
        self.setWindowTitle("Métricas y Gráficos")
        self.resize(1000, 600)

        # Obtener los datos de la base de datos
        self.salary_list = self.st.get_salary_data()

        # Crear la ventana gráfica
        self.create_graph_widget()

    def create_graph_widget(self):
        # Crear el widget de gráficos y agregarlo a la ventana
        self.graph_widget = pg.PlotWidget()
        self.setCentralWidget(self.graph_widget)

        # Configurar los ejes
        x_axis = pg.AxisItem(orientation='bottom')
        x_axis.setTicks([[(i, month) for i, month in enumerate(['ENERO', 'FEBRERO', 'MARZO', 'ABRIL'])]])
        self.graph_widget.setLabel('bottom', 'Mes', units='')
        self.graph_widget.setLabel('left', '% de aumento', units='')

        # Mostrar la ventana
        self.show()
