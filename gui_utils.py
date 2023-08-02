from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtWidgets import QPushButton, QGridLayout, QSizePolicy, QFrame, QWidget, QLabel, QGraphicsDropShadowEffect, QApplication
from PyQt6.QtGui import QIcon, QColor, QFont
from random import choice
from threading import Thread
from tweak import (regtweaks, schemes, 
                   RegTweakByName, PowerPlanByName, 
                   RegFile, PowerPlanFile, 
                   version, UWPApps, 
                   removeUWP, CMDTweak,
                   removeAllUWP)
import webbrowser, sys


buttonStyleSheet = '''
QPushButton {
    padding: 3px;
}
QPushButton:hover {
    background-color: #5e6a73;
}
QPushButton:pressed {
    background-color: #3d4b52;
}
'''

frameStyleSheet = '''
QFrame {
    border: 2px solid #3E454A;
    border-radius: 6px;
}
QPushButton {
    background-color: #1A1A1A;
    color: #DCE4EE;
    border: 2px solid #3E454A;
    border-radius: 6px;
}
'''

# Custom button
class TweakButton(QPushButton):
    def __init__(self, tweak: RegFile | CMDTweak, *args, **kwargs):
        super().__init__(tweak.name)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setStyleSheet(buttonStyleSheet)
        self.setMinimumSize(self.sizeHint())
        self.setFont(QFont('Bahnschrift', 12))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if isinstance(tweak, RegFile) or isinstance(tweak, CMDTweak):
            if tweak.recommended:
                effect = QGraphicsDropShadowEffect( offset=QPointF(0, 0), blurRadius=10, color=QColor("#a4f4a8"))
                self.setGraphicsEffect(effect)

            if tweak.dangerous:
                effect = QGraphicsDropShadowEffect( offset=QPointF(0, 0), blurRadius=10, color=QColor("#f6f69d"))
                self.setGraphicsEffect(effect)
            
        if tweak.desc != None:
            self.setToolTip(tweak.desc)
        
        if isinstance(tweak, RegFile):
            if not tweak.checkCompatibility():
                self.setEnabled(False)
                self.setStyleSheet('QPushButton { color: #3e3e42; }')
                
        if isinstance(tweak, RegFile):
            self.clicked.connect(lambda checked, t=self.text():Thread(target=RegTweakByName, args=(t,)).start())
            
        elif isinstance(tweak, PowerPlanFile):
            self.clicked.connect(lambda checked, t=self.text():Thread(target=PowerPlanByName, args=(t,)).start())

# Make InfoWindow
class InfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(500, 200)
        self.setStyleSheet('background-color: #1A1A1A;color: #DCE4EE;')
        self.setWindowTitle('CoreTweaks - Info')
        self.setWindowIcon(QIcon('tweaks/coretweaks.ico'))

        layout = QGridLayout(self)
        layout.setRowStretch(10, 10)
        self.rainbowLabel = createLabel('CoreTweaks ' + version)
        layout.addWidget(self.rainbowLabel, 0, 0)
        layout.addWidget(createLabel('By Purpl3 - Program/Gui\nArsenii - Tweaks'), 1, 0)
        layout.addWidget(createLabel('Part of'), 2, 0)
        layout.addWidget(createLabelLink('C0reLabs (click)', 'https://t.me/c0relabs'), 3, 0)

        self.rainbowLabel.setProperty("hue", 0)

        self.rainbow_timer = QTimer(self)
        self.rainbow_timer.timeout.connect(self.updateRainbowColor)
        self.rainbow_timer.start(100)

    def updateRainbowColor(self):
        hue = (self.rainbowLabel.property("hue") + 1) % 360
        self.rainbowLabel.setProperty("hue", hue)
        self.rainbowLabel.setStyleSheet(
            f"color: {QColor.fromHsl(hue, 255, 127).name()};"
            f'font-family: Bahnshrift; font-size: {str(20)}px;'
        )

