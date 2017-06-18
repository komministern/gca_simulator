

from PySide import QtGui, QtCore


class AlertsField(QtCore.QObject):
    
    # QGraphicsItemGroup seems ideal for this, but a bug concerning propagation of
    # signals from scene to the member items of the group made this difficult.
    # This works and will do.
    
    def __init__(self, scene):
        super(AlertsField, self).__init__()
        self.scene = scene
        self.frame_item = None
        self.alerts = []
        
    def addAlert(self, text, critical=False):
        if len(self.alerts) == 0:
            self.alerts.append(NonClickableAlert('ALERT', self, scene=self.scene))

        if unicode(text) not in [each.toPlainText() for each in self.alerts]:
            self.alerts.append(Alert(text, self, scene=self.scene))
            self.draw()

    def draw(self):
        if self.frame_item:
            self.scene.removeItem(self.frame_item)
            del self.frame_item
        self.frame_item = None
        
        for each in self.alerts:
            self.scene.removeItem(each)
        
        for each in self.alerts:
            if each.obsolete:
                self.alerts.remove(each)
                del each
        
        if len(self.alerts) > 1:
            y = 0.0
            largest_width = 0.0
            for each in self.alerts:
                self.scene.addItem(each)
                each.setPos(self.scene.alerts_field_centre_x - each.width/2.0, self.scene.alerts_field_top_y + y)
                largest_width = max(largest_width, each.width)
                y += each.height
                
            self.frame_item = QtGui.QGraphicsRectItem(self.scene.alerts_field_centre_x - largest_width/2.0 - self.scene.alerts_frame_margin, self.scene.alerts_field_top_y - self.scene.alerts_frame_margin, 
                                                      largest_width + self.scene.alerts_frame_margin*2, y + self.scene.alerts_frame_margin*2, scene=self.scene)
            self.frame_item.setPen(self.scene.alerts_field_pen)
    
    #self.scene.alerts_field_width / 2.0


class Alert(QtGui.QGraphicsTextItem):
        
    def __init__(self, text, field, scene):
        super(Alert, self).__init__(text, scene=scene)
        self.field = field
        self.acknowledged = False
        # INVERT HERE
        self.obsolete = False
        self.setFont(self.scene().alerts_font)
        self.setZValue(self.scene().alerts_zvalue)
        self.document().setDocumentMargin(0.0)
        self.width = self.boundingRect().width()
        self.height = self.boundingRect().height()
        
        self.setDefaultTextColor(self.scene().alerts_color)


    def mousePressEvent(self, event):
        if not self.acknowledged:
            self.acknowledged = True
            self.setDefaultTextColor(QtCore.Qt.yellow)  # REVERT HERE!!!!!!!
        else:
            self.obsolete = True
            self.field.draw()


class CriticalAlert(Alert):
    pass


class NonClickableAlert(Alert):
    def __init__(self, text, field, scene):
        super(NonClickableAlert, self).__init__(text, field, scene=scene)
        
    def mousePressEvent(self, event):
        pass