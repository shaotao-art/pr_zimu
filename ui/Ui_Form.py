# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testqjaKko.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(825, 653)
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(30, 15, 731, 551))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cho_met = QComboBox(self.layoutWidget)
        self.cho_met.addItem("")
        self.cho_met.addItem("")
        self.cho_met.addItem("")
        self.cho_met.addItem("")
        self.cho_met.setObjectName(u"cho_met")

        self.horizontalLayout_2.addWidget(self.cho_met)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.PlainText)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.url_input = QLineEdit(self.layoutWidget)
        self.url_input.setObjectName(u"url_input")

        self.horizontalLayout_2.addWidget(self.url_input)

        self.send = QPushButton(self.layoutWidget)
        self.send.setObjectName(u"send")

        self.horizontalLayout_2.addWidget(self.send)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setTextFormat(Qt.PlainText)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.add = QPushButton(self.layoutWidget)
        self.add.setObjectName(u"add")

        self.horizontalLayout_3.addWidget(self.add)

        self.delete_2 = QPushButton(self.layoutWidget)
        self.delete_2.setObjectName(u"delete_2")

        self.horizontalLayout_3.addWidget(self.delete_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.headers = QTableWidget(self.layoutWidget)
        if (self.headers.columnCount() < 3):
            self.headers.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.headers.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.headers.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.headers.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.headers.rowCount() < 1):
            self.headers.setRowCount(1)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.headers.setVerticalHeaderItem(0, __qtablewidgetitem3)
        self.headers.setObjectName(u"headers")
        self.headers.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.headers)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setTextFormat(Qt.PlainText)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.body = QPlainTextEdit(self.layoutWidget)
        self.body.setObjectName(u"body")

        self.verticalLayout_2.addWidget(self.body)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setTextFormat(Qt.PlainText)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_4)

        self.ret_msg = QTextBrowser(self.layoutWidget)
        self.ret_msg.setObjectName(u"ret_msg")

        self.verticalLayout_3.addWidget(self.ret_msg)

        self.clear = QPushButton(self.layoutWidget)
        self.clear.setObjectName(u"clear")

        self.verticalLayout_3.addWidget(self.clear)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.retranslateUi(Form)
        self.clear.clicked.connect(self.ret_msg.clear)
        self.add.clicked.connect(self.headers.insertRow(0))
        self.delete_2.clicked.connect(self.headers.removeRow(0))
        self.send.clicked.connect(self.req)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.cho_met.setItemText(0, QCoreApplication.translate("Form", u"post", None))
        self.cho_met.setItemText(1, QCoreApplication.translate("Form", u"put", None))
        self.cho_met.setItemText(2, QCoreApplication.translate("Form", u"delete", None))
        self.cho_met.setItemText(3, QCoreApplication.translate("Form", u"get", None))

        self.cho_met.setPlaceholderText("")
        self.label.setText(QCoreApplication.translate("Form", u"url\u5730\u5740\uff1a", None))
        self.url_input.setText("")
        self.url_input.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u5728\u6b64\u8f93\u5165url\u5730\u5740", None))
        self.send.setText(QCoreApplication.translate("Form", u"\u53d1\u9001", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u6d88\u606f\u5934\uff1a", None))
        self.add.setText(QCoreApplication.translate("Form", u"+", None))
        self.delete_2.setText(QCoreApplication.translate("Form", u"\u2014", None))
        ___qtablewidgetitem = self.headers.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u53c2\u6570", None));
        ___qtablewidgetitem1 = self.headers.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"New Column", None));
        ___qtablewidgetitem2 = self.headers.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u503c", None));
        ___qtablewidgetitem3 = self.headers.verticalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"New Row", None));
        self.label_3.setText(QCoreApplication.translate("Form", u"\u6d88\u606f\u4f53\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u8fd4\u56de\u5185\u5bb9\uff1a", None))
        self.ret_msg.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.clear.setText(QCoreApplication.translate("Form", u"\u6e05\u7a7a\u5185\u5bb9", None))
    # retranslateUi

    def req(self):
        url=self.url_input.text()
        header={ 'User-Agent' :'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
        r=requests.get(url=url,headers=header)
        self.ret_msg.setText(r.text)
