import sys
from PyQt5.QtWidgets import QApplication, QWidget
from mainWindow import *

def main():
    app = QApplication(sys.argv)

    # TODO Start by coding in the concept GUI to start out
    # TODO Implement the buttons in the concept GUI

    form = MainWindow()
    form.show() # Uncomment this out when testing
    #form.showFullScreen() # Uncomment this when not testing

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
