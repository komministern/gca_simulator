

from PySide2 import QtCore, QtWidgets, QtGui


class MyLineEditProxyWidget(QtWidgets.QGraphicsProxyWidget):

    return_pressed = QtCore.Signal()
    
    def __init__(self, editable=False, hidden_password_input=False, allowed_input_characters='', convert_to_upper_case=False, first_char_must_be_letter=False, max_input_length=0):
        super(MyLineEditProxyWidget, self).__init__()
        self.myLineEditWidget = QtWidgets.QLineEdit()
        self.setWidget(self.myLineEditWidget)

        if not editable:
            self.myLineEditWidget.setReadOnly(True)

        if hidden_password_input:
            self.myLineEditWidget.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        if allowed_input_characters:
            self.myvalidator = MyValidator(self, allowed_input_characters, convert_to_upper_case, first_char_must_be_letter, max_input_length)
            self.myLineEditWidget.setValidator(self.myvalidator)

        self.myLineEditWidget.returnPressed.connect(self.rp)    # REMOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        self.myLineEditWidget.setFixedHeight(24)


    def rp(self):
        self.return_pressed.emit()          # REMOVE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def setWidth(self, width):
        self.myLineEditWidget.setFixedWidth(width)

    def setText(self, text):
        self.myLineEditWidget.setText(text)

    def text(self):
        return self.myLineEditWidget.text()



    # Do not know what the code below did for the mygraphicstextitem.....
    #def paint(self, painter, option, widget):
    #    # This takes care of the dashed frame
    #    o = QtWidgets.QStyleOptionGraphicsItem(option)
    #    o.state &= (not QtWidgets.QStyle.State_Selected) and (not QtWidgets.QStyle.State_HasFocus)
    #    super(MyLineEditProxyWidget, self).paint(painter, o, widget)



class MyValidator(QtGui.QValidator):
    def __init__(self, lineedit_widget, allowed_characters, convert_to_upper_case, first_char_must_be_letter, max_input_length):
        super(MyValidator, self).__init__()
        self.lineedit_widget = lineedit_widget
        self.allowed_characters = allowed_characters
        self.convert_to_upper_case = convert_to_upper_case
        self.first_char_must_be_letter = first_char_must_be_letter
        self.max_input_length = max_input_length

    def validate(self, input_str, anint):
        if self.max_input_length > 0:
            if len(input_str) > self.max_input_length:
                return QtGui.QValidator.Invalid
        if input_str != '':
            if self.convert_to_upper_case:
                if input_str[-1] in 'abcdefghijklmnopqrstuvwxyzåäö':
                    self.lineedit_widget.setText(input_str.upper())
            if self.first_char_must_be_letter:
                if not input_str[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    return QtGui.QValidator.Invalid
            if input_str[-1] in self.allowed_characters:
                return QtGui.QValidator.Acceptable
            else:
                return QtGui.QValidator.Invalid
        else:
            return QtGui.QValidator.Acceptable
