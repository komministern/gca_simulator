
from PySide import QtGui

class MapSymbols(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(MapSymbols, self).__init__(scene=scene)
        
        self.setZValue(self.scene().mapsymbols_zvalue)
        #self.create()
    
    def draw(self):
        pass
        #self.create()
    



    def drawMapSymbols(self):
        
        if self.mapsymbols_item:
            self.removeItem(self.mapsymbols_item)
            del self.mapsymbols_item
            self.mapsymbols_item = None
            
        if self.map_active:
            
            self.mapsymbols_item = QtGui.QGraphicsItemGroup(parent=None, scene=self)
            
            lineitem = QtGui.QGraphicsLineItem(0.0, 0.0, 100.0, 100.0, parent=self.mapsymbols_item)
            lineitem.setPen(self.axis_pen)