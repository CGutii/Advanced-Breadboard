import sys
import subprocess
import espCommunication
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout, QFrame, QInputDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QDrag, QIcon, QTransform
from PyQt5.QtCore import Qt, QMimeData, QPoint, QByteArray, pyqtSignal

class DraggableLabel(QLabel):
    def __init__(self, parent, image, title):
        super().__init__(parent)
        self.originalPixmap = image.scaled(60, 60, Qt.KeepAspectRatio)
        self.setPixmap(self.originalPixmap)

        self.title = QLabel(title, parent)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.move(0, 60)  # Position the label under the component

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimeData = QMimeData()

        componentData = QByteArray()
        componentData.append(self.title.text().encode('utf-8'))
        mimeData.setData("application/x-component", componentData)

        drag.setMimeData(mimeData)
        drag.setPixmap(self.originalPixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction)


class TextDraggableLabel(QLabel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.setText(title)
        self.setStyleSheet("background-color: white; color: black; border: 1px solid black; padding: 2px;")
        self.setFixedSize(100, 30)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimeData = QMimeData()

        componentData = QByteArray()
        componentData.append("TextComponent")
        mimeData.setData("application/x-component", componentData)

        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction)

class EditableTextLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent, text):
        super().__init__(parent)
        self.setText(text)
        self.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.setFixedSize(100, 30)

    def mousePressEvent(self, event):
        self.clicked.emit()

class ComponentLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent, image):
        super().__init__(parent)
        self.setPixmap(image)
        self.setAcceptDrops(True)
        self.is_moving = False
        self.rotation_angle = 0
        self.text_label = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.is_moving = True
            self.clicked.emit()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if self.is_moving:
            self.move(self.mapToParent(event.pos() - self.drag_start_position))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_moving = False

    def rotate(self):
        self.rotation_angle = (self.rotation_angle + 90) % 360
        pixmap = self.pixmap().transformed(QTransform().rotate(self.rotation_angle))
        self.setPixmap(pixmap)
        if self.text_label:
            self.text_label.setPixmap(self.text_label.pixmap().transformed(QTransform().rotate(self.rotation_angle)))

    def addLabel(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter label:')
        if ok:
            if self.text_label:
                self.text_label.deleteLater()
            self.text_label = QLabel(text, self)
            self.text_label.setStyleSheet("color: black;")
            self.text_label.move(0, -20)
            self.text_label.show()

class DropLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: white;")

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-component"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-component"):
            componentData = event.mimeData().data("application/x-component").data().decode('utf-8')
            if componentData == "TextComponent":
                self.parent().parent().addTextToCanvas("Edit Text", event.pos())
            else:
                self.parent().parent().addComponentToCanvas(componentData, event.pos())


class CircuitSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.actionStack = []  # Stack to track actions for undo

    def initUI(self):
        self.setWindowTitle('Circuit Simulator')
        self.setStyleSheet("background-color: green;")
        self.setGeometry(100, 100, 720, 600)  # Adjusted window size

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QGridLayout()

        # Canvas for circuit
        self.canvas = DropLabel(self)
        self.canvas.setFixedSize(700, 500)
        mainLayout.addWidget(self.canvas, 1, 0, 1, 3)

        # Top buttons setup
        self.setupTopButtons(mainLayout)

        # Toolbox setup
        toolboxLayout = QHBoxLayout()
        self.setupToolbox(toolboxLayout)
        mainLayout.addLayout(toolboxLayout, 2, 0, 1, 3)

        centralWidget.setLayout(mainLayout)

    def setupTopButtons(self, layout):
        # File button
        fileButton = QPushButton('File', self)
        fileButton.setStyleSheet("background-color: white;")
        fileButton.setFixedSize(80, 25)
        layout.addWidget(fileButton, 0, 0)

        # Undo button
        undoButton = QPushButton('Undo', self)
        undoButton.setStyleSheet("background-color: white;")
        undoButton.setFixedSize(120, 25)
        undoButton.clicked.connect(self.undoLastAction)
        layout.addWidget(undoButton, 0, 1)

        # Finish button
        finishButton = QPushButton('Finish', self)
        finishButton.setStyleSheet("background-color: white;")
        finishButton.setFixedSize(80, 25)
        finishButton.clicked.connect(self.runReportScript)  # Connect button to the method
        layout.addWidget(finishButton, 0, 2)  # Corrected here

        # Trash can image
        self.trashCanLabel = QLabel(self)
        trashCanPixmap = QPixmap("trash_can.png").scaled(40, 40, Qt.KeepAspectRatio)
        self.trashCanLabel.setPixmap(trashCanPixmap)
        self.trashCanLabel.setAcceptDrops(True)
        self.trashCanLabel.dropEvent = self.trashDropEvent
        layout.addWidget(self.trashCanLabel, 0, 3, Qt.AlignRight)

    def setupToolbox(self, layout):
        # Component setup
        components = [('Power Source', 'powerSource.png'),
                      ('Resistor', 'resistor.png'),
                      ('Capacitor', 'capacitor.png'),
                      ('Inductor', 'inductor.png'),
                      ('Ground', 'ground.png')]
        for title, image_path in components:
            pixmap = QPixmap(image_path)
            label = DraggableLabel(self, pixmap, title)
            layout.addWidget(label)
            layout.addWidget(label.title)

        # Draggable text component
        textLabel = TextDraggableLabel(self, "Text")
        layout.addWidget(textLabel)

    def addComponentToCanvas(self, componentType, position):
        pixmap = QPixmap(f'{componentType.replace(" ", "").lower()}.png')
        if pixmap.isNull():
            print(f"Failed to load image: {componentType.replace(' ', '').lower()}.png")
            return
        pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio)
        componentLabel = ComponentLabel(self.canvas, pixmap)
        componentLabel.move(position - QPoint(30, 30))
        componentLabel.clicked.connect(lambda: self.componentClicked(componentLabel))
        componentLabel.show()
        self.actionStack.append(componentLabel)

    def componentClicked(self, label):
        action = QInputDialog.getItem(self, "Component Actions", 
                                      "Select action:", ["Rotate", "Delete", "Add Label"], 0, False)
        if action[1]:
            if action[0] == "Rotate":
                label.rotate()
            elif action[0] == "Delete":
                label.deleteLater()
                self.actionStack.remove(label)
            elif action[0] == "Add Label":
                label.addLabel()

    def undoLastAction(self):
        if self.actionStack:
            lastAction = self.actionStack.pop()
            lastAction.deleteLater()

    def trashDropEvent(self, event):
        if event.mimeData().hasFormat("application/x-component"):
            event.acceptProposedAction()
            componentType = event.mimeData().data("application/x-component").data().decode('utf-8')
            self.removeComponentFromCanvas(componentType)

    # Draggable text component
        textLabel = TextDraggableLabel(self, "Text")
        layout.addWidget(textLabel)
    
    def addTextToCanvas(self, text, position):
        textLabel = EditableTextLabel(self.canvas, text)
        textLabel.clicked.connect(lambda: self.editText(textLabel))
        textLabel.move(position)
        textLabel.show()
        self.actionStack.append(textLabel)

    def editText(self, label):
        text, ok = QInputDialog.getText(self, 'Edit Text', 'Enter text:', QLineEdit.Normal, label.text())
        if ok:
            label.setText(text)
    
    def runReportScript(self):
        subprocess.run(["python", "report.py"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CircuitSimulatorApp()
    ex.show()
    sys.exit(app.exec_())
