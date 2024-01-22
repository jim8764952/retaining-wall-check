from PyQt6 import QtWidgets
from controller import MainWindow_controller

if __name__ == '__main__':
    import subprocess
    import sys
    # conversion .ui to .py
    subprocess.call('pyuic6 UI.ui -o UI.py'.split())
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())
