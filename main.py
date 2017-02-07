import sys
from PyQt5.QtWidgets import QApplication, QWidget
from mainWindow import *
from configobj import ConfigObj
from validate import Validator
from exception import *
from configobj import *

def main():
    configspec = ConfigObj('./configspec.ini', raise_errors=True, _inspec=True)
    validator = Validator()

    config = ConfigObj('./config.ini', configspec=configspec, create_empty=True)
    errors = config.validate(validator, preserve_errors=True, copy=True)

    msg = ""
    for entry in flatten_errors(config, errors):
        [sectionList, key, error] = entry

        if key is not None:
            sectionList.append(key)

        # Parameter name is each section joined by an arrow(->) followed by the value
        # So one->two would be the value two in the section one
        parameterName = '->'.join(sectionList)

        # An error of false means the section/value was missing, otherwise error is an exception with a string describing error
        if error is False:
            msg += "%s: Missing value or section\n" % parameterName
        else:
            msg += "%s: %s\n" % (parameterName, error)

    if len(msg) > 0:
        # An error occurred, save the config file in case any default data was copied
        config.write()
        raise SmartShopException("Could not parse config file:\n%s" % msg)

    app = QApplication(sys.argv)

    # TODO Start by coding in the concept GUI to start out
    # TODO Implement the buttons in the concept GUI

    form = MainWindow(config)

    # Will pass this argument in Raspberry Pi 3 to get fullscreen display
    if "-fullscreen" in sys.argv:
        form.showFullScreen()
    else:
        form.show()

    ret = app.exec()

    # Save config file. It is possible for changes to be made using settings menu in GUI
    config.write()

    sys.exit(ret)

if __name__ == '__main__':
    main()
