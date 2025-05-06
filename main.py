
import sys
from PySide6.QtWidgets import QApplication
from vista.ventana_principal import VentanaPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
