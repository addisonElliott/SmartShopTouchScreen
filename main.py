import sys
from PyQt5.QtWidgets import QApplication, QWidget
from mainWindow import *

def main():
    app = QApplication(sys.argv)

    # TODO Start by coding in the concept GUI to start out
    # TODO Implement the buttons in the concept GUI

    form = MainWindow()

    # Will pass this argument in Raspberry Pi 3 to get fullscreen display
    if "-fullscreen" in sys.argv:
        form.showFullScreen()
    else:
        form.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
