# -*- coding: utf-8 -*-
from .modules import *

class Path_Solving_listbox_show(QWidget, PathSolvingListbox_Dialog):
    deleteResult = pyqtSignal(int)
    mergeResult = pyqtSignal(int)
    def __init__(self, resultData, parent=None):
        super(Path_Solving_listbox_show, self).__init__(parent)
        self.setupUi(self)
        for e in resultData: self.addResult(e)
    
    def addResult(self, e):
        item = QListWidgetItem(e['Algorithm']+(": {} ... {}".format(e['path'][:3], e['path'][-3:]) if len(e['path'])>6 else ": {}".format(e['path'])))
        item.setToolTip("[{}]\nAx: {}\nAy: {}\nDx: {}\nDy: {}\nL0: {}\nL1: {}\nL2: {}\nL3: {}\nL4: {}\nTime spand: {:.2f} s".format(
            e['Algorithm'], e['Ax'], e['Ay'], e['Dx'], e['Dy'], e['L0'], e['L1'], e['L2'], e['L3'], e['L4'], e['time']))
        self.Result_list.addItem(item)
    
    @pyqtSlot()
    def on_deleteButton_clicked(self):
        if self.Result_list.currentRow()>-1:
            self.deleteResult.emit(self.Result_list.currentRow())
            self.Result_list.takeItem(self.Result_list.currentRow())
    
    @pyqtSlot()
    def on_mergeButton_clicked(self):
        if self.Result_list.currentRow()>-1:
            reply = QMessageBox.question(self, 'Prompt Message', "Are you sure to merge?\nThe result of the algorithm will be removed at the same time.",
                (QMessageBox.Apply | QMessageBox.Discard), QMessageBox.Apply)
            if reply==QMessageBox.Apply:
                self.mergeResult.emit(self.Result_list.currentRow())
                self.Result_list.takeItem(self.Result_list.currentRow())