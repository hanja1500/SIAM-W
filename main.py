from PySide6.QtCore import QSize    # Qt
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
    QScrollArea
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
        self.lineedit.returnPressed.connect(self.execute)           # execute()
        input_layout.addWidget(self.lineedit)

        button = QPushButton("Enter")
        button.setFixedSize(QSize(100, 30))
        button.clicked.connect(self.execute)                        # execute()
        input_layout.addWidget(button)
        
        self.vuln = QListWidget()
        self.vuln.addItems(SQLi)
        self.vuln.currentItemChanged.connect(self.print_manual)     # print_manual()
        layout.addWidget(self.vuln)

        self.man = QLabel(manual)
        self.man.setMaximumWidth(1000)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.man)
        
        layout.addWidget(self.scroll)

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
        crawling.clear_crawl()

        for key in self.summary.keys():
            SQLi.append(key)

        while self.vuln.count():
            self.vuln.takeItem(0)
        self.man.setText('Select SQLi')
        self.vuln.addItems(SQLi)
        
    def print_manual(self):
        global manual

        try:
            vulnerable = self.vuln.currentItem().text()
        except AttributeError:
            vulnerable = ''

        manual = auto_manual.vulnerability_responses[vulnerable] + '\n\n| 대응 방안 |\n\n'

        for k in auto_manual.response_to_countermeasure[vulnerable]:
            manual = manual + auto_manual.vulnerability_countermeasures[k]

        try:
            manual = manual + '\n\n| 세부 유형 |\n' + self.summary[vulnerable]['Title']
            manual = manual + '\n\n| Payload |\n'
            full_word = self.summary[vulnerable]['Payload']
        except AttributeError:
            full_word = ''
            manual = "Select SQLi"

        word = []

        for i in range(len(full_word)):
            word.append(full_word[i])
            if (i + 1) % 100 == 0:
                manual = manual + ''.join(word) + '\n'
                word = []
        try:
            manual = manual + ''.join(word) + '\n'
        except AttributeError:
            manual = manual + '\n'

        self.man.setText(manual)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
