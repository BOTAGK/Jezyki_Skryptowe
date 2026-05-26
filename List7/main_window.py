# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_browser.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTimeEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.fileLayout = QHBoxLayout()
        self.fileLayout.setObjectName(u"fileLayout")
        self.filePathLine = QLineEdit(self.centralwidget)
        self.filePathLine.setObjectName(u"filePathLine")

        self.fileLayout.addWidget(self.filePathLine)

        self.openButton = QPushButton(self.centralwidget)
        self.openButton.setObjectName(u"openButton")

        self.fileLayout.addWidget(self.openButton)


        self.mainLayout.addLayout(self.fileLayout)

        self.filterGroup = QGroupBox(self.centralwidget)
        self.filterGroup.setObjectName(u"filterGroup")
        self.filterLayout = QGridLayout(self.filterGroup)
        self.filterLayout.setObjectName(u"filterLayout")
        self.fromDateLabel = QLabel(self.filterGroup)
        self.fromDateLabel.setObjectName(u"fromDateLabel")

        self.filterLayout.addWidget(self.fromDateLabel, 0, 0, 1, 1)

        self.fromDateEdit = QDateEdit(self.filterGroup)
        self.fromDateEdit.setObjectName(u"fromDateEdit")
        self.fromDateEdit.setCalendarPopup(True)

        self.filterLayout.addWidget(self.fromDateEdit, 0, 1, 1, 1)

        self.fromTimeLabel = QLabel(self.filterGroup)
        self.fromTimeLabel.setObjectName(u"fromTimeLabel")

        self.filterLayout.addWidget(self.fromTimeLabel, 0, 2, 1, 1)

        self.fromTimeEdit = QTimeEdit(self.filterGroup)
        self.fromTimeEdit.setObjectName(u"fromTimeEdit")

        self.filterLayout.addWidget(self.fromTimeEdit, 0, 3, 1, 1)

        self.toDateLabel = QLabel(self.filterGroup)
        self.toDateLabel.setObjectName(u"toDateLabel")

        self.filterLayout.addWidget(self.toDateLabel, 1, 0, 1, 1)

        self.toDateEdit = QDateEdit(self.filterGroup)
        self.toDateEdit.setObjectName(u"toDateEdit")
        self.toDateEdit.setCalendarPopup(True)

        self.filterLayout.addWidget(self.toDateEdit, 1, 1, 1, 1)

        self.toTimeLabel = QLabel(self.filterGroup)
        self.toTimeLabel.setObjectName(u"toTimeLabel")

        self.filterLayout.addWidget(self.toTimeLabel, 1, 2, 1, 1)

        self.toTimeEdit = QTimeEdit(self.filterGroup)
        self.toTimeEdit.setObjectName(u"toTimeEdit")

        self.filterLayout.addWidget(self.toTimeEdit, 1, 3, 1, 1)

        self.applyButton = QPushButton(self.filterGroup)
        self.applyButton.setObjectName(u"applyButton")

        self.filterLayout.addWidget(self.applyButton, 0, 4, 2, 1)

        self.clearButton = QPushButton(self.filterGroup)
        self.clearButton.setObjectName(u"clearButton")

        self.filterLayout.addWidget(self.clearButton, 0, 5, 2, 1)


        self.mainLayout.addWidget(self.filterGroup)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.setObjectName(u"contentLayout")
        self.logList = QListWidget(self.centralwidget)
        self.logList.setObjectName(u"logList")

        self.contentLayout.addWidget(self.logList)

        self.detailsGroup = QGroupBox(self.centralwidget)
        self.detailsGroup.setObjectName(u"detailsGroup")
        self.detailsLayout = QFormLayout(self.detailsGroup)
        self.detailsLayout.setObjectName(u"detailsLayout")
        self.remoteHostLabel = QLabel(self.detailsGroup)
        self.remoteHostLabel.setObjectName(u"remoteHostLabel")

        self.detailsLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.remoteHostLabel)

        self.remoteHostEdit = QLineEdit(self.detailsGroup)
        self.remoteHostEdit.setObjectName(u"remoteHostEdit")
        self.remoteHostEdit.setReadOnly(True)

        self.detailsLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.remoteHostEdit)

        self.hostLabel = QLabel(self.detailsGroup)
        self.hostLabel.setObjectName(u"hostLabel")

        self.detailsLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.hostLabel)

        self.hostEdit = QLineEdit(self.detailsGroup)
        self.hostEdit.setObjectName(u"hostEdit")
        self.hostEdit.setReadOnly(True)

        self.detailsLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.hostEdit)

        self.dateLabel = QLabel(self.detailsGroup)
        self.dateLabel.setObjectName(u"dateLabel")

        self.detailsLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.dateLabel)

        self.dateEdit = QLineEdit(self.detailsGroup)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setReadOnly(True)

        self.detailsLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.dateEdit)

        self.timeLabel = QLabel(self.detailsGroup)
        self.timeLabel.setObjectName(u"timeLabel")

        self.detailsLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.timeLabel)

        self.timeEdit = QLineEdit(self.detailsGroup)
        self.timeEdit.setObjectName(u"timeEdit")
        self.timeEdit.setReadOnly(True)

        self.detailsLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.timeEdit)

        self.timezoneLabel = QLabel(self.detailsGroup)
        self.timezoneLabel.setObjectName(u"timezoneLabel")

        self.detailsLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.timezoneLabel)

        self.timezoneEdit = QLineEdit(self.detailsGroup)
        self.timezoneEdit.setObjectName(u"timezoneEdit")
        self.timezoneEdit.setReadOnly(True)

        self.detailsLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.timezoneEdit)

        self.methodLabel = QLabel(self.detailsGroup)
        self.methodLabel.setObjectName(u"methodLabel")

        self.detailsLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.methodLabel)

        self.methodEdit = QLineEdit(self.detailsGroup)
        self.methodEdit.setObjectName(u"methodEdit")
        self.methodEdit.setReadOnly(True)

        self.detailsLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.methodEdit)

        self.statusCodeLabel = QLabel(self.detailsGroup)
        self.statusCodeLabel.setObjectName(u"statusCodeLabel")

        self.detailsLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.statusCodeLabel)

        self.statusCodeEdit = QLineEdit(self.detailsGroup)
        self.statusCodeEdit.setObjectName(u"statusCodeEdit")
        self.statusCodeEdit.setReadOnly(True)

        self.detailsLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.statusCodeEdit)

        self.statusTextLabel = QLabel(self.detailsGroup)
        self.statusTextLabel.setObjectName(u"statusTextLabel")

        self.detailsLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.statusTextLabel)

        self.statusTextEdit = QLineEdit(self.detailsGroup)
        self.statusTextEdit.setObjectName(u"statusTextEdit")
        self.statusTextEdit.setReadOnly(True)

        self.detailsLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.statusTextEdit)

        self.resourceLabel = QLabel(self.detailsGroup)
        self.resourceLabel.setObjectName(u"resourceLabel")

        self.detailsLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.resourceLabel)

        self.resourceEdit = QLineEdit(self.detailsGroup)
        self.resourceEdit.setObjectName(u"resourceEdit")
        self.resourceEdit.setReadOnly(True)

        self.detailsLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.resourceEdit)

        self.origPortLabel = QLabel(self.detailsGroup)
        self.origPortLabel.setObjectName(u"origPortLabel")

        self.detailsLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.origPortLabel)

        self.origPortEdit = QLineEdit(self.detailsGroup)
        self.origPortEdit.setObjectName(u"origPortEdit")
        self.origPortEdit.setReadOnly(True)

        self.detailsLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.origPortEdit)

        self.respHostLabel = QLabel(self.detailsGroup)
        self.respHostLabel.setObjectName(u"respHostLabel")

        self.detailsLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.respHostLabel)

        self.respHostEdit = QLineEdit(self.detailsGroup)
        self.respHostEdit.setObjectName(u"respHostEdit")
        self.respHostEdit.setReadOnly(True)

        self.detailsLayout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.respHostEdit)

        self.respPortLabel = QLabel(self.detailsGroup)
        self.respPortLabel.setObjectName(u"respPortLabel")

        self.detailsLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.respPortLabel)

        self.respPortEdit = QLineEdit(self.detailsGroup)
        self.respPortEdit.setObjectName(u"respPortEdit")
        self.respPortEdit.setReadOnly(True)

        self.detailsLayout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.respPortEdit)


        self.contentLayout.addWidget(self.detailsGroup)


        self.mainLayout.addLayout(self.contentLayout)

        self.navLayout = QHBoxLayout()
        self.navLayout.setObjectName(u"navLayout")
        self.prevButton = QPushButton(self.centralwidget)
        self.prevButton.setObjectName(u"prevButton")

        self.navLayout.addWidget(self.prevButton)

        self.navSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.navLayout.addItem(self.navSpacer)

        self.nextButton = QPushButton(self.centralwidget)
        self.nextButton.setObjectName(u"nextButton")

        self.navLayout.addWidget(self.nextButton)


        self.mainLayout.addLayout(self.navLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Log browser", None))
        self.openButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.filterGroup.setTitle(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.fromDateLabel.setText(QCoreApplication.translate("MainWindow", u"From date", None))
        self.fromDateEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd", None))
        self.fromTimeLabel.setText(QCoreApplication.translate("MainWindow", u"From time", None))
        self.fromTimeEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss", None))
        self.toDateLabel.setText(QCoreApplication.translate("MainWindow", u"To date", None))
        self.toDateEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd", None))
        self.toTimeLabel.setText(QCoreApplication.translate("MainWindow", u"To time", None))
        self.toTimeEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.detailsGroup.setTitle(QCoreApplication.translate("MainWindow", u"Details", None))
        self.remoteHostLabel.setText(QCoreApplication.translate("MainWindow", u"Remote host", None))
        self.hostLabel.setText(QCoreApplication.translate("MainWindow", u"Host", None))
        self.dateLabel.setText(QCoreApplication.translate("MainWindow", u"Date", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.timezoneLabel.setText(QCoreApplication.translate("MainWindow", u"Timezone", None))
        self.methodLabel.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.statusCodeLabel.setText(QCoreApplication.translate("MainWindow", u"Status code", None))
        self.statusTextLabel.setText(QCoreApplication.translate("MainWindow", u"Status text", None))
        self.resourceLabel.setText(QCoreApplication.translate("MainWindow", u"Resource", None))
        self.origPortLabel.setText(QCoreApplication.translate("MainWindow", u"Orig port", None))
        self.respHostLabel.setText(QCoreApplication.translate("MainWindow", u"Resp host", None))
        self.respPortLabel.setText(QCoreApplication.translate("MainWindow", u"Resp port", None))
        self.prevButton.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
    # retranslateUi

