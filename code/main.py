from PyQt5 import uic
from PySide2.QtWidgets import QApplication

class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi("./../ui/test.ui")

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()