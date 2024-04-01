from PyQt6 import QtWidgets
from mycheck.UI import Ui_MainWindow
import mycheck.analyze as analyze
# import numpy as np
import matplotlib
# import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
matplotlib.use("QtAgg")


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.RW = analyze.analyze()
        self.setup_graph()
        self.mylineedit = {
            "H": self.ui.H_edit,
            "H2": self.ui.H2_Edit,
            "D": self.ui.D_Edit,
            "B": self.ui.B_Edit,
            "B1": self.ui.B1_Edit,
            "B2": self.ui.B2_Edit,
            "B3": self.ui.B3_Edit,
            "S1": self.ui.S1_Edit,
            "S2": self.ui.S2_Edit,
            "r2": self.ui.r2_Edit,
            "Phi2": self.ui.phi2_Edit,
            "c2": self.ui.c2_Edit,
            "r1": self.ui.r1_Edit,
            "Phi1": self.ui.phi1_Edit,
            "c1": self.ui.c1_Edit,
            "alpha": self.ui.alpha_Edit,
            "rc": self.ui.rc_Edit
        }
        self.setup_control()

    def setup_graph(self):
        self.ui.canvas = FigureCanvas(
            self.RW.graph()  # 將圖表繪製在 FigureCanvas 裡
            )
        self.ui.graphicscene = QtWidgets.QGraphicsScene()   # 建立場景
        self.ui.graphicscene.setSceneRect(0, 0, 387, 240)
        self.ui.graphicscene.addWidget(self.ui.canvas)              # 場景中放入圖表

        self.ui.graphicsView.setScene(self.ui.graphicscene)          # 元件中放入場景

    def setup_control(self):
        for lineedit in self.mylineedit.values():
            lineedit.textChanged.connect(self.lineeditChanged)

    def lineeditChanged(self):
        args = {}
        for key, lineedit in self.mylineedit.items():  # get每格數值
            text = lineedit.text()
            if text != "":
                try:
                    args[key] = float(text)
                    lineedit.setStyleSheet(
                        ""
                        )
                except ValueError:
                    lineedit.setStyleSheet(
                        "QLineEdit { border: 2px solid red; }"
                        )
                    print("ValueError:")
        print(args)
        self.RW.update_val(**args)
        fall_word = f"抗翻轉破壞安全係數 : {self.RW.FS_fall():.2f}"
        slide_word = f"抗滑動破壞安全係數 : {self.RW.FS_slide():.2f}"
        carry_word = f"抗承載值安全係數 : {self.RW.FS_carrying():.2f}"
        self.ui.show_fsval.setPlainText("\n".join([fall_word, slide_word, carry_word]))
