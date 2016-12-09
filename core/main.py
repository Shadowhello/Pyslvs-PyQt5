# -*- coding: utf-8 -*-
'''
PySolvespace - PyQt 5 GUI with Solvespace Library
Copyright (C) 2016 Yuan Chang
E-mail: daan0014119@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
'''
from .__init__ import *
_translate = QCoreApplication.translate
#Self UI Ports
from .Ui_main import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #File & Default Setting
        self.File = File()
        self.load_settings()
        #QPainter Window
        self.qpainterWindow = DynamicCanvas()
        self.qpainterWindow.setCursor(Qt.CrossCursor)
        self.qpainterWindow.setStatusTip(_translate("MainWindow", "Press Ctrl Key and use mouse to Change Origin or Zoom Size."))
        self.mplLayout.insertWidget(0, self.qpainterWindow)
        self.qpainterWindow.show()
        self.Resolve()
        #Solve & Script & DOF & Mask & Parameter
        self.Solvefail = False
        self.Script = ""
        self.Slvs_Script = ""
        self.DOF = 0
        self.Mask_Change()
        self.init_Right_click_menu()
        self.Parameter_digital.setValidator(QRegExpValidator(QRegExp('^[-]?([1-9][0-9]{1,'+str(self.Default_Bits-2)+'})?[0-9][.][0-9]{1,'+str(self.Default_Bits)+'}$')))
        self.init_open_file()
    
    def load_settings(self):
        option_info = Pyslvs_Settings_ini()
        self.Default_Environment_variables = option_info.Environment_variables
        self.Default_canvas_view = option_info.Zoom_factor
        self.Default_Bits = 8
        self.sym_part = False
    
    def init_open_file(self):
        for i in sys.argv:
            if ".csv" in i:
                fileName = sys.argv[sys.argv.index(i)][2::]
                self.load_Workbook(fileName)
                break
    
    def init_Right_click_menu(self):
        #qpainterWindow Right-click menu
        self.qpainterWindow.setContextMenuPolicy(Qt.CustomContextMenu)
        self.qpainterWindow.customContextMenuRequested.connect(self.on_painter_context_menu)
        self.popMenu_painter = QMenu(self)
        self.action_painter_right_click_menu_add = QAction("Add a Point", self)
        self.popMenu_painter.addAction(self.action_painter_right_click_menu_add)
        self.action_painter_right_click_menu_fix_add = QAction("Add a Fixed Point", self)
        self.popMenu_painter.addAction(self.action_painter_right_click_menu_fix_add)
        self.popMenu_painter.addSeparator()
        self.action_painter_right_click_menu_dimension_add = QAction("Show Dimension", self)
        self.popMenu_painter.addAction(self.action_painter_right_click_menu_dimension_add)
        self.mouse_pos_x = 0.0
        self.mouse_pos_y = 0.0
        self.qpainterWindow.mouse_track.connect(self.context_menu_mouse_pos)
        #Entiteis_Point Right-click menu
        self.Entiteis_Point_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Point_Widget.customContextMenuRequested.connect(self.on_point_context_menu)
        self.popMenu_point = QMenu(self)
        self.action_point_right_click_menu_copy = QAction("Copy Coordinate", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_copy)
        self.action_point_right_click_menu_coverage = QAction("Coverage Coordinate", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_coverage)
        self.action_point_right_click_menu_add = QAction("Add a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_add)
        self.action_point_right_click_menu_edit = QAction("Edit this Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_edit)
        self.popMenu_point.addSeparator()
        self.action_point_right_click_menu_delete = QAction("Delete this Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_delete) 
        #Entiteis_Link Right-click menu
        self.Entiteis_Link_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Link_Widget.customContextMenuRequested.connect(self.on_link_context_menu)
        self.popMenu_link = QMenu(self)
        self.action_link_right_click_menu_add = QAction("Add a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_add)
        self.action_link_right_click_menu_edit = QAction("Edit this Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_edit)
        self.popMenu_link.addSeparator()
        self.action_link_right_click_menu_move_up = QAction("Move up", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_move_up)
        self.action_link_right_click_menu_move_down = QAction("Move down", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_move_down)
        self.popMenu_link.addSeparator()
        self.action_link_right_click_menu_delete = QAction("Delete this Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_delete) 
        #Entiteis_Chain Right-click menu
        self.Entiteis_Stay_Chain_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Stay_Chain_Widget.customContextMenuRequested.connect(self.on_chain_context_menu)
        self.popMenu_chain = QMenu(self)
        self.action_chain_right_click_menu_add = QAction("Add a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_add)
        self.action_chain_right_click_menu_edit = QAction("Edit this Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_edit)
        self.popMenu_chain.addSeparator()
        self.action_chain_right_click_menu_move_up = QAction("Move up", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_move_up)
        self.action_chain_right_click_menu_move_down = QAction("Move down", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_move_down)
        self.popMenu_chain.addSeparator()
        self.action_chain_right_click_menu_delete = QAction("Delete this Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_delete) 
        #Drive_Shaft Right-click menu
        self.Drive_Shaft_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Drive_Shaft_Widget.customContextMenuRequested.connect(self.on_shaft_context_menu)
        self.popMenu_shaft = QMenu(self)
        self.action_shaft_right_click_menu_add = QAction("Add a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_add)
        self.action_shaft_right_click_menu_edit = QAction("Edit this Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_edit)
        self.popMenu_shaft.addSeparator()
        self.action_shaft_right_click_menu_delete = QAction("Delete this Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_delete) 
        #Slider Right-click menu
        self.Slider_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Slider_Widget.customContextMenuRequested.connect(self.on_slider_context_menu)
        self.popMenu_slider = QMenu(self)
        self.action_slider_right_click_menu_add = QAction("Add a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_add)
        self.action_slider_right_click_menu_edit = QAction("Edit this Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_edit)
        self.popMenu_slider.addSeparator()
        self.action_slider_right_click_menu_delete = QAction("Delete this Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_delete) 
        #Rod Right-click menu
        self.Rod_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Rod_Widget.customContextMenuRequested.connect(self.on_rod_context_menu)
        self.popMenu_rod = QMenu(self)
        self.action_rod_right_click_menu_add = QAction("Add a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_add)
        self.action_rod_right_click_menu_edit = QAction("Edit this Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_edit)
        self.popMenu_rod.addSeparator()
        self.action_rod_right_click_menu_delete = QAction("Delete this Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_delete)
        #Parameter Right-click menu
        self.Parameter_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Parameter_Widget.customContextMenuRequested.connect(self.on_parameter_context_menu)
        self.popMenu_parameter = QMenu(self)
        self.action_parameter_right_click_menu_copy = QAction("Copy Parameter", self)
        self.popMenu_parameter.addAction(self.action_parameter_right_click_menu_copy)
        self.action_parameter_right_click_menu_add = QAction("Add a Parameter", self)
        self.popMenu_parameter.addAction(self.action_parameter_right_click_menu_add)
        self.popMenu_parameter.addSeparator()
        self.action_parameter_right_click_menu_move_up = QAction("Move up", self)
        self.popMenu_parameter.addAction(self.action_parameter_right_click_menu_move_up)
        self.action_parameter_right_click_menu_move_down = QAction("Move down", self)
        self.popMenu_parameter.addAction(self.action_parameter_right_click_menu_move_down)
        self.popMenu_parameter.addSeparator()
        self.action_parameter_right_click_menu_delete = QAction("Delete this Parameter", self)
        self.popMenu_parameter.addAction(self.action_parameter_right_click_menu_delete)
    
    #Right-click menu event
    @pyqtSlot(float, float)
    def context_menu_mouse_pos(self, x, y):
        self.mouse_pos_x = x
        self.mouse_pos_y = y
    def on_painter_context_menu(self, point):
        action = self.popMenu_painter.exec_(self.qpainterWindow.mapToGlobal(point))
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        x = str(self.mouse_pos_x)
        y = str(self.mouse_pos_y)
        if action == self.action_painter_right_click_menu_add:
            self.File.Points.editTable(table1, "Point"+str(table1.rowCount()), x, y, False, False)
            self.File.Points.styleAdd(table2, "Point"+str(table2.rowCount()), "Green", "5", "Green")
            self.Resolve()
        elif action == self.action_painter_right_click_menu_fix_add:
            self.File.Points.editTable(table1, "Point"+str(table1.rowCount()), x, y, True, False)
            self.File.Points.styleAdd(table2, "Point"+str(table2.rowCount()), "Green", "10", "Green")
            self.Resolve()
        elif action == self.action_painter_right_click_menu_dimension_add:
            if self.actionDisplay_Dimensions.isChecked()==False:
                self.action_painter_right_click_menu_dimension_add.setText("Hide Dimension")
                self.action_painter_right_click_menu_dimension_add.setChecked(True)
                self.actionDisplay_Dimensions.setChecked(True)
            elif self.actionDisplay_Dimensions.isChecked()==True:
                self.action_painter_right_click_menu_dimension_add.setText("Show Dimension")
                self.action_painter_right_click_menu_dimension_add.setChecked(False)
                self.actionDisplay_Dimensions.setChecked(False)
    def on_point_context_menu(self, point):
        self.action_point_right_click_menu_copy.setVisible(self.Entiteis_Point.currentColumn()==4)
        self.action_point_right_click_menu_coverage.setVisible(self.Entiteis_Point.currentColumn()==4 and self.Entiteis_Point.currentRow()!=0)
        self.action_point_right_click_menu_edit.setEnabled(self.Entiteis_Point.rowCount()>=2)
        self.action_point_right_click_menu_delete.setEnabled(self.Entiteis_Point.rowCount()>=2)
        action = self.popMenu_point.exec_(self.Entiteis_Point_Widget.mapToGlobal(point))
        table_pos = self.Entiteis_Point.currentRow() if self.Entiteis_Point.currentRow()>=1 else 1
        if action == self.action_point_right_click_menu_copy: self.Coordinate_Copy(self.Entiteis_Point)
        elif action == self.action_point_right_click_menu_coverage: self.File.Points.coverageCoordinate(self.Entiteis_Point, self.Entiteis_Point.currentRow())
        elif action == self.action_point_right_click_menu_add: self.on_action_New_Point_triggered()
        elif action == self.action_point_right_click_menu_edit: self.on_actionEdit_Point_triggered(table_pos)
        elif action == self.action_point_right_click_menu_delete: self.on_actionDelete_Point_triggered(table_pos)
    def on_link_context_menu(self, point):
        self.action_link_right_click_menu_edit.setEnabled(self.Entiteis_Link.rowCount()>=1)
        self.action_link_right_click_menu_delete.setEnabled(self.Entiteis_Link.rowCount()>=1)
        self.action_link_right_click_menu_move_up.setEnabled((not bool(self.Entiteis_Link.rowCount()<=1))and(self.Entiteis_Link.currentRow()>=1))
        self.action_link_right_click_menu_move_down.setEnabled((not bool(self.Entiteis_Link.rowCount()<=1))and(self.Entiteis_Link.currentRow()<=self.Entiteis_Link.rowCount()-2))
        action = self.popMenu_link.exec_(self.Entiteis_Link_Widget.mapToGlobal(point))
        if action == self.action_link_right_click_menu_add: self.on_action_New_Line_triggered()
        elif action == self.action_link_right_click_menu_edit: self.on_actionEdit_Linkage_triggered(self.Entiteis_Link.currentRow())
        elif action == self.action_link_right_click_menu_move_up:
            self.move_up(self.Entiteis_Link, self.Entiteis_Link.currentRow(), "Line")
            for i in range(self.Slider.rowCount()):
                if int(self.Slider.item(i, 2).text().replace("Line", ""))==self.Entiteis_Link.currentRow(): self.Slider.setItem(i, 2, "Line"+str(self.Entiteis_Link.currentRow()))
        elif action == self.action_link_right_click_menu_move_down:
            self.move_down(self.Entiteis_Link, self.Entiteis_Link.currentRow(), "Line")
            for i in range(self.Slider.rowCount()):
                if int(self.Slider.item(i, 2).text().replace("Line", ""))==self.Entiteis_Link.currentRow(): self.Slider.setItem(i, 2, "Line"+str(self.Entiteis_Link.currentRow()))
        elif action == self.action_link_right_click_menu_delete: self.on_actionDelete_Linkage_triggered(self.Entiteis_Link.currentRow())
    def on_chain_context_menu(self, point):
        self.action_chain_right_click_menu_edit.setEnabled(self.Entiteis_Stay_Chain.rowCount()>=1)
        self.action_chain_right_click_menu_delete.setEnabled(self.Entiteis_Stay_Chain.rowCount()>=1)
        self.action_chain_right_click_menu_move_up.setEnabled((not bool(self.Entiteis_Stay_Chain.rowCount()<=1))and(self.Entiteis_Stay_Chain.currentRow()>=1))
        self.action_chain_right_click_menu_move_down.setEnabled((not bool(self.Entiteis_Stay_Chain.rowCount()<=1))and(self.Entiteis_Stay_Chain.currentRow()<=self.Entiteis_Link.rowCount()-2))
        action = self.popMenu_chain.exec_(self.Entiteis_Stay_Chain_Widget.mapToGlobal(point))
        if action == self.action_chain_right_click_menu_add: self.on_action_New_Stay_Chain_triggered()
        elif action == self.action_chain_right_click_menu_edit: self.on_actionEdit_Stay_Chain_triggered(self.Entiteis_Stay_Chain.currentRow())
        elif action == self.action_chain_right_click_menu_move_up: self.move_up(self.Entiteis_Stay_Chain, self.Entiteis_Stay_Chain.currentRow(), "Chain")
        elif action == self.action_chain_right_click_menu_move_down: self.move_down(self.Entiteis_Stay_Chain, self.Entiteis_Stay_Chain.currentRow(), "Chain")
        elif action == self.action_chain_right_click_menu_delete: self.on_actionDelete_Stay_Chain_triggered(self.Entiteis_Stay_Chain.currentRow())
    def on_shaft_context_menu(self, point):
        self.action_shaft_right_click_menu_edit.setEnabled(self.Drive_Shaft.rowCount()>=1)
        self.action_shaft_right_click_menu_delete.setEnabled(self.Drive_Shaft.rowCount()>=1)
        action = self.popMenu_shaft.exec_(self.Drive_Shaft_Widget.mapToGlobal(point))
        if action == self.action_shaft_right_click_menu_add: self.on_action_Set_Drive_Shaft_triggered()
        elif action == self.action_shaft_right_click_menu_edit: self.on_action_Edit_Drive_Shaft_triggered(self.Drive_Shaft.currentRow())
        elif action == self.action_shaft_right_click_menu_delete: self.on_actionDelete_Drive_Shaft_triggered(self.Drive_Shaft.currentRow())
    def on_slider_context_menu(self, point):
        self.action_slider_right_click_menu_edit.setEnabled(self.Slider.rowCount()>=1)
        self.action_slider_right_click_menu_delete.setEnabled(self.Slider.rowCount()>=1)
        action = self.popMenu_slider.exec_(self.Slider_Widget.mapToGlobal(point))
        if action == self.action_slider_right_click_menu_add: self.on_action_Set_Slider_triggered()
        elif action == self.action_slider_right_click_menu_edit: self.on_action_Edit_Slider_triggered(self.Slider.currentRow())
        elif action == self.action_slider_right_click_menu_delete: self.on_actionDelete_Slider_triggered(self.Slider.currentRow())
    def on_rod_context_menu(self, point):
        self.action_rod_right_click_menu_edit.setEnabled(self.Rod.rowCount()>=1)
        self.action_rod_right_click_menu_delete.setEnabled(self.Rod.rowCount()>=1)
        action = self.popMenu_rod.exec_(self.Rod_Widget.mapToGlobal(point))
        if action == self.action_rod_right_click_menu_add: self.on_action_Set_Rod_triggered()
        elif action == self.action_rod_right_click_menu_edit: self.on_action_Edit_Piston_Spring_triggered(self.Rod.currentRow())
        elif action == self.action_rod_right_click_menu_delete: self.on_actionDelete_Piston_Spring_triggered(self.Rod.currentRow())
    def on_parameter_context_menu(self, point):
        self.action_parameter_right_click_menu_copy.setVisible(self.Parameter_list.currentColumn()==1)
        self.action_parameter_right_click_menu_move_up.setEnabled((not bool(self.Parameter_list.rowCount()<=1))and(self.Parameter_list.currentRow()>=1))
        self.action_parameter_right_click_menu_move_down.setEnabled((not bool(self.Parameter_list.rowCount()<=1))and(self.Parameter_list.currentRow()<=self.Parameter_list.rowCount()-2))
        self.action_parameter_right_click_menu_delete.setEnabled(self.Parameter_list.rowCount()>=1)
        action = self.popMenu_parameter.exec_(self.Parameter_Widget.mapToGlobal(point))
        if action == self.action_parameter_right_click_menu_copy: self.Coordinate_Copy(self.Parameter_list)
        elif action == self.action_parameter_right_click_menu_add: self.on_parameter_add()
        elif action == self.action_parameter_right_click_menu_move_up:
            table = self.Parameter_list
            row = self.Parameter_list.currentRow()
            try:
                table.insertRow(row-1)
                for i in range(2):
                    name_set = QTableWidgetItem(table.item(row+1, i).text())
                    name_set.setFlags(Qt.ItemIsEnabled)
                    table.setItem(row-1, i, name_set)
                commit_set = QTableWidgetItem(table.item(row+1, 2).text())
                commit_set.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                table.setItem(row-1, 2, commit_set)
                table.removeRow(row+1)
                self.Workbook_noSave()
                self.Mask_Change()
                self.Resolve()
            except: pass
        elif action == self.action_parameter_right_click_menu_move_down:
            try:
                table.insertRow(row+2)
                for i in range(2):
                    name_set = QTableWidgetItem(table.item(row+2, i).text())
                    name_set.setFlags(Qt.ItemIsEnabled)
                    table.setItem(row+2, i, name_set)
                commit_set = QTableWidgetItem(table.item(row+2, 2).text())
                commit_set.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                table.removeRow(row)
                self.Workbook_noSave()
            except: pass
        elif action == self.action_parameter_right_click_menu_delete:
            self.Parameter_list.removeRow(self.Parameter_list.currentRow())
            self.Workbook_noSave()
            self.Mask_Change()
    
    #Table move up & down & copy
    def move_up(self, table, row, name):
        try:
            table.insertRow(row-1)
            for i in range(table.columnCount()): table.setItem(row-1, i, QTableWidgetItem(table.item(row+1, i).text()))
            table.removeRow(row+1)
            for j in range(table.rowCount()):
                name_set = QTableWidgetItem(name+str(j))
                name_set.setFlags(Qt.ItemIsEnabled)
                table.setItem(j, 0, name_set)
            self.Workbook_noSave()
        except: pass
    def move_down(self, table, row, name):
        try:
            table.insertRow(row+2)
            for i in range(table.columnCount()): table.setItem(row+2, i, QTableWidgetItem(table.item(row, i).text()))
            table.removeRow(row)
            for j in range(table.rowCount()):
                name_set = QTableWidgetItem(name+str(j))
                name_set.setFlags(Qt.ItemIsEnabled)
                table.setItem(j, 0, QTableWidgetItem(name+str(j)))
            self.Workbook_noSave()
        except: pass
    def Coordinate_Copy(self, table):
        clipboard = QApplication.clipboard()
        clipboard.setText(table.currentItem().text())
    
    #Close Event
    def closeEvent(self, event):
        if self.File.form['changed']:
            reply = QMessageBox.question(self, 'Saving Message', "Are you sure to quit?\nAny Changes won't be saved.",
                (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply == QMessageBox.Discard or reply == QMessageBox.Ok:
                print("Exit.")
                event.accept()
            elif reply == QMessageBox.Save:
                self.on_actionSave_triggered()
                if not self.File.form['changed']:
                    print("Exit.")
                    event.accept()
                else: event.ignore()
            else: event.ignore()
        else:
            print("Exit.")
            event.accept()
    
    #Scripts
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self):
        dlg = Script_Dialog()
        dlg.script.setPlainText(self.Script)
        dlg.show()
        dlg.exec()
    
    #Resolve
    def Resolve(self):
        table_point, table_line, table_chain, table_shaft, table_slider, table_rod = self.Obstacles_Exclusion()
        #Solve
        result = []
        solvespace = Solvespace()
        fileName = self.windowTitle().replace("Pyslvs - ", "").replace("*", "").split("/")[-1].split(".")[0]
        result, DOF = solvespace.static_process(table_point, table_line, table_chain,
            table_shaft, table_slider, table_rod, fileName, self.Parameter_list, self.sym_part)
        self.Script = solvespace.Script
        if result==[]:
            self.Solvefail = True
            print("Rebuild the cavanc falled.")
        else:
            self.Solvefail = False
            for i in range(table_point.rowCount()): self.File.Points.currentPos(table_point, i, result[i*2], result[i*2+1])
            self.DOF = DOF
            self.DOF_view.setPlainText(str(self.DOF-6+self.Drive_Shaft.rowCount())+" ("+str(self.DOF-6)+")")
            self.Reload_Canvas()
    
    #Reload Canvas
    def Reload_Canvas(self):
        self.qpainterWindow.update_figure(
        float(self.LineWidth.text()), float(self.PathWidth.text()),
            self.Entiteis_Point, self.Entiteis_Link,
            self.Entiteis_Stay_Chain, self.Drive_Shaft,
            self.Slider, self.Rod, self.Parameter_list,
            self.Entiteis_Point_Style, self.ZoomText.toPlainText(),
            self.Font_size.value(),
            self.actionDisplay_Dimensions.isChecked(), self.actionDisplay_Point_Mark.isChecked(),
            self.action_Black_Blackground.isChecked())
    
    #Obstacles Exclusion
    def Obstacles_Exclusion(self):
        table_point = self.Entiteis_Point
        table_line = self.Entiteis_Link
        table_chain = self.Entiteis_Stay_Chain
        table_shaft = self.Drive_Shaft
        table_slider = self.Slider
        table_rod = self.Rod
        for i in range(table_line.rowCount()):
            a = int(table_line.item(i, 1).text().replace("Point", ""))
            b = int(table_line.item(i, 2).text().replace("Point", ""))
            case1 = float(table_point.item(a, 1).text())==float(table_point.item(b, 1).text())
            case2 = float(table_point.item(a, 2).text())==float(table_point.item(b, 2).text())
            if case1 and case2:
                if b == 0: table_point.setItem(a, 1, QTableWidgetItem(str(float(table_point.item(a, 1).text())+0.01)))
                else: table_point.setItem(b, 1, QTableWidgetItem(str(float(table_point.item(b, 1).text())+0.01)))
        for i in range(table_chain.rowCount()):
            a = int(table_chain.item(i, 1).text().replace("Point", ""))
            b = int(table_chain.item(i, 2).text().replace("Point", ""))
            c = int(table_chain.item(i, 3).text().replace("Point", ""))
            case1 = float(table_point.item(a, 1).text())==float(table_point.item(b, 1).text())
            case2 = float(table_point.item(a, 2).text())==float(table_point.item(b, 2).text())
            case3 = float(table_point.item(b, 1).text())==float(table_point.item(c, 1).text())
            case4 = float(table_point.item(b, 2).text())==float(table_point.item(c, 2).text())
            case5 = float(table_point.item(a, 1).text())==float(table_point.item(c, 1).text())
            case6 = float(table_point.item(a, 2).text())==float(table_point.item(c, 2).text())
            if case1 and case2:
                if b==0: table_point.setItem(a, 1, QTableWidgetItem(str(float(table_point.item(a, 1).text())+0.01)))
                else: table_point.setItem(b, 1, QTableWidgetItem(str(float(table_point.item(b, 1).text())+0.01)))
            if case3 and case4:
                if c==0: table_point.setItem(b, 2, QTableWidgetItem(str(float(table_point.item(b, 2).text())+0.01)))
                else: table_point.setItem(c, 2, QTableWidgetItem(str(float(table_point.item(c, 2).text())+0.01)))
            if case5 and case6:
                if c==0: table_point.setItem(a, 2, QTableWidgetItem(str(float(table_point.item(a, 2).text())+0.01)))
                else: table_point.setItem(c, 2, QTableWidgetItem(str(float(table_point.item(c, 2).text())+0.01)))
        return table_point, table_line, table_chain, table_shaft, table_slider, table_rod
    
    #Workbook Change
    def Workbook_noSave(self):
        self.File.form['changed'] = True
        self.setWindowTitle(_translate("MainWindow", self.windowTitle().replace("*", "")+"*"))
    
    @pyqtSlot()
    def on_action_Full_Screen_triggered(self): print("Full Screen.")
    @pyqtSlot()
    def on_actionNormalmized_triggered(self): print("Normal Screen.")
    
    @pyqtSlot()
    def on_actionHow_to_use_triggered(self):
        dlg = Help_info_show()
        dlg.show()
        dlg.exec()
    @pyqtSlot()
    def on_action_Get_Help_triggered(self):
        print("Open http://project.mde.tw/blog/slvs-library-functions.html")
        webbrowser.open("http://project.mde.tw/blog/slvs-library-functions.html")
    @pyqtSlot()
    def on_actionGit_hub_Site_triggered(self):
        print("Open https://github.com/40323230/python-solvespace")
        webbrowser.open("https://github.com/40323230/python-solvespace")
    @pyqtSlot()
    def on_actionGithub_Wiki_triggered(self):
        print("Open https://github.com/40323230/python-solvespace/wiki")
        webbrowser.open("https://github.com/40323230/python-solvespace/wiki")
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self):
        dlg = version_show()
        dlg.show()
        dlg.exec()
    @pyqtSlot()
    def on_action_About_Python_Solvspace_triggered(self):
        dlg = Info_show()
        dlg.show()
        dlg.exec()
    
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self): self.checkChange("[New Workbook]", new_workbook(), 'Generating New Workbook...')
    @pyqtSlot()
    def on_action_Load_Workbook_triggered(self): self.checkChange()
    @pyqtSlot()
    def on_actionCrank_rocker_triggered(self): self.checkChange("[Example] Crank Rocker", example_crankRocker(), 'Loading Example...')
    @pyqtSlot()
    def on_actionMutiple_Link_triggered(self): self.checkChange("[Example] Mutiple Link", example_mutipleLink(), 'Loading Example...')
    #Workbook Functions
    def checkChange(self, name=False, data=[], say=''):
        if self.File.form['changed']:
            warning_reset  = reset_show()
            warning_reset.show()
            if warning_reset.exec_():
                print(say)
                self.load_Workbook(name, data)
        else:
            print(say)
            self.load_Workbook(name, data)
    def load_Workbook(self, fileName=False, data=[]):
        self.closePanel()
        self.File.reset(
            self.Entiteis_Point, self.Entiteis_Point_Style,
            self.Entiteis_Link, self.Entiteis_Stay_Chain,
            self.Drive_Shaft, self.Slider,
            self.Rod, self.Parameter_list)
        self.qpainterWindow.removePath()
        self.Resolve()
        print("Reset workbook.")
        if fileName==False: fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', self.Default_Environment_variables, 'CSV File(*.csv);;Text File(*.txt)')
        if fileName[-4::]=='.csv' or "[Example]" in fileName:
            if data==[]:
                print("Get:"+fileName)
                with open(fileName, newline="") as stream:
                    reader = csv.reader(stream, delimiter=' ', quotechar='|')
                    for row in reader: data += ', '.join(row).split('\t,')
            if self.File.check(data):
                self.File.read(
                    fileName, data,
                    self.Entiteis_Point, self.Entiteis_Point_Style,
                    self.Entiteis_Link, self.Entiteis_Stay_Chain,
                    self.Drive_Shaft, self.Slider,
                    self.Rod, self.Parameter_list)
                for i in range(1, self.Entiteis_Point_Style.rowCount()): self.Entiteis_Point_Style.cellWidget(i, 3).currentIndexChanged.connect(self.Point_Style_set)
                self.File.form['changed'] = False
                self.setWindowTitle(_translate("MainWindow", "Pyslvs - "+fileName))
                self.Resolve()
                self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">No Path Data</span></p></body></html>"))
                self.Path_Clear.setEnabled(bool(self.File.Path.data) and bool(self.File.Path.runList))
                self.Path_coordinate.setEnabled(bool(self.File.Path.data) and bool(self.File.Path.runList))
                self.Path_data_show.setEnabled(bool(self.File.Path.data) and bool(self.File.Path.runList))
                self.qpainterWindow.path_track(self.File.Path.data, self.File.Path.runList)
                print("Successful Load the workbook...")
            else:
                print("Failed to load!")
    def closePanel(self):
        try:
            self.MeasurementWidget.deleteLater()
            del self.MeasurementWidget
            self.Measurement.setChecked(False)
        except: pass
        try:
            self.DriveWidget.deleteLater()
            del self.DriveWidget
            self.Drive.setChecked(False)
        except: pass
        try:
            self.qpainterWindow.AuxLine['show'] = False
            self.AuxLineWidget.deleteLater()
            del self.AuxLineWidget
            self.AuxLine.setChecked(False)
        except: pass
        self.reset_Auxline()
    
    @pyqtSlot()
    def on_action_Property_triggered(self): self.File.setProperty()
    
    @pyqtSlot()
    def on_actionSave_triggered(self):
        print("Saving this Workbook...")
        if "[New Workbook]" in self.File.form['fileName'] or "[Example]" in self.File.form['fileName']:
            fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', self.Default_Environment_variables, 'Spreadsheet(*.csv)')
        else:
            fileName = self.windowTitle().replace("Pyslvs - ", "").replace("*", "")
        if fileName:
            self.save(fileName)
    @pyqtSlot()
    def on_actionSave_as_triggered(self):
        print("Saving to another Workbook...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', self.Default_Environment_variables, 'Spreadsheet(*.csv)')
        if fileName:
            self.save(fileName)
    def save(self, fileName):
        fileName = fileName.replace(".csv", "")+".csv"
        with open(fileName, 'w', newline="") as stream:
            writer = csv.writer(stream)
            self.File.write(
                fileName, writer,
                self.Entiteis_Point, self.Entiteis_Point_Style,
                self.Entiteis_Link, self.Entiteis_Stay_Chain,
                self.Drive_Shaft, self.Slider,
                self.Rod, self.Parameter_list)
        print("Successful Save: "+fileName)
        self.File.form['changed'] = False
        self.setWindowTitle(_translate("MainWindow", "Pyslvs - "+fileName))
    
    @pyqtSlot()
    def on_action_Output_to_Solvespace_triggered(self):
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', self.Default_Environment_variables, 'Solvespace models(*.slvs)')
        if fileName:
            solvespace = Solvespace()
            self.Slvs_Script = solvespace.slvs_formate(self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain,
                self.Drive_Shaft, self.Slider, self.Rod, self.Parameter_list)
            fileName = fileName.replace(".slvs", "")+".slvs"
            with open(fileName, 'w', encoding="iso-8859-15", newline="") as f:
                f.write(self.Slvs_Script)
            print("Successful Save: "+fileName)
            self.File.form['changed'] = False
            self.setWindowTitle(_translate("MainWindow", "Pyslvs - "+fileName))
    
    @pyqtSlot()
    def on_action_Output_to_Script_triggered(self):
        print("Saving to script...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', self.Default_Environment_variables, 'Python Script(*.py)')
        if fileName:
            fileName = fileName.replace(".py", "")
            if sub == "Python Script(*.py)": fileName += ".py"
            with open(fileName, 'w', newline="") as f:
                f.write(self.Script)
            print("Saved to:"+str(fileName))
    
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        print("Saving to picture...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', self.Default_Environment_variables,
            "Portable Network Graphics (*.png);;Joint Photographic Experts Group (*.jpg);;Joint Photographic Experts Group (*.jpeg);;Bitmap Image file (*.bmp);;\
            Business Process Model (*.bpm);;Tagged Image File Format (*.tiff);;Tagged Image File Format (*.tif);;Windows Icon (*.ico);;Wireless Application Protocol Bitmap (*.wbmp);;\
            X BitMap (*.xbm);;X Pixmap (*.xpm)")
        if fileName:
            print("Formate: "+sub)
            sub = sub[sub.find('.')+1:sub.find(')')]
            fileName = fileName.replace('.'+sub, "")
            fileName += '.'+sub
            pixmap = self.qpainterWindow.grab()
            pixmap.save(fileName, format = sub)
            print("Saved to:"+str(fileName))
    
    @pyqtSlot()
    def on_actionOutput_to_DXF_triggered(self):
        print("Saving to DXF...")
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save file...', self.Default_Environment_variables, 'AutoCAD DXF (*.dxf)')
        if fileName:
            fileName = fileName.replace(".dxf", "")
            fileName += ".dxf"
            solvespace = Solvespace()
            solvespace.dxf_process(fileName, self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain,
                self.Drive_Shaft, self.Slider, self.Rod, self.Parameter_list)
    
    @pyqtSlot()
    def on_action_Output_to_S_QLite_Data_Base_triggered(self):
        print("Saving to Data Base...")
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save file...', self.Default_Environment_variables, 'Data Base(*.db)')
        if fileName:
            fileName = fileName.replace(".db", "")
            fileName += ".db"
            #TODO: SQLite
    
    def on_parameter_add(self):
        rowPosition = self.Parameter_list.rowCount()
        self.Parameter_list.insertRow(rowPosition)
        name_set = 0
        for i in range(rowPosition):
            if 'n'+str(name_set) == self.Parameter_list.item(i, 0).text(): name_set += 1
        name_set = QTableWidgetItem('n'+str(name_set))
        name_set.setFlags(Qt.ItemIsEnabled)
        digit_set = QTableWidgetItem("0.0")
        digit_set.setFlags(Qt.ItemIsEnabled)
        commit_set = QTableWidgetItem("Not committed yet.")
        commit_set.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        self.Parameter_list.setItem(rowPosition, 0, name_set)
        self.Parameter_list.setItem(rowPosition, 1, digit_set)
        self.Parameter_list.setItem(rowPosition, 2, commit_set)
        self.Workbook_noSave()
        self.Mask_Change()
    @pyqtSlot()
    def on_Parameter_add_clicked(self): self.on_parameter_add()
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        dlg  = New_point()
        dlg.Point_num.insertPlainText("Point"+str(table1.rowCount()))
        dlg.X_coordinate.setValidator(self.Mask)
        dlg.Y_coordinate.setValidator(self.Mask)
        dlg.show()
        if dlg.exec_():
            x = self.X_coordinate.text() if not self.X_coordinate.text()in["", "n", "-"] else self.X_coordinate.placeholderText()
            y = self.Y_coordinate.text() if not self.Y_coordinate.text()in["", "n", "-"] else self.Y_coordinate.placeholderText()
            self.File.Points.editTable(table1, dlg.Point_num.toPlainText(),
                x, y, dlg.Fix_Point.checkState(), False)
            fix = "10" if dlg.Fix_Point.checkState() else "5"
            self.File.Points.styleAdd(table2, dlg.Point_num.toPlainText(), "Green", fix, "Green")
            self.Resolve()
            self.Workbook_noSave()
    @pyqtSlot()
    def on_Point_add_button_clicked(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        x = self.X_coordinate.text() if not self.X_coordinate.text()in["", "n", "-"] else self.X_coordinate.placeholderText()
        y = self.Y_coordinate.text() if not self.Y_coordinate.text()in["", "n", "-"] else self.Y_coordinate.placeholderText()
        self.File.Points.editTable(table1, "Point"+str(table1.rowCount()), x, y, False, False)
        self.File.Points.styleAdd(table2, "Point"+str(table2.rowCount()), "Green", "5", "Green")
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionEdit_Point_triggered(self, pos = 1):
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg  = edit_point_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(1, table1.rowCount()): dlg.Point.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Another_point.connect(self.Change_Edit_Point)
            self.point_feedback.connect(dlg.change_feedback)
            dlg.Point.setCurrentIndex(pos-1)
            self.Change_Edit_Point(pos)
            dlg.X_coordinate.setValidator(self.Mask)
            dlg.Y_coordinate.setValidator(self.Mask)
            dlg.show()
            if dlg.exec_():
                table2 = self.Entiteis_Point_Style
                self.File.Points.editTable(table1, dlg.Point.currentText(),
                    dlg.X_coordinate.text() if not dlg.X_coordinate.text()in["", "n", "-"] else dlg.X_coordinate.placeholderText(),
                    dlg.Y_coordinate.text() if not dlg.Y_coordinate.text()in["", "n", "-"] else dlg.Y_coordinate.placeholderText(),
                    dlg.Fix_Point.checkState(), True)
                self.File.Points.styleFix(table2, dlg.Point.currentText(), dlg.Fix_Point.checkState())
                self.Resolve()
                self.Workbook_noSave()
    point_feedback = pyqtSignal(float, float, bool)
    @pyqtSlot(int)
    def Change_Edit_Point(self, pos):
        table = self.Entiteis_Point
        x = float(table.item(pos, 1).text())
        y = float(table.item(pos, 2).text())
        fix = table.item(pos, 3).checkState()
        self.point_feedback.emit(x, y, fix)
    
    @pyqtSlot()
    def on_action_New_Line_triggered(self):
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            dlg  = New_link()
            for i in range(table1.rowCount()):
                dlg.Start_Point.insertItem(i, icon, table1.item(i, 0).text())
                dlg.End_Point.insertItem(i, icon, table1.item(i, 0).text())
            table2 = self.Entiteis_Link
            dlg.Link_num.insertPlainText("Line"+str(table2.rowCount()))
            dlg.Length.setValidator(self.Mask)
            dlg.show()
            if dlg.exec_():
                a = dlg.Start_Point.currentText()
                b = dlg.End_Point.currentText()
                if self.File.Lines.repeatedCheck(table2, a, b): self.on_action_New_Line_triggered()
                elif a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_New_Line_triggered()
                else:
                    self.File.Lines.editTable(table2, dlg.Link_num.toPlainText(),
                        dlg.Start_Point.currentText(), dlg.End_Point.currentText(),
                        dlg.Length.text()if not dlg.Length.text()in["", "n"] else dlg.Length.placeholderText(), False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionEdit_Linkage_triggered(self, pos = 0):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
            dlg  = edit_link_show()
            for i in range(table1.rowCount()):
                dlg.Start_Point.insertItem(i, icon1, table1.item(i, 0).text())
                dlg.End_Point.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Link.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.Another_line.connect(self.Change_Edit_Line)
            self.link_feedback.connect(dlg.change_feedback)
            dlg.Link.setCurrentIndex(pos)
            self.Change_Edit_Line(pos)
            dlg.Length.setValidator(self.Mask)
            dlg.show()
            if dlg.exec_():
                a = dlg.Start_Point.currentText()
                b = dlg.End_Point.currentText()
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_actionEdit_Linkage_triggered()
                else:
                    self.File.Lines.editTable(table2, dlg.Link.currentText(),
                        dlg.Start_Point.currentText(),  dlg.End_Point.currentText(),
                        dlg.Length.text() if not dlg.Length.text()in["", "n"] else dlg.Length.placeholderText(), True)
                    self.Resolve()
                    self.Workbook_noSave()
    link_feedback = pyqtSignal(int, int, float)
    @pyqtSlot(int)
    def Change_Edit_Line(self, pos):
        table = self.Entiteis_Link
        start = int(table.item(pos, 1).text().replace("Point", ""))
        end = int(table.item(pos, 2).text().replace("Point", ""))
        len = float(table.item(pos, 3).text())
        self.link_feedback.emit(start, end, len)
    
    @pyqtSlot()
    def on_action_New_Stay_Chain_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 2):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = chain_show()
            table2 = self.Entiteis_Stay_Chain
            for i in range(table1.rowCount()):
                dlg.Point1.insertItem(i, icon, table1.item(i, 0).text())
                dlg.Point2.insertItem(i, icon, table1.item(i, 0).text())
                dlg.Point3.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Chain_num.insertPlainText("Chain"+str(table2.rowCount()))
            dlg.p1_p2.setValidator(self.Mask)
            dlg.p2_p3.setValidator(self.Mask)
            dlg.p1_p3.setValidator(self.Mask)
            dlg.show()
            if dlg.exec_():
                p1 = dlg.Point1.currentText()
                p2 = dlg.Point2.currentText()
                p3 = dlg.Point3.currentText()
                if (p1 == p2) | (p2 == p3) | (p1 == p3):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_New_Stay_Chain_triggered()
                else:
                    self.File.Chains.editTable(table2, dlg.Chain_num.toPlainText(),
                        p1, p2, p3,
                        dlg.p1_p2.text() if not dlg.p1_p2.text()in["", "n"] else dlg.p1_p2.placeholderText(),
                        dlg.p2_p3.text() if not dlg.p2_p3.text()in["", "n"] else dlg.p2_p3.placeholderText(),
                        dlg.p1_p3.text() if not dlg.p1_p3.text()in["", "n"] else dlg.p1_p3.placeholderText(), False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionEdit_Stay_Chain_triggered(self, pos = 0):
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/icons/equal.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Stay_Chain
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_stay_chain_show()
            for i in range(table1.rowCount()):
                dlg.Point1.insertItem(i, icon1, table1.item(i, 0).text())
                dlg.Point2.insertItem(i, icon1, table1.item(i, 0).text())
                dlg.Point3.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Chain.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.Another_chain.connect(self.Change_Edit_Chain)
            self.chain_feedback.connect(dlg.change_feedback)
            dlg.Chain.setCurrentIndex(pos)
            self.Change_Edit_Chain(pos)
            dlg.p1_p2.setValidator(self.Mask)
            dlg.p2_p3.setValidator(self.Mask)
            dlg.p1_p3.setValidator(self.Mask)
            dlg.show()
            if dlg.exec_():
                p1 = dlg.Point1.currentText()
                p2 = dlg.Point2.currentText()
                p3 = dlg.Point3.currentText()
                if (p1 == p2) | (p2 == p3) | (p1 == p3):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_actionEdit_Stay_Chain_triggered()
                else:
                    self.File.Chains.editTable(table2, dlg.Chain.currentText(), p1, p2, p3,
                        dlg.p1_p2.text() if not dlg.p1_p2.text()in["", "n"] else dlg.p1_p2.placeholderText(),
                        dlg.p2_p3.text() if not dlg.p2_p3.text()in["", "n"] else dlg.p2_p3.placeholderText(),
                        dlg.p1_p3.text() if not dlg.p1_p3.text()in["", "n"] else dlg.p1_p3.placeholderText(), True)
                    self.Resolve()
                    self.Workbook_noSave()
    chain_feedback = pyqtSignal(int, int, int, float, float, float)
    @pyqtSlot(int)
    def Change_Edit_Chain(self, pos):
        table = self.Entiteis_Stay_Chain
        Point1 = int(table.item(pos, 1).text().replace("Point", ""))
        Point2 = int(table.item(pos, 2).text().replace("Point", ""))
        Point3 = int(table.item(pos, 3).text().replace("Point", ""))
        p1_p2 = float(table.item(pos, 4).text())
        p2_p3 = float(table.item(pos, 5).text())
        p1_p3 = float(table.item(pos, 6).text())
        self.chain_feedback.emit(Point1, Point2, Point3, p1_p2, p2_p3, p1_p3)
    
    @pyqtSlot()
    def on_action_Set_Drive_Shaft_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Drive_Shaft
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = shaft_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Shaft_Center.insertItem(i, icon, table1.item(i, 0).text())
                dlg.References.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Shaft_num.insertPlainText("Shaft"+str(table2.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Shaft_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.Start_Angle.text()
                d = dlg.End_Angle.text()
                if dlg.Demo_angle_enable.checkState(): e = dlg.Demo_angle.text()
                else: e = None
                if (a == b) or (c == d):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    self.File.Shafts.editTable(table2, dlg.Shaft_num.toPlainText(), a, b, c, d, e, False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Edit_Drive_Shaft_triggered(self, pos = 0):
        table1 = self.Entiteis_Point
        table2 = self.Drive_Shaft
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_shaft_show()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Shaft_Center.insertItem(i, icon1, table1.item(i, 0).text())
                dlg.References.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Shaft.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.Another_shaft.connect(self.Change_Edit_Shaft)
            self.shaft_feedback.connect(dlg.change_feedback)
            dlg.Shaft.setCurrentIndex(pos)
            self.Change_Edit_Shaft(pos)
            dlg.show()
            if dlg.exec_():
                a = dlg.Shaft_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.Start_Angle.text()
                d = dlg.End_Angle.text()
                if (a == b) or (c == d):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    self.File.Shafts.editTable(table2, dlg.Shaft.currentText(), a, b, c, d, table2.item(dlg.Shaft.currentIndex(), 5), True)
                    self.Resolve()
                    self.Workbook_noSave()
    shaft_feedback = pyqtSignal(int, int, float, float)
    @pyqtSlot(int)
    def Change_Edit_Shaft(self, pos):
        table = self.Drive_Shaft
        center = int(table.item(pos, 1).text().replace("Point", ""))
        references = int(table.item(pos, 2).text().replace("Point", ""))
        start = float(table.item(pos, 3).text())
        end = float(table.item(pos, 4).text())
        self.shaft_feedback.emit(center, references, start, end)
    
    @pyqtSlot()
    def on_action_Set_Slider_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        table3 = self.Slider
        if (table2.rowCount() <= 0) and (table1.rowCount() <= 2):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = slider_show()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Slider_Center.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.References.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.Slider_num.insertPlainText("Slider"+str(table3.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Slider_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.References.currentIndex()
                if (table2.item(c, 1).text()==a) or (table2.item(c, 2).text()==a):
                    dlg = restriction_conflict_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Slider_triggered()
                else:
                    self.File.Sliders.editTable(table3, dlg.Slider_num.toPlainText(), a, b, False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Edit_Slider_triggered(self, pos):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        table3 = self.Slider
        if (table3.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_slider_show()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
            icon3 = QIcon()
            icon3.addPixmap(QPixmap(":/icons/pointonx.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()): dlg.Slider_Center.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()): dlg.References.insertItem(i, icon2, table2.item(i, 0).text())
            for i in range(table3.rowCount()): dlg.Slider.insertItem(i, icon3, table3.item(i, 0).text())
            dlg.Another_slider.connect(self.Change_Edit_Slider)
            self.slider_feedback.connect(dlg.change_feedback)
            dlg.Slider.setCurrentIndex(pos)
            self.Change_Edit_Slider(pos)
            dlg.show()
            if dlg.exec_():
                a = dlg.Slider_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.References.currentIndex()
                if (table2.item(c, 1).text()==a) or (table2.item(c, 2).text()==a):
                    dlg = restriction_conflict_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Edit_Slider_triggered()
                else:
                    self.File.Sliders.editTable(table3, dlg.Slider.currentText(), a, b, True)
                    self.Resolve()
                    self.Workbook_noSave()
    slider_feedback = pyqtSignal(int, int)
    @pyqtSlot(int)
    def Change_Edit_Slider(self, pos):
        table = self.Slider
        point = int(table.item(pos, 1).text().replace("Ponit", ""))
        line = int(table.item(pos, 2).text().replace("Line", ""))
        self.slider_feedback.emit(point, line)
    
    @pyqtSlot()
    def on_action_Set_Rod_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = rod_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Start.insertItem(i, icon, table1.item(i, 0).text())
                dlg.End.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Rod_num.insertPlainText("Rod"+str(table2.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Start.currentText()
                b = dlg.End.currentText()
                c = str(min(float(dlg.len1.text()), float(dlg.len2.text())))
                d = str(max(float(dlg.len1.text()), float(dlg.len2.text())))
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    self.File.Rods.editTable(table2, dlg.Rod_num.toPlainText(), a, b, c, d, False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Edit_Piston_Spring_triggered(self, pos = 0):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_rod_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Start.insertItem(i, icon, table1.item(i, 0).text())
                dlg.End.insertItem(i, icon, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Rod.insertItem(i, icon, table2.item(i, 0).text())
            dlg.Another_rod.connect(self.Change_Edit_Rod)
            self.rod_feedback.connect(dlg.change_feedback)
            dlg.Rod.setCurrentIndex(pos)
            self.Change_Edit_Rod(pos)
            dlg.show()
            if dlg.exec_():
                a = dlg.Start.currentText()
                b = dlg.End.currentText()
                c = str(min(float(dlg.len1.text()), float(dlg.len2.text())))
                d = str(max(float(dlg.len1.text()), float(dlg.len2.text())))
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    self.File.Rods.editTable(table2, dlg.Rod.currentText(), a, b, c, d, True)
                    self.Resolve()
                    self.Workbook_noSave()
    rod_feedback = pyqtSignal(int, int, int, float)
    @pyqtSlot(int)
    def Change_Edit_Rod(self, pos):
        table = self.Rod
        center = int(table.item(pos, 1).text().replace("Point", ""))
        start = int(table.item(pos, 2).text().replace("Point", ""))
        end = int(table.item(pos, 3).text().replace("Point", ""))
        position = float(table.item(pos, 4).text())
        self.rod_feedback.emit(center, start, end, position)
    
    @pyqtSlot()
    def on_actionDelete_Point_triggered(self, pos = 1):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        table = self.Entiteis_Point
        if table.rowCount() <= 1:
            dlg = kill_origin_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = delete_point_show()
            for i in range(1, table.rowCount()):
                dlg.Entity.insertItem(i, icon, table.item(i, 0).text())
            dlg.Entity.setCurrentIndex(pos-1)
            dlg.show()
            if dlg.exec_():
                self.File.Points.deleteTable(table,
                    self.Entiteis_Point_Style, self.Entiteis_Link,
                    self.Entiteis_Stay_Chain, self.Drive_Shaft,
                    self.Slider, self.Rod, dlg)
                self.Resolve()
                self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Linkage_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Link
        table2 = self.Slider
        if table1.rowCount() <= 0:
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = delete_linkage_show()
            for i in range(table1.rowCount()):
                dlg.Entity.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Entity.setCurrentIndex(pos)
            dlg.show()
            if dlg.exec_():
                self.File.Lines.deleteTable(table1, table2, dlg)
                self.Resolve()
                self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Stay_Chain_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/equal.png"), QIcon.Normal, QIcon.Off)
        self.File.delTable(self.Entiteis_Stay_Chain, icon, delete_chain_show(), "Chain", pos)
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Drive_Shaft_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
        self.File.delTable(self.Drive_Shaft, icon, delete_shaft_show(), "Shaft", pos)
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Slider_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/pointonx.png"), QIcon.Normal, QIcon.Off)
        self.File.delTable(self.Slider, icon, delete_slider_show(), "Slider", pos)
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Piston_Spring_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/spring.png"), QIcon.Normal, QIcon.Off)
        self.File.delTable(self.Rod, icon, delete_rod_show(), "Rod", pos)
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_ResetCanvas_clicked(self):
        self.ZoomBar.setValue(self.Default_canvas_view)
        self.qpainterWindow.points['origin']['x'] = self.qpainterWindow.width()/2
        self.qpainterWindow.points['origin']['y'] = self.qpainterWindow.height()/2
        self.Reload_Canvas()
    @pyqtSlot()
    def on_FitW_clicked(self):
        self.Fit2H()
        self.Fit2W()
    def Fit2W(self):
        for i in range(10):
            max_pt = max(self.qpainterWindow.points['x'])
            min_pt = min(self.qpainterWindow.points['x'])
            self.qpainterWindow.points['origin']['x'] = (self.qpainterWindow.width()-(max_pt+min_pt))/2
            self.ZoomBar.setValue(self.ZoomBar.value()*self.qpainterWindow.width()/(max_pt+min_pt+100))
            self.Reload_Canvas()
    @pyqtSlot()
    def on_FitH_clicked(self):
        self.Fit2W()
        self.Fit2H()
    def Fit2H(self):
        for i in range(10):
            max_pt = max(self.qpainterWindow.points['y'])
            min_pt = min(self.qpainterWindow.points['y'])
            self.qpainterWindow.points['origin']['y'] = (self.qpainterWindow.height()-(max_pt+min_pt))/2
            self.ZoomBar.setValue(self.ZoomBar.value()*self.qpainterWindow.height()/(max_pt-min_pt+100))
            self.Reload_Canvas()
    @pyqtSlot(int)
    def on_ZoomBar_valueChanged(self, value):
        self.ZoomText.setPlainText(str(value)+"%")
        self.Reload_Canvas()
    #Wheel Event
    def wheelEvent(self, event):
        if self.mapFromGlobal(QCursor.pos()).x()>=470:
            if event.angleDelta().y()>0: self.ZoomBar.setValue(self.ZoomBar.value()+10)
            if event.angleDelta().y()<0: self.ZoomBar.setValue(self.ZoomBar.value()-10)
    
    @pyqtSlot()
    def on_actionReload_Drawing_triggered(self): self.Resolve()
    @pyqtSlot(QTableWidgetItem)
    def on_Entiteis_Point_Style_itemChanged(self, item):
        self.Reload_Canvas()
        self.Workbook_noSave()
    @pyqtSlot(int)
    def on_LineWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(int)
    def on_PathWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_actionDisplay_Dimensions_toggled(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_actionDisplay_Point_Mark_toggled(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_action_Black_Blackground_toggled(self, p0): self.Reload_Canvas()
    @pyqtSlot(int)
    def Point_Style_set(self, index): self.Reload_Canvas()
    @pyqtSlot()
    def on_Path_data_show_clicked(self):
        self.qpainterWindow.Path['show'] = self.Path_data_show.checkState()
        self.Reload_Canvas()
    
    @pyqtSlot()
    def on_PathTrack_clicked(self):
        table1 = self.Entiteis_Point
        dlg = Path_Track_show()
        self.actionDisplay_Point_Mark.setChecked(True)
        for i in range(table1.rowCount()):
            if not table1.item(i, 3).checkState(): dlg.Point_list.addItem(table1.item(i, 0).text())
        if dlg.Point_list.count()==0:
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg.Entiteis_Point = self.Entiteis_Point
            dlg.Entiteis_Link = self.Entiteis_Link
            dlg.Entiteis_Stay_Chain = self.Entiteis_Stay_Chain
            dlg.Drive_Shaft = self.Drive_Shaft
            dlg.Slider = self.Slider
            dlg.Rod = self.Rod
            dlg.Parameter_list = self.Parameter_list
            dlg.show()
            if dlg.exec_():
                self.File.Path.runList = []
                for i in range(dlg.Run_list.count()): self.File.Path.runList += [dlg.Run_list.item(i).text()]
                self.File.Path.data = dlg.Path_data
                self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">Path Data Exist</span></p></body></html>"))
                self.Path_Clear.setEnabled(True)
                self.Path_coordinate.setEnabled(True)
                self.Path_data_show.setEnabled(True)
                self.qpainterWindow.path_track(self.File.Path.data, self.File.Path.runList)
    @pyqtSlot()
    def on_Path_Clear_clicked(self):
        self.qpainterWindow.removePath()
        self.Reload_Canvas()
        self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">No Path Data</span></p></body></html>"))
        self.Path_Clear.setEnabled(False)
        self.Path_coordinate.setEnabled(False)
        self.Path_data_show.setEnabled(False)
    @pyqtSlot()
    def on_Path_coordinate_clicked(self):
        dlg = path_point_data_show()
        self.File.Path.setup(dlg.path_data, self.File.Path.data, self.File.Path.runList)
        dlg.show()
        dlg.exec()
    
    @pyqtSlot()
    def on_Drive_clicked(self):
        if not hasattr(self, 'DriveWidget'):
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
            self.DriveWidget = Drive_show()
            for i in range(self.Drive_Shaft.rowCount()): self.DriveWidget.Shaft.insertItem(i, icon, self.Drive_Shaft.item(i, 0).text())
            self.mplLayout.insertWidget(1, self.DriveWidget)
            self.DriveWidget.Degree_change.connect(self.Change_demo_angle)
            self.DriveWidget.Shaft_change.connect(self.Shaft_limit)
            self.Shaft_limit(0)
        else:
            try:
                self.DriveWidget.deleteLater()
                del self.DriveWidget
            except: pass
    @pyqtSlot(int)
    def Shaft_limit(self, pos):
        try:
            self.DriveWidget.Degree.setMinimum(int(float(self.Drive_Shaft.item(pos, 3).text()))*100)
            self.DriveWidget.Degree.setMaximum(int(float(self.Drive_Shaft.item(pos, 4).text()))*100)
            self.DriveWidget.Degree.setValue(int(float(self.Drive_Shaft.item(pos, 5).text()))*100)
        except: self.DriveWidget.Degree.setValue(int((self.DriveWidget.Degree.maximum()+self.DriveWidget.Degree.minimum())/2))
        self.DriveWidget.Degree_text.setValue(float(self.DriveWidget.Degree.value()/100))
    @pyqtSlot(int, float)
    def Change_demo_angle(self, shaft_int, angle):
        self.Drive_Shaft.setItem(shaft_int, 5, QTableWidgetItem(str(angle)))
        self.Resolve()
    
    @pyqtSlot()
    def on_Measurement_clicked(self):
        if not hasattr(self, 'MeasurementWidget'):
            table = self.Entiteis_Point
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            self.MeasurementWidget = Measurement_show()
            for i in range(table.rowCount()):
                self.MeasurementWidget.Start.insertItem(i, icon, table.item(i, 0).text())
                self.MeasurementWidget.End.insertItem(i, icon, table.item(i, 0).text())
            self.mplLayout.insertWidget(1, self.MeasurementWidget)
            self.qpainterWindow.change_event.connect(self.MeasurementWidget.Detection_do)
            self.actionDisplay_Dimensions.setChecked(True)
            self.actionDisplay_Point_Mark.setChecked(True)
            self.qpainterWindow.mouse_track.connect(self.MeasurementWidget.show_mouse_track)
            self.MeasurementWidget.point_change.connect(self.distance_solving)
            self.distance_changed.connect(self.MeasurementWidget.change_distance)
            self.MeasurementWidget.Mouse.setPlainText("Detecting")
        else:
            try:
                self.MeasurementWidget.deleteLater()
                del self.MeasurementWidget
            except: pass
    distance_changed = pyqtSignal(float)
    @pyqtSlot(int, int)
    def distance_solving(self, start, end):
        start = self.Entiteis_Point.item(start, 4).text().replace("(", "").replace(")", "")
        end = self.Entiteis_Point.item(end, 4).text().replace("(", "").replace(")", "")
        x = float(start.split(", ")[0])-float(end.split(", ")[0])
        y = float(start.split(", ")[1])-float(end.split(", ")[1])
        self.distance_changed.emit(round(math.sqrt(x**2+y**2), 9))
    
    @pyqtSlot()
    def on_AuxLine_clicked(self):
        if not hasattr(self, 'AuxLineWidget'):
            self.qpainterWindow.AuxLine['show'] = True
            self.qpainterWindow.AuxLine['horizontal'] = True
            self.qpainterWindow.AuxLine['vertical'] = True
            table = self.Entiteis_Point
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            self.AuxLineWidget = AuxLine_show()
            for i in range(table.rowCount()): self.AuxLineWidget.Point.insertItem(i, icon, table.item(i, 0).text())
            for i in range(len(self.qpainterWindow.re_Color)): self.AuxLineWidget.Color.insertItem(i, self.qpainterWindow.re_Color[i])
            for i in range(len(self.qpainterWindow.re_Color)): self.AuxLineWidget.Color_l.insertItem(i, self.qpainterWindow.re_Color[i])
            self.AuxLineWidget.Point.setCurrentIndex(self.qpainterWindow.AuxLine['pt'])
            self.AuxLineWidget.Color.setCurrentIndex(self.qpainterWindow.AuxLine['color'])
            self.AuxLineWidget.Color_l.setCurrentIndex(self.qpainterWindow.AuxLine['limit_color'])
            self.AuxLineWidget.Point_change.connect(self.draw_Auxline)
            self.mplLayout.insertWidget(1, self.AuxLineWidget)
        else:
            self.qpainterWindow.AuxLine['show'] = False
            try:
                self.AuxLineWidget.deleteLater()
                del self.AuxLineWidget
            except: pass
        self.Reload_Canvas()
    @pyqtSlot(int, int, int, bool, bool, bool, bool, bool)
    def draw_Auxline(self, pt, color, color_l, axe_H, axe_V, max_l, min_l, pt_change):
        self.qpainterWindow.AuxLine['pt'] = pt
        self.qpainterWindow.AuxLine['color'] = color
        self.qpainterWindow.AuxLine['limit_color'] = color_l
        if pt_change:
            self.qpainterWindow.Reset_Aux_limit()
            self.Reload_Canvas()
        self.qpainterWindow.AuxLine['horizontal'] = axe_H
        self.qpainterWindow.AuxLine['vertical'] = axe_V
        self.qpainterWindow.AuxLine['isMax'] = max_l
        self.qpainterWindow.AuxLine['isMin'] = min_l
        self.Reload_Canvas()
    def reset_Auxline(self):
        self.qpainterWindow.AuxLine['Max']['x'] = 0
        self.qpainterWindow.AuxLine['Max']['y'] = 0
        self.qpainterWindow.AuxLine['Min']['x'] = 0
        self.qpainterWindow.AuxLine['Min']['y'] = 0
        self.qpainterWindow.AuxLine['pt'] = 0
        self.qpainterWindow.AuxLine['color'] = 6
        self.qpainterWindow.AuxLine['limit_color'] = 8
    
    def Mask_Change(self):
        row_Count = str(self.Parameter_list.rowCount()-1)
        param = '(('
        for i in range(len(row_Count)): param += '[1-'+row_Count[i]+']' if i==0 and not len(row_Count)<=1 else '[0-'+row_Count[i]+']'
        param += ')|'
        param_100 = '[0-9]{0,'+str(len(row_Count)-2)+'}' if len(row_Count)>2 else ''
        param_20 = '([1-'+str(int(row_Count[0])-1)+']'+param_100+')?' if self.Parameter_list.rowCount()>19 else ''
        if len(row_Count)>1: param += param_20+'[0-9]'
        param += ')'
        param_use = '^[n]'+param+'$|' if self.Parameter_list.rowCount()>=1 else ''
        mask = '('+param_use+'^[-]?([1-9][0-9]{0,'+str(self.Default_Bits-2)+'})?[0-9][.][0-9]{1,'+str(self.Default_Bits)+'}$)'
        self.Mask = QRegExpValidator(QRegExp(mask))
        self.X_coordinate.setValidator(self.Mask)
        self.Y_coordinate.setValidator(self.Mask)
    
    @pyqtSlot(int, int, int, int)
    def on_Parameter_list_currentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        try:
            self.Parameter_num.setPlainText("n"+str(currentRow))
            self.Parameter_digital.setPlaceholderText(str(self.Parameter_list.item(currentRow, 1).text()))
            self.Parameter_digital.clear()
        except:
            self.Parameter_num.setPlainText("N/A")
            self.Parameter_digital.setPlaceholderText("0.0")
            self.Parameter_digital.clear()
        self.Parameter_num.setEnabled(self.Parameter_list.rowCount()>0 and currentRow>-1)
        self.Parameter_digital.setEnabled(self.Parameter_list.rowCount()>0 and currentRow>-1)
        self.Parameter_lable.setEnabled(self.Parameter_list.rowCount()>0 and currentRow>-1)
        self.Parameter_update.setEnabled(self.Parameter_list.rowCount()>0 and currentRow>-1)
    
    @pyqtSlot()
    def on_Parameter_update_clicked(self):
        try: self.Parameter_list.setItem(self.Parameter_list.currentRow(), 1, QTableWidgetItem(self.Parameter_digital.text() if self.Parameter_digital.text() else Parameter_digital.placeholderText()))
        except: pass
    
    @pyqtSlot(int, int, int, int)
    def on_Entiteis_Point_currentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        self.X_coordinate.setPlaceholderText(self.Entiteis_Point.item(currentRow, 1).text())
        self.Y_coordinate.setPlaceholderText(self.Entiteis_Point.item(currentRow, 2).text())
    
    @pyqtSlot(int, int)
    def on_Parameter_list_cellChanged(self, row, column):
        if column in [1, 2]: self.Parameter_list.item(row, column).setToolTip(self.Parameter_list.item(row, column).text())
    
    @pyqtSlot()
    def on_action_Prefenece_triggered(self):
        dlg = options_show()
        color_list = self.qpainterWindow.re_Color
        for i in range(len(color_list)): dlg.LinkingLinesColor.insertItem(i, color_list[i])
        for i in range(len(color_list)): dlg.StayChainColor.insertItem(i, color_list[i])
        for i in range(len(color_list)): dlg.AuxiliaryLineColor.insertItem(i, color_list[i])
        for i in range(len(color_list)): dlg.AuxiliaryLimitLineColor.insertItem(i, color_list[i])
        for i in range(len(color_list)): dlg.TextColor.insertItem(i, color_list[i])
        dlg.show()
        if dlg.exec_(): pass
    
    @pyqtSlot()
    def on_symmetrical_part_clicked(self):
        self.sym_part = self.symmetrical_part.isChecked()
        self.Resolve()
