# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs-PyQt5/core/dialog/template.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(755, 529)
        Dialog.setMinimumSize(QtCore.QSize(755, 529))
        Dialog.setMaximumSize(QtCore.QSize(755, 529))
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(1, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.preview = QtWidgets.QGraphicsView(Dialog)
        self.preview.setObjectName("preview")
        self.verticalLayout_2.addWidget(self.preview)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.Ay = QtWidgets.QDoubleSpinBox(Dialog)
        self.Ay.setMinimum(-9999.99)
        self.Ay.setMaximum(9999.99)
        self.Ay.setObjectName("Ay")
        self.gridLayout.addWidget(self.Ay, 1, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.Ax = QtWidgets.QDoubleSpinBox(Dialog)
        self.Ax.setMinimum(-9999.99)
        self.Ax.setMaximum(9999.99)
        self.Ax.setObjectName("Ax")
        self.gridLayout.addWidget(self.Ax, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 3, 1, 1)
        self.Dx = QtWidgets.QDoubleSpinBox(Dialog)
        self.Dx.setMinimum(-9999.99)
        self.Dx.setMaximum(9999.99)
        self.Dx.setObjectName("Dx")
        self.gridLayout.addWidget(self.Dx, 3, 2, 1, 1)
        self.Dy = QtWidgets.QDoubleSpinBox(Dialog)
        self.Dy.setMinimum(-9999.99)
        self.Dy.setMaximum(9999.99)
        self.Dy.setObjectName("Dy")
        self.gridLayout.addWidget(self.Dy, 3, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.dimensionsTable = QtWidgets.QTableWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dimensionsTable.sizePolicy().hasHeightForWidth())
        self.dimensionsTable.setSizePolicy(sizePolicy)
        self.dimensionsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dimensionsTable.setObjectName("dimensionsTable")
        self.dimensionsTable.setColumnCount(2)
        self.dimensionsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.dimensionsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.dimensionsTable.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.dimensionsTable)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Template"))
        self.comboBox.setItemText(0, _translate("Dialog", "4 Bar"))
        self.comboBox.setItemText(1, _translate("Dialog", "8 Bar"))
        self.label_3.setText(_translate("Dialog", "Point B:"))
        self.label_2.setText(_translate("Dialog", "x"))
        self.label.setText(_translate("Dialog", "Point A:"))
        self.label_4.setText(_translate("Dialog", "x"))
        self.label_5.setText(_translate("Dialog", "y"))
        self.label_6.setText(_translate("Dialog", "y"))
        item = self.dimensionsTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "ID"))
        item = self.dimensionsTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Dimension"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

