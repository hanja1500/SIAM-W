from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
import sys
import crawling

SQLi = ['vulnerabilities']
manual = ""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SIAM-W")

        layout = QVBoxLayout()

        notify = QLabel("Enter your URL to receive manual")
        layout.addWidget(notify)
        
        input_layout = QHBoxLayout()
        layout.addLayout(input_layout)

        self.lineedit = QLineEdit()
        self.lineedit.setPlaceholderText("Enter your URL")
        input_layout.addWidget(self.lineedit)

        button = QPushButton("Enter")
        button.setFixedSize(QSize(100, 30))
        button.clicked.connect(self.execute)
        input_layout.addWidget(button)
        
        self.vuln = QListWidget()
        self.vuln.addItems(SQLi)
        self.vuln.currentItemChanged.connect(self.print_manual)
        layout.addWidget(self.vuln)

        self.man = QLabel(manual)
        layout.addWidget(self.man)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def execute(self):
        url = self.lineedit.text()
        SQLi.pop()
        summary = crawling.summary()
        for item in summary:
            SQLi.append(item['Type'])
        self.vuln.takeItem(0)
        self.vuln.addItems(SQLi)
        
    def print_manual(self):
        vulnerable = self.vuln.currentItem().text()
        if vulnerable == '':
            manual = "Select SQLi"
        manual = "change your brain" # 여기에 vulnerable에 맞 매뉴얼
        self.man.setText(manual)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
