import sys
from circuit import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *


class MovingObject(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

class PreviewObject(QGraphicsPixmapItem):
    def __init__(self, x, y, fileName):
        self.pm = QPixmap(fileName)
        self.pm = self.pm.scaled(50, 50, Qt.KeepAspectRatio)
        super().__init__(self.pm)
        self.setPos(x, y)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    def mousePressEvent(self, event):
        pass
    
    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(updated_cursor_x, updated_cursor_y)
        print('x: {0}, y: {1}'.format(updated_cursor_position.x(), updated_cursor_position.y()))

class GraphicView(QGraphicsView):
    def __init__(self, a):
        super().__init__(a)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)       
        self.setSceneRect(0, 0, 1080, 720)

        self.moveObject = MovingObject(50, 50, 40)
        self.previewObject = PreviewObject(20, 20, "elements\Voltage_Source.svg.png")
        # self.moveObject2 = MovingObject(100, 100, 100)
        self.scene.addItem(self.moveObject)
        self.scene.addItem(self.previewObject)
        # self.scene.addItem(self.moveObject2)


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.detectedErrors = 0

        self.setFixedSize(QSize(1080, 720))
        self.setWindowTitle("SPICE Simulator [ver xx.xx.xx]")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        pixmapi = getattr(QStyle, "SP_MediaPlay")
        icon = self.style().standardIcon(pixmapi)
        startButton = QAction(QIcon(icon), "Start", self)
        sourceButton = QAction(QIcon("elements\Voltage_Source.svg.png"), "Source", self)
        pixmapi = getattr(QStyle, "SP_FileIcon")
        icon = self.style().standardIcon(pixmapi)
        newfileButton = QAction(QIcon(icon), "&New Schematic", self)
        

        taskbar = QToolBar("main")
        self.addToolBar(taskbar)
        taskbar.addAction(startButton)
        taskbar.addAction(sourceButton)

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(newfileButton)

        simulation_menu = menu.addMenu("&Simulation")
        

        self.mainview = GraphicView(self.centralwidget)

        self.setStatusBar(QStatusBar(self))


app = QApplication(sys.argv)
view = MainView()
view.show()
sys.exit(app.exec_())