class UWPRemover(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(850, 500)
        self.setStyleSheet('background-color: #1A1A1A;color: #DCE4EE;')
        self.setWindowTitle('CoreTweaks - UWP Remover')
        self.setWindowIcon(QIcon('tweaks/coretweaks.ico'))

        layout = QGridLayout(self)
        layout.setRowStretch(10, 10)
        
        layout.addWidget(createLabel('UWP Remover', 30), 0, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        appsFrame = createFrame()
        appsGrid = QGridLayout(appsFrame)
        for key, value, i in zip(UWPApps.keys(), UWPApps.values(), enumerate(UWPApps.keys())):
            button = makeButton(key, lambda checked, v=value:Thread(target=removeUWP, args=(v,)).start(), True, 'padding: 3px;font-size: 17px', lambda clicked, v=value:Thread(target=removeUWP, args=(v,True)).start())
            button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

            appsGrid.addWidget(button, i[0] // 3, i[0] % 3, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(appsFrame)

        removeAll = makeButton('REMOVE ALL', lambda checked:Thread(target=removeAllUWP).start(), True)
        effect = QGraphicsDropShadowEffect( offset=QPointF(0, 0), blurRadius=10, color=QColor("#f6f69d"))
        removeAll.setGraphicsEffect(effect)
        removeAll.setToolTip('We do not recommend it.')
        appsGrid.addWidget(removeAll, 10, 10, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        layout.addWidget(makeButton('Back', lambda checked:self.close(), border=True, customStyle='font-size:20px;padding: 5px;'), 10, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

def createFrame():
    frame = QFrame()
    frame.setStyleSheet(frameStyleSheet)
    frame.setFrameShape(QFrame.Shape.StyledPanel)
    return frame

def createLabel(text, size = 18):
    label = QLabel(text)
    label.setFont(QFont('Bahnschrift', size))
    return label

def createLabelLink(text, link):
    label = createLabel(text)
    label.setStyleSheet(f'font-family: Bahnshrift; font-size: {str(20)}px;color: #4A55A2;')
    label.setCursor(Qt.CursorShape.PointingHandCursor)
    label.mousePressEvent = lambda clicked:webbrowser.open(link)

    return label

def getRegButtons(frame: QFrame):
    grid = QGridLayout(frame)

    for i, tweak in enumerate(regtweaks):
        button = TweakButton(tweak)

        if not tweak.checkCompatibility(): # Check tweak compatibility
            button.setEnabled(False)
            button.setStyleSheet('QPushButton { color: #3e3e42; }')

        grid.addWidget(button, i // 3, i % 3, alignment=Qt.AlignmentFlag.AlignCenter)

    grid.setColumnStretch(3, 1)

    return grid

def getPowerPlans(frame: QFrame):
    grid = QGridLayout(frame)
    for i, scheme in enumerate(schemes):
        button = TweakButton(scheme)
        if scheme.dangerous:
                effect = QGraphicsDropShadowEffect( offset=QPointF(0, 0), blurRadius=10, color=QColor("#f6f69d"))
                button.setGraphicsEffect(effect)

        grid.addWidget(button, i // 3, i % 3, alignment=Qt.AlignmentFlag.AlignCenter)

    grid.setColumnStretch(3, 1)

def makeButton(text: str, function, border = False, customStyle = None, rightClickFunction = None):
    button = QPushButton(text)
    button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    button.setStyleSheet(buttonStyleSheet)
    if border:
        button.setStyleSheet(buttonStyleSheet + 'QPushButton { border: 2px solid #3E454A; border-radius: 6px; }')
    if customStyle != None and border:
        button.setStyleSheet(buttonStyleSheet + 'QPushButton { border: 2px solid #3E454A; border-radius: 6px;' + customStyle + '}')
    button.setFont(QFont('Bahnschrift', 12))
    button.setMinimumSize(button.sizeHint())
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.clicked.connect(function)
    if rightClickFunction != None:
        button.customContextMenuRequested.connect(rightClickFunction)
    return button

def HackAnimation(text):
    symbols = ['*','@','#','$','%','^','&']
    shif = [choice(symbols) for _ in range(len(text))]
    steps = [''.join(shif)]
    
    for i in range(len(text)):
        shif.pop(i)
        shif.insert(i, text[i])
        steps.append(''.join(shif))
        
    return steps

'''
# Debug
app = QApplication(sys.argv)
window = UWPRemover()
window.show()
sys.exit(app.exec())
'''