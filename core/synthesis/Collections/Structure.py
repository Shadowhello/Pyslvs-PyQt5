# -*- coding: utf-8 -*-

"""The widget of 'Structure' tab."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    List,
    Tuple,
    Optional,
)
from networkx import Graph, is_isomorphic
from core.QtModules import (
    pyqtSignal,
    pyqtSlot,
    Qt,
    QMessageBox,
    QProgressDialog,
    QCoreApplication,
    QListWidgetItem,
    QInputDialog,
    QImage,
    QSize,
    QColor,
    QWidget,
    QPainter,
    QPointF,
    QPixmap,
    QFileInfo,
    QApplication,
)
from core.io import QTIMAGES
from core.graphics import (
    graph,
    engine_picker,
    engines,
    EngineError,
)
from .Ui_Structure import Ui_Form


class _TestError(Exception):
    """Error raise while add a graphs."""
    pass


class StructureWidget(QWidget, Ui_Form):
    
    """Structure widget.
    
    Preview the structures that was been added in collection list by user.
    """
    
    layout_sender = pyqtSignal(Graph, dict)
    
    def __init__(self, parent: QWidget):
        """Get IO dialog functions from parent."""
        super(StructureWidget, self).__init__(parent)
        self.setupUi(self)
        self.outputTo = parent.outputTo
        self.saveReplyBox = parent.saveReplyBox
        self.inputFrom = parent.inputFrom
        self.addPointsByGraph = parent.addPointsByGraph
        self.unsaveFunc = parent.workbookNoSave
        
        """Data structures."""
        self.collections = []
        self.collections_layouts = []
        self.collections_grounded = []
        
        """Engine list."""
        self.graph_engine.addItems(engines)
        self.graph_engine.setCurrentIndex(2)
        self.graph_engine.currentIndexChanged.connect(self.__reloadAtlas)
    
    def __clearSelection(self):
        """Clear the selection preview data."""
        self.grounded_list.clear()
        self.selection_window.clear()
        self.expr_edges.clear()
        self.NL.setText('0')
        self.NJ.setText('0')
        self.DOF.setText('0')
    
    def clear(self):
        """Clear all sub-widgets."""
        self.grounded_merge.setEnabled(False)
        self.triangle_button.setEnabled(False)
        self.collections.clear()
        self.collection_list.clear()
        self.__clearSelection()
    
    @pyqtSlot(name='on_clear_button_clicked')
    def __userClear(self):
        """Ask user before clear."""
        if not self.collections:
            return
        reply = QMessageBox.question(self,
            "Delete",
            "Sure to remove all your collections?"
        )
        if reply != QMessageBox.Yes:
            return
        self.clear()
        self.unsaveFunc()
    
    def __engineErrorMsg(self, e: EngineError):
        """Show up error message."""
        QMessageBox.warning(self,
            str(e),
            "Please install and make sure Graphviz is working."
        )
    
    @pyqtSlot(name='on_reload_atlas_clicked')
    @pyqtSlot(int)
    def __reloadAtlas(self, p0: Optional[int] = None):
        """Reload atlas with the engine."""
        if not self.collections:
            return
        self.collections_layouts.clear()
        self.collection_list.clear()
        self.selection_window.clear()
        self.expr_edges.clear()
        self.NL.setText('0')
        self.NJ.setText('0')
        self.DOF.setText('0')
        self.grounded_list.clear()
        progdlg = QProgressDialog(
            "Drawing atlas...",
            "Cancel",
            0,
            len(self.collections),
            self
        )
        progdlg.setAttribute(Qt.WA_DeleteOnClose, True)
        progdlg.setWindowTitle("Type synthesis")
        progdlg.resize(400, progdlg.height())
        progdlg.setModal(True)
        progdlg.show()
        engineSTR = self.graph_engine.currentText().split(" - ")[1]
        for i, G in enumerate(self.collections):
            QCoreApplication.processEvents()
            if progdlg.wasCanceled():
                return
            item = QListWidgetItem("No. {}".format(i+1))
            try:
                engine = engine_picker(G, engineSTR)
                item.setIcon(graph(
                    G,
                    self.collection_list.iconSize().width(),
                    engine
                ))
            except EngineError as e:
                progdlg.setValue(progdlg.maximum())
                self.__engineErrorMsg(e)
                break
            else:
                self.collections_layouts.append(engine)
                item.setToolTip(
                    "{}\nUse the right-click menu to operate.".format(G.edges)
                )
                self.collection_list.addItem(item)
                progdlg.setValue(i+1)
    
    def addCollection(self, edges: Tuple[Tuple[int, int]]):
        """Add collection by in put edges."""
        G = Graph(edges)
        try:
            if not edges:
                raise _TestError("is empty graph.")
            for n in G.nodes:
                if len(list(G.neighbors(n)))<2:
                    raise _TestError("is not close chain")
            for H in self.collections:
                if is_isomorphic(G, H):
                    raise _TestError("is isomorphic")
        except _TestError as e:
            QMessageBox.warning(self, "Add Collection Error", "Error: {}".format(e))
            return
        self.collections.append(G)
        self.unsaveFunc()
        self.__reloadAtlas()
    
    def addCollections(self, collections: List[Tuple[Tuple[int, int]]]):
        """Add collections."""
        for c in collections:
            self.addCollection(c)
    
    @pyqtSlot(name='on_add_by_edges_button_clicked')
    def __addFromEdges(self):
        """Add collection by input string."""
        edgesSTR = ""
        while not edgesSTR:
            edgesSTR, ok = QInputDialog.getText(
                self,
                "Add by edges",
                "Please enter a connection expression:\n" +
                "Example: [(0, 1), (1, 2), (2, 3), (3, 0)]"
            )
            if not ok:
                return
        try:
            edges = eval(edgesSTR)
            if any(len(edge)!=2 for edge in edges):
                raise IOError("Wrong format")
        except Exception as e:
            QMessageBox.warning(self, str(e), "Error: {}".format(e))
            return
        else:
            self.addCollection(edges)
    
    @pyqtSlot(name='on_add_by_files_button_clicked')
    def __addFromFiles(self):
        """Append atlas by text files."""
        file_names = self.inputFrom(
            "Edges data",
            ["Text File (*.txt)"],
            multiple=True
        )
        if not file_names:
            return
        read_data = []
        for file_name in file_names:
            with open(file_name, 'r') as f:
                for line in f:
                    read_data.append(line[:-1])
        collections = []
        for edges in read_data:
            try:
                collections.append(Graph(eval(edges)))
            except:
                QMessageBox.warning(self,
                    "Wrong format",
                    "Please check the edges text format."
                )
                return
        if not collections:
            return
        self.collections += collections
        self.__reloadAtlas()
    
    @pyqtSlot(name='on_save_atlas_clicked')
    def __saveAtlas(self):
        """Save function as same as type synthesis widget."""
        count = self.collection_list.count()
        if not count:
            return
        lateral, ok = QInputDialog.getInt(self,
            "Atlas",
            "The number of lateral:",
            5, 1, 10
        )
        if not ok:
            return
        file_name = self.outputTo("Atlas image", QTIMAGES)
        if not file_name:
            return
        icon_size = self.collection_list.iconSize()
        width = icon_size.width()
        image_main = QImage(
            QSize(
                lateral * width if count>lateral else count * width,
                ((count // lateral) + bool(count % lateral)) * width
            ),
            self.collection_list.item(0).icon().pixmap(icon_size).toImage().format()
        )
        image_main.fill(QColor(Qt.white).rgb())
        painter = QPainter(image_main)
        for row in range(count):
            image = self.collection_list.item(row).icon().pixmap(icon_size).toImage()
            painter.drawImage(QPointF(
                row % lateral * width,
                row // lateral * width
            ), image)
        painter.end()
        pixmap = QPixmap()
        pixmap.convertFromImage(image_main)
        pixmap.save(file_name, format=QFileInfo(file_name).suffix())
        self.saveReplyBox("Atlas", file_name)
    
    @pyqtSlot(name='on_save_edges_clicked')
    def __saveEdges(self):
        """Save function as same as type synthesis widget."""
        count = self.collection_list.count()
        if not count:
            return
        file_name = self.outputTo("Atlas edges expression", ["Text file (*.txt)"])
        if not file_name:
            return
        with open(file_name, 'w') as f:
            f.write('\n'.join(str(G.edges) for G in self.collections))
        self.saveReplyBox("edges expression", file_name)
    
    @pyqtSlot(
        QListWidgetItem,
        QListWidgetItem,
        name='on_collection_list_currentItemChanged')
    def __reloadDetails(self, item: QListWidgetItem, p0: QListWidgetItem):
        """Show the data of collection.
        
        Save the layout position to keep the graphs
        will be in same appearance.
        """
        has_item = bool(item)
        self.delete_button.setEnabled(has_item)
        self.grounded_button.setEnabled(has_item)
        self.triangle_button.setEnabled(has_item)
        if not item:
            return
        self.selection_window.clear()
        item_ = QListWidgetItem(item.text())
        row = self.collection_list.row(item)
        G = self.collections[row]
        self.ground_engine = self.collections_layouts[row]
        item_.setIcon(graph(
            G,
            self.selection_window.iconSize().width(),
            self.ground_engine
        ))
        self.selection_window.addItem(item_)
        self.expr_edges.setText(str(list(G.edges)))
        self.NL.setText(str(len(G.nodes)))
        self.NJ.setText(str(len(G.edges)))
        self.DOF.setText(str(3*(int(self.NL.text())-1) - 2*int(self.NJ.text())))
    
    @pyqtSlot(name='on_expr_copy_clicked')
    def __copyExpr(self):
        """Copy the expression."""
        string = self.expr_edges.text()
        if string:
            QApplication.clipboard().setText(string)
            self.expr_edges.selectAll()
    
    @pyqtSlot(name='on_delete_button_clicked')
    def __deleteCollection(self):
        """Delete the selected collection."""
        row = self.collection_list.currentRow()
        if not row > -1:
            return
        reply = QMessageBox.question(self,
            "Delete",
            "Sure to remove #{} from your collections?".format(row)
        )
        if reply != QMessageBox.Yes:
            return
        self.__clearSelection()
        self.collection_list.takeItem(row)
        del self.collections[row]
        self.unsaveFunc()
    
    @pyqtSlot(name='on_triangle_button_clicked')
    def __triangulation(self):
        """Triangular iteration."""
        self.layout_sender.emit(
            self.collections[self.collection_list.currentRow()],
            self.ground_engine
        )
    
    @pyqtSlot(name='on_grounded_button_clicked')
    def __grounded(self):
        """Grounded combinations."""
        current_item = self.collection_list.currentItem()
        self.collections_grounded.clear()
        self.grounded_list.clear()
        G = self.collections[self.collection_list.row(current_item)]
        item = QListWidgetItem("Released")
        try:
            icon = graph(
                G,
                self.grounded_list.iconSize().width(),
                self.ground_engine
            )
        except EngineError as e:
            self.__engineErrorMsg(e)
            return
        item.setIcon(icon)
        self.collections_grounded.append(G)
        self.grounded_list.addItem(item)
        
        def isomorphic(G: Graph, l: List[Graph]) -> bool:
            for H in l:
                if is_isomorphic(G, H):
                    return True
            return False
        
        for node in G.nodes:
            G_ = Graph(G)
            G_.remove_node(node)
            if isomorphic(G_, self.collections_grounded):
                continue
            item = QListWidgetItem("link_{}".format(node))
            icon = graph(
                G,
                self.grounded_list.iconSize().width(),
                self.ground_engine,
                except_node=node
            )
            item.setIcon(icon)
            self.collections_grounded.append(G_)
            self.grounded_list.addItem(item)
        self.grounded_merge.setEnabled(bool(self.grounded_list.count()))
    
    @pyqtSlot(name='on_grounded_merge_clicked')
    def __groundedMerge(self):
        """Merge the grounded result."""
        item = self.grounded_list.currentItem()
        if not item:
            return
        G = self.collections_grounded[0]
        text = item.text()
        if text == "Released":
            ground_link = None
        else:
            ground_link = int(text.split("_")[1])
        reply = QMessageBox.question(self,
            "Message",
            "Merge \"{}\" chain to your canvas?".format(text)
        )
        if reply == QMessageBox.Yes:
            self.addPointsByGraph(
                G,
                self.ground_engine,
                ground_link
            )
