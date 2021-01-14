"""
Copyright (C) 2021 Oscar Franzén <oscarfranzen@protonmail.com>

This file is part of GCA Simulator.

GCA Simulator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GCA Simulator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GCA Simulator.  If not, see <https://www.gnu.org/licenses/>.
"""

from PySide2 import QtCore, QtWidgets, QtGui

class MyGraphicsTextItem(QtWidgets.QGraphicsTextItem):

    return_pressed = QtCore.Signal()
    
    def __init__(self, editable=False, hidden_input=False, exclusive_characters=False):
        super(MyGraphicsTextItem, self).__init__('')

        self.exclusive_characters = 'abcdefghijklmnopqrstuvwxyz0123456789!"#¤%&/()=?+-,.;:ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        self.hidden_input = hidden_input

        #self.setEcho

        self.hidden_string = ''

        if editable:
            self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        
        #self.document().contentsChanged.connect(self.new_character_entered)
        
        #fmt = QtGui.QTextCharFormat()
        #fmt.setFontCapitalization(QtGui.QFont.AllUppercase)
        #self.textCursor().setCharFormat(fmt)
        
        #self.lowercase = 'abcdefghijklmnopqrstuvwxyz'
        #self.uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        #self.allowed = self.uppercase + ' 1234567890.:'

            
    def paint(self, painter, option, widget):
        # This takes care of the dashed frame
        o = QtWidgets.QStyleOptionGraphicsItem(option)
        o.state &= (not QtWidgets.QStyle.State_Selected) and (not QtWidgets.QStyle.State_HasFocus)
        super(MyGraphicsTextItem, self).paint(painter, o, widget)
        
        
    def keyPressEvent(self, event):



        #type = event.type()
        key = event.key()
        #print(key)
        
        



        #modifiers = event.modifiers()
        #e = QtGui.QKeyEvent(type, key+1, modifiers)
        #print key
        
        if key == 16777220:
            #print 'return'
            self.return_pressed.emit()

        else:

        #    if self.hidden_input:

        #        if len(self.hidden_string) > 0 and event.key() == 16777219: # DELETE
        #            self.hidden_string = self.hidden_string[:-1]
        #        elif event.text() in self.exclusive_characters:
        #            self.hidden_string += event.text()

        #        print(self.hidden_string)

        #        self.setPlainText(self.hidden_string)

            super(MyGraphicsTextItem, self).keyPressEvent(event)
    
        
#    def new_character_entered(self):
#        pass
        #index = self.textCursor().position()
        #print index
        
        #if index > 0 and self.test:
            #new_char = self.toPlainText()[index-1]
        
            #if new_char == '\n':
                #print 'return'
                #print len(self.toPlainText())
                #self.textCursor().deletePreviousChar()

            #if new_char in self.lowercase:
                #new_char = self.uppercase[self.lowercase.index(new_char)]
                #print new_char
        
            #if new_char not in self.allowed:
                #print 'nope'
                #self.textCursor().deletePreviousChar()
                
        #if self.test:
            #self.test = False
        #else:
            #self.test = True
        
        #print index

        #if not (self.toPlainText()[index] in self.allowed):
        #    print 'deleting'
        #    self.textCursor().deletePreviousChar()
            
        
#        widget = QtGui.QTextEdit()
#fmt = QtGui.QTextCharFormat()
#fmt.setFontCapitalization(QtGui.QFont.AllUppercase)
#widget.setCurrentCharFormat(fmt)