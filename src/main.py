import sys
from PySide6.QtWidgets import QApplication, QWidget,QPushButton,QMainWindow,QSlider,QLabel,QMessageBox,QLineEdit
from PySide6.QtWidgets import QVBoxLayout,QHBoxLayout,QFileDialog,QToolBar,QSizePolicy
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon,QAction 

import frontend
import backend


#from backend.controllers.controller import UIController

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the MainWindow class
        """
        super().__init__()
        # Initialize the UI
        self.ui = frontend.Ui_MainWindow()
        # Set up the user interface using the ui instance
        self.ui.setupUi(self) #Pass the MainWindow instance to setupUi function

        # Create an instance of the controller and pass the UI instance
        self.controller = backend.UIController(self.ui)
        
        # Timer to update motor state
        self.timer = QTimer(self)  # Create a timer
        self.timer.setInterval(100)  # Set the timer interval 100ms
        self.timer.timeout.connect(self.controller.update_parameters) # function call 
        self.timer.start() 
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    #window.controller.start_timer()  # Start the timer
    #window.controller.update_parameters()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
