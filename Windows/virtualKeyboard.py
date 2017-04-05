import logging
from Windows import virtualKeyboard_ui
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Util import scroller
from Util.enums import *

logger = logging.getLogger(__name__)


class VirtualKeyboard(QDialog, virtualKeyboard_ui.Ui_VirtualKeyboard):
    WIDTH = 800
    HEIGHT_NO_SUGGESTIONS = 334
    HEIGHT_WITH_SUGGESTIONS = 480

    # Signal is emitted when the text changes to update suggestions model
    updateSuggestions = pyqtSignal(str)

    def __init__(self, parent=None, lineEdit=None, suggestionsListModel=None):
        super(VirtualKeyboard, self).__init__(parent)
        self.setupUi(self)

        # Move dialog to the top left corner of page
        self.move(0, 0)

        self.parentLineEdit = lineEdit
        if self.parentLineEdit:
            self.lineEdit.setAlignment(self.parentLineEdit.alignment())
            self.lineEdit.setCompleter(self.parentLineEdit.completer())
            self.lineEdit.setEchoMode(self.parentLineEdit.echoMode())
            self.lineEdit.setMaxLength(self.parentLineEdit.maxLength())
            self.lineEdit.setValidator(self.parentLineEdit.validator())
            self.lineEdit.setText(self.parentLineEdit.text())

        self.suggestionsListModel = suggestionsListModel
        if self.suggestionsListModel:
            self.suggestionsListView.setModel(suggestionsListModel)
            self.resize(self.WIDTH, self.HEIGHT_WITH_SUGGESTIONS)
            self.suggestionsListView.selectionModel().selectionChanged.connect(self.selectSuggestion)
            scroller.setupScrolling(self.suggestionsListView)
        else:
            self.gridLayout.removeWidget(self.suggestionsListView)
            self.suggestionsListView.setParent(None) # This works for modal dialog boxes where deleteLater DOES NOT
            self.suggestionsListView = None
            self.resize(self.WIDTH, self.HEIGHT_NO_SUGGESTIONS)

        # Remove title bar
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        self.state = KeyboardState.Normal

        self.layout = \
        [[self.tildeBtn,            ['`', '~', '`']],
         [self.oneBtn,              ['1', '!', '1']],
         [self.twoBtn,              ['2', '@', '2']],
         [self.threeBtn,            ['3', '#', '3']],
         [self.fourBtn,             ['4', '$', '4']],
         [self.fiveBtn,             ['5', '%', '5']],
         [self.sixBtn,              ['6', '^', '6']],
         [self.sevenBtn,            ['7', '&&', '7']],
         [self.eightBtn,            ['8', '*', '8']],
         [self.nineBtn,             ['9', '(', '9']],
         [self.zeroBtn,             ['0', ')', '0']],
         [self.minusBtn,            ['-', '_', '-']],
         [self.equalBtn,            ['=', '+', '=']],

         [self.qBtn,                ['q', 'Q', 'Q']],
         [self.wBtn,                ['w', 'W', 'W']],
         [self.eBtn,                ['e', 'E', 'E']],
         [self.rBtn,                ['r', 'R', 'R']],
         [self.tBtn,                ['t', 'T', 'T']],
         [self.yBtn,                ['y', 'Y', 'Y']],
         [self.uBtn,                ['u', 'U', 'U']],
         [self.iBtn,                ['i', 'I', 'I']],
         [self.oBtn,                ['o', 'O', 'O']],
         [self.pBtn,                ['p', 'P', 'P']],
         [self.leftBraceBtn,        ['[', '{', '[']],
         [self.rightBraceBtn,       [']', '}', ']']],
         [self.backSlashBtn,        ['\\', '|', '\\']],

         [self.aBtn,                ['a', 'A', 'A']],
         [self.sBtn,                ['s', 'S', 'S']],
         [self.dBtn,                ['d', 'D', 'D']],
         [self.fBtn,                ['f', 'F', 'F']],
         [self.gBtn,                ['g', 'G', 'G']],
         [self.hBtn,                ['h', 'H', 'H']],
         [self.jBtn,                ['j', 'J', 'J']],
         [self.kBtn,                ['k', 'K', 'K']],
         [self.lBtn,                ['l', 'L', 'L']],
         [self.semicolonBtn,        [';', ':', ';']],
         [self.quoteBtn,            ['\'', '\"', '\'']],

         [self.zBtn,                ['z', 'Z', 'Z']],
         [self.xBtn,                ['x', 'X', 'X']],
         [self.cBtn,                ['c', 'C', 'C']],
         [self.vBtn,                ['v', 'V', 'V']],
         [self.bBtn,                ['b', 'B', 'B']],
         [self.nBtn,                ['n', 'N', 'N']],
         [self.mBtn,                ['m', 'M', 'M']],
         [self.commaBtn,            [',', '<', ',']],
         [self.periodBtn,           ['.', '>', '.']],
         [self.forwardSlashBtn,     ['/', '?', '/']]]

        for buttonInfo in self.layout:
            buttonInfo[0].pressed.connect(self.characterPressed)

    @pyqtSlot()
    def showEvent(self, event):
        # Give focus to the line edit so you can see where the caret is located
        self.lineEdit.setFocus()

    def closeDialog(self, saveText=True):
        # Set text variable regardless if execution was successful
        self.text = self.lineEdit.text()

        if self.isModal():
            # If the dialog box is modal, then set the text variable to the current text in the line edit. Also, if the
            # text is empty (len = 0), then cancel the box, otherwise accept it. Also, if saveText is false, then close
            # the dialog box
            if len(self.text) > 0 and saveText:
                self.accept()
            else:
                self.close()
        else:
            self.hide()

            if self.parentLineEdit:
                self.parentLineEdit.clearFocus()

                # Only set the parent line edit to the text if supposed to save the text
                if saveText:
                    self.parentLineEdit.setText(self.lineEdit.text())

    def changeEvent(self, event):
        super(VirtualKeyboard, self).changeEvent(event)

        if self.isModal():
            return

        # If this dialog window is not active, hide it and clear focus to the parent widget so that it wont pop up
        # immediately after hiding this dialog
        if event.type() == QEvent.ActivationChange:
            if not self.isActiveWindow():
                self.closeDialog()

    @pyqtSlot(bool, bool)
    def on_enterBtn_clicked(self, checked, longPressed):
        self.closeDialog()

    @pyqtSlot(bool, bool)
    def on_confirmBtn_clicked(self, checked, longPressed):
        self.closeDialog()

    @pyqtSlot(bool, bool)
    def on_cancelBtn_clicked(self, checked, longPressed):
        self.closeDialog(False)

    @pyqtSlot(bool, bool)
    def on_leftShiftBtn_clicked(self, checked, longPressed):
        if checked:
            self.state |= KeyboardState.Shift
        else:
            self.state &= ~KeyboardState.Shift

        self.rightShiftBtn.setChecked(checked)
        self.updateState()

    @pyqtSlot(bool, bool)
    def on_rightShiftBtn_clicked(self, checked, longPressed):
        if checked:
           self.state |= KeyboardState.Shift
        else:
           self.state &= ~KeyboardState.Shift

        self.leftShiftBtn.setChecked(checked)
        self.updateState()

    @pyqtSlot(bool, bool)
    def on_capsBtn_clicked(self, checked, longPressed):
        if checked:
            self.state |= KeyboardState.Caps
        else:
            self.state &= ~KeyboardState.Caps

        self.updateState()

    @pyqtSlot(bool, bool)
    def on_backspaceBtn_clicked(self, checked, longPressed):
        self.lineEdit.backspace()

    @pyqtSlot(bool, bool)
    def on_tabBtn_clicked(self, checked, longPressed):
        self.lineEdit.insert("\t")

    @pyqtSlot(bool, bool)
    def on_clearBtn_clicked(self, checked, longPressed):
        self.lineEdit.clear()

    @pyqtSlot(bool, bool)
    def on_spaceBarBtn_clicked(self, checked, longPressed):
        self.lineEdit.insert(" ")

    @pyqtSlot(bool, bool)
    def on_leftBtn_clicked(self, checked, longPressed):
        # Move cursor backward without selecting the text
        self.lineEdit.cursorBackward(False)

    @pyqtSlot(bool, bool)
    def on_rightBtn_clicked(self, checked, longPressed):
        # Move cursor forward without selecting the text
        self.lineEdit.cursorForward(False)

    @pyqtSlot(str)
    def on_lineEdit_textChanged(self, str):
        self.updateSuggestions.emit(str)

    @pyqtSlot(bool, bool)
    def characterPressed(self, checked, longPressed):
        sender = self.sender()

        # Search layout for the correct button information
        for buttonInfo in self.layout:
            if buttonInfo[0] is sender:
                # The amperstand is special and must have hardcoded its output, otherwise, just insert the text on the btn
                if sender.text() == '&&':
                    self.lineEdit.insert("&")
                else:
                    self.lineEdit.insert(sender.text())

                # Turn off the shift modifier if it is currently set.
                # Shift key only lasts for one keypress
                if self.state & KeyboardState.Shift:
                    self.state &= ~KeyboardState.Shift
                    self.leftShiftBtn.setChecked(False)
                    self.rightShiftBtn.setChecked(False)
                    self.updateState()
                break

    def updateState(self):
        if self.state & KeyboardState.Shift:
            for buttonInfo in self.layout:
                buttonInfo[0].setText(buttonInfo[1][1])
        elif self.state & KeyboardState.Caps:
            for buttonInfo in self.layout:
                buttonInfo[0].setText(buttonInfo[1][2])
        else:
            for buttonInfo in self.layout:
                buttonInfo[0].setText(buttonInfo[1][0])

    @pyqtSlot()
    def selectSuggestion(self):
        records = self.suggestionsListModel.getSelectedRecords(self.sender().selectedIndexes())
        if len(records) != 1:
            logger.warning('Invalid number of records retrieved from suggestions list in selectSuggestion of Virtual '
                           'Keyboard.')
            return

        self.lineEdit.setText(records[0]['name'])
        self.lineEdit.setFocus()
        self.sender().clearSelection()