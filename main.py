import sys
from tweak import InstallVCPP, InstallDirectX, CheckHPET, MsiModeTools, version, IsWin10
from time import sleep
from threading import Thread
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from gui_utils import (
    UWPRemover,
    makeButton,
    HackAnimation,
    getRegButtons,
    getPowerPlans,
    createLabel,
    createFrame,
)

import webbrowser

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(900, 550)
        self.setStyleSheet(
            '''
            QWidget {
                background-color: #1A1A1A; 
                color: #DCE4EE;       
            }

            QToolTip { 
                background-color: black; 
                color: white; 
                border: black solid 1px;
                font-size: 15px;
                font-family: Consolas;
            }

            QMessageBox {
                font-size: 14px;
            }

            QMessageBox QPushButton {
                background-color: #1A1A1A;
                color: #DCE4EE;
                border: 2px solid #3E454A;
                border-radius: 6px;
                padding: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: #5e6a73;
            }
            QMessageBox QPushButton:pressed {
                background-color: #3d4b52;
            }
            '''
        )

        self.setWindowTitle('CoreTweaks')
        self.setWindowIcon(QIcon('tweaks/coretweaks.ico'))

        layout = QGridLayout(self)
        layout.setRowStretch(10, 10)

        center_align = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft

        header_label = createLabel('')
        header_label.setStyleSheet('font-size: 20px; font-family: Consolas;')
        layout.addWidget(header_label, 1, 0, alignment=center_align)

        Thread(target=self.makeAnimation, args=('CoreTweaks', header_label)).start()

        layout.addWidget(createLabel('Tweaks:'), 2, 0)
        layout.addWidget(self.create_registry_frame(), 3, 0, alignment=center_align)

        layout.addWidget(createLabel('Power plans:'), 4, 0, alignment=center_align)
        layout.addWidget(self.create_power_frame(), 5, 0, alignment=center_align)

        layout.addWidget(createLabel('Tools:'), 9, 0, alignment=center_align)
        layout.addWidget(self.create_tools_frame(), 10, 0, alignment=center_align)

        # Info icon
        info_label = self.create_icon('GithubIcon')
        info_label.setCursor(Qt.CursorShape.PointingHandCursor)

        info_label.mousePressEvent = lambda event: webbrowser.open('https://github.com/dest4590/CoreTweaks')

        layout.addWidget(
            info_label, 10, 10,
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight,
        )

    def makeAnimation(self, text, label: QLabel):
        for p in HackAnimation(f'{text} {version}'):
            label.setText(p)
            sleep(0.05)

    def create_icon(self, icon: str):
        label = QLabel(self)
        pixmap = QPixmap(f'tweaks/{icon}.png')
        label.setPixmap(pixmap)
        return label

    def create_registry_frame(self):
        reg_frame = createFrame()
        reg_grid = getRegButtons(reg_frame)
        return reg_frame

    def create_power_frame(self):
        power_frame = createFrame()
        getPowerPlans(power_frame)
        return power_frame

    def create_tools_frame(self):
        tools_frame = createFrame()
        tools_layout = QGridLayout(tools_frame)
        tools_layout.setColumnStretch(3, 1)

        tools_layout.addWidget(makeButton('Install all VisualCPP', self.install_vcpp))
        tools_layout.addWidget(makeButton('Install DirectX', self.install_directx))

        if IsWin10:
            tools_layout.addWidget(makeButton('Check HPET', self.check_hpet))

        tools_layout.addWidget(makeButton('Msi Mode Tool', self.msi_mode_tools))

        uwpremover = UWPRemover()

        def run_uwp():
            popup = QMessageBox.information(self, 'Note',
                                            'Right click on the button to bring the application back up')

            print(popup)
            uwpremover.show()

        tools_layout.addWidget(makeButton('UWP Remover', run_uwp))

        return tools_frame

    def install_vcpp(self):
        Thread(target=InstallVCPP).start()

    def install_directx(self):
        Thread(target=InstallDirectX).start()

    def check_hpet(self):
        Thread(target=CheckHPET).start()

    def msi_mode_tools(self):
        Thread(target=MsiModeTools).start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())