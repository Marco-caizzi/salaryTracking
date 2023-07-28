import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow
import numpy as np

from db.salaryTracker import SalaryTracker


class SalaryEvolutionGraphWindow(QMainWindow):
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

        months = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE',
                  'NOVIEMBRE', 'DICIEMBRE']

        # Crear los datos de las barras
        y = [salary[1] for salary in self.salary_list]
        x = np.arange(len(self.salary_list))

        # Configurar los ejes
        axis = self.graph_widget.getAxis('bottom')
        axis.setTicks([[(i, month) for i, month in enumerate(months)]])
        self.graph_widget.setLabel('bottom', 'Mes', units='')
        self.graph_widget.setLabel('left', 'Salario', units='$')

        # Crear las barras
        bar = pg.BarGraphItem(x=x, height=y, width=0.6, brush='b')
        self.graph_widget.addItem(bar)

        # Configurar la vista
        self.graph_widget.setYRange(0, max(y) + 10000)
        self.graph_widget.setXRange(-1, len(self.salary_list))
        self.graph_widget.showGrid(x=True, y=True, alpha=0.5)

        # Mostrar la ventana
        self.show()
