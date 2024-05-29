import os

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFont, QColor
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
    QScrollArea,
    QDialog,
    QFileDialog,
)
import sys
import crawling
import auto_manual
import SaveLine_Extraction as se
import pandas as pd

SQLi = ['vulnerabilities']
manual = "Select SQLi"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.summary = {}

        self.setWindowTitle("SIAM-W")

        layout = QVBoxLayout()

        notice_layout = QHBoxLayout()

        notify = QLabel("Enter your URL to receive manual")
        code_button = QPushButton("revice your code")
        code_button.setFixedSize(200, 30)
        code_button.clicked.connect(self.codeRevice)
        notice_layout.addWidget(notify)
        notice_layout.addWidget(code_button)
        layout.addLayout(notice_layout)
        
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
        central_widget.setMinimumSize(800, 600)

        self.setCentralWidget(central_widget)

        self.dialog = None
        self.line = []

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def codeRevice(self):
        if self.dialog is None:
            self.dialog = QDialog(self)
        else:
            self.dialog = QDialog(self)

        self.dialog.setWindowTitle('Revice Your Code!')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(500, 400)
        
        dialog_layout = QVBoxLayout(self.dialog)
        beginning_layout = QHBoxLayout()

        explanatory = QLabel("Select Your File here ->", self.dialog)
        file_button = QPushButton('Open', self.dialog)
        file_button.setFixedSize(80, 30)
        file_button.clicked.connect(self.open)
        beginning_layout.addStretch()
        beginning_layout.addWidget(explanatory)
        beginning_layout.addWidget(file_button)

        self.reviced_code = QScrollArea(self.dialog)
        self.reviced_code.setWidget(QLabel('your code will be reviced and show here.')) 
        
        dialog_layout.addLayout(beginning_layout)
        dialog_layout.addWidget(self.reviced_code)

        self.dialog.show()

    def open(self):
        self.line.clear()
        codes = QVBoxLayout()

        file_name = QFileDialog.getOpenFileName(self)[0]
        se.process_file(file_name)
        try:
            revice_list = pd.read_csv('./output.csv')
        except:
            revice_list = pd.DataFrame([{'Line Number': -1, 'Content': '<<< Clean Code ! >>>'},
                                        {'Line Number': -2, 'Content': 'No edit point in this code :)'},
                                        {'Line Number': -3, 'Content': 'Here is your code.'},
                                        ])
        revice_list.set_index('Line Number', inplace=True)
        idx_list = list(revice_list.index.values)
        
        with open(file_name, 'r') as file:
            code = file.readlines()
        
        self.reviced_code.takeWidget()
        
        self.line.clear()
        n = 0
        font = QFont()
        font.setBold(True)
        
        if -1 in idx_list:
            for i in [-1, -2, -3]:
                self.line.append(QLabel(str(revice_list.loc[i, 'Content']), self.dialog))
                
                self.line[n].setFont(font)
                self.line[n].setStyleSheet("color: white; background-color: blue")
                
                n = n + 1
            self.line.append(QLabel('\n\n'))
        
        for idx in range(len(code)):
            # HTML string escape
            if idx in idx_list:
                self.line.append(QLabel(str(revice_list.loc[idx, 'Content']), self.dialog))
                self.line[n].setFont(font)
                self.line[n].setStyleSheet("background-color: orange")
            else:
                self.line.append(QLabel(code[idx].replace('<', '&lt;'), self.dialog))
            n = n + 1
                    
        for idx in range(len(code)):
            codes.addWidget(self.line[idx])
        
        code_widget = QWidget()
        code_widget.setLayout(codes)
        self.reviced_code.setWidget(code_widget)
        if idx_list:
            os.remove("./output.csv")
        

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
