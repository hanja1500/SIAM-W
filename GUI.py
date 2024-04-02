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
import auto_manual

SQLi = ['vulnerabilities']
manual = "Select SQLi"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.summary = {}

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
        self.man.setMaximumWidth(1000)
        layout.addWidget(self.man)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def execute(self):
        self.summary = {}
        url = self.lineedit.text()
        auto_manual.call_SQLmap(url)

        while len(SQLi):
            SQLi.pop()

        self.summary = crawling.summary()
        auto_manual.clear_crawl

        for key in self.summary.keys():
            SQLi.append(key)

        while self.vuln.count():
            self.vuln.takeItem(0)
        self.vuln.addItems(SQLi)
        
    def print_manual(self):
        vulnerable = self.vuln.currentItem().text()
        
        if vulnerable == '' or vulnerable == 'vulnerabilities':
            manual = "Select SQLi"
        else:
            manual = auto_manual.vulnerability_responses[vulnerable]
            manual = manual + '\n\n| 세부 유형 |\n' + self.summary[vulnerable]['Title']
            manual = manual + '\n\n| Payload |\n'
            word = []
            full_word = self.summary[vulnerable]['Payload']
            for i in range(len(full_word)):
                word.append(full_word[i])
                if (i + 1) % 100 == 0:
                    manual = manual + ''.join(word) + '\n'
                    word = []
            manual = manual + ''.join(word) + '\n'
        self.man.setText(manual)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
