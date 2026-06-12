# /src/backend/services/file_services.py

from PySide6.QtWidgets import QFileDialog
import numpy as np

# this function is userd in multiple location in calibration data control code to open the file

def open_file(ui):
    file_dialog = QFileDialog(ui.centralwidget)
    file_dialog.setFileMode(QFileDialog.ExistingFile) 
    file_dialog.setNameFilter("CSV files (*.csv)")
    if file_dialog.exec():
        file_paths = file_dialog.selectedFiles()
        for file_path in file_paths:
            print("Selected file:", file_path)          # get the file locations
            return file_path


