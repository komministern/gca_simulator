
from PySide import QtGui, QtCore
import numpy as np

class ElevationCoverage(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(ElevationCoverage, self).__init__(scene=scene)
        
        self.lower_line_item = None
        self.upper_line_item = None
        self.azantelev_item = None
        
        self.rangescale = None
        self.elevationscale = None
        #self.azimuthscale = None
        self.azantelev = None
        
        self.setVisible(self.scene().radarcover_active)
        self.setZValue(self.scene().coverage_zvalue)
        
        self.create()


    def draw(self):
        
        # If the rangescale or elevationscale or azantelev differs from the last creation, create new line items.
        #if (self.scene().rangescale != self.rangescale) or (self.scene().elevationscale != self.elevationscale) or (self.scene().azantelev != self.azantelev):
        self.create()
        # The if statement above is commented out due to erroneous behavior when changing runway. Inefficiency before error.
        
        # Set visibility
        self.setVisible(self.scene().radarcover_active and self.scene().connected)

        
    def create(self):
        
        if self.lower_line_item != None and self.upper_line_item != None:   # These really either both exists, or not.
            self.removeFromGroup(self.lower_line_item)
            self.removeFromGroup(self.upper_line_item)
            self.removeFromGroup(self.azantelev_item)
            self.upper_line_item = None                 # Let the garbage collector do its job
            self.lower_line_item = None
            self.azantelev_item = None
        
        
        if self.scene().rangescale and self.scene().elevationscale and self.scene().gca_elevation_point and (self.scene().azantelev != None):# and self.scene().radarcover_active:
            
            self.rangescale = self.scene().rangescale
            self.elevationscale = self.scene().elevationscale
            self.azimuthscale = self.scene().azimuthscale
            self.azantelev = self.scene().azantelev
            
            m_per_x_pixel = self.scene().rangescale*1852.0 / (self.scene().rangeaxismax_x - self.scene().rangeaxiszero_x)
            m_per_y_pixel = self.scene().elevationscale*0.3048 / (self.scene().elevationaxiszero_y - self.scene().elevationaxismax_y)
            
            start_point = self.scene().gca_elevation_point
            
            upper_slope = np.tan(7.0*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            upper_end_point = QtCore.QPointF(self.scene().rangeaxismax_x, start_point.y() - upper_slope*(self.scene().rangeaxismax_x - self.scene().gca_elevation_point.x()))
        
            # Keep upper coverage line inside the elevation graphics area
            if upper_end_point.y() < self.scene().elevationgraphicsareatopleft_y:
                new_x = -1.0 * (self.scene().elevationgraphicsareatopleft_y - start_point.y()) / upper_slope + start_point.x()
                if new_x > self.scene().rangeaxismax_x:
                    new_x = self.scene().rangeaxismax_x
                
                delta_x = new_x - start_point.x()
                upper_end_point = QtCore.QPointF(new_x, start_point.y() - upper_slope*delta_x)

            upper_line = QtCore.QLineF(start_point, upper_end_point)
        
            self.upper_line_item = QtGui.QGraphicsLineItem(upper_line)
            self.upper_line_item.setPen(self.scene().coverage_pen)
            
            self.addToGroup(self.upper_line_item)
        

            lower_slope = np.tan(-1.0*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            lower_end_point = QtCore.QPointF(self.scene().rangeaxismax_x, start_point.y() - lower_slope*(self.scene().rangeaxismax_x - self.scene().gca_elevation_point.x()))
            
            # Keep lower coverage line inside the elevation graphics area
            if lower_end_point.y() > self.scene().elevationgraphicsareabottomright_y:
                new_x = -1.0 * (self.scene().elevationgraphicsareabottomright_y - start_point.y()) / lower_slope + start_point.x()
                if new_x > self.scene().rangeaxismax_x:
                    new_x = self.scene().rangeaxismax_x
                
                delta_x = new_x - start_point.x()
                lower_end_point = QtCore.QPointF(new_x, start_point.y() - lower_slope*delta_x)
                
            lower_line = QtCore.QLineF(start_point, lower_end_point)
            self.lower_line_item = QtGui.QGraphicsLineItem(lower_line)
            self.lower_line_item.setPen(self.scene().coverage_pen)
            
            self.addToGroup(self.lower_line_item)
            

            azantelev_slope = np.tan(self.scene().azantelev*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            azantelev_end_point = QtCore.QPointF(self.scene().rangeaxismax_x, start_point.y() - azantelev_slope*(self.scene().rangeaxismax_x - self.scene().gca_elevation_point.x()))
            
            # Keep azantelev coverage line inside the elevation graphics area
            if azantelev_end_point.y() < self.scene().elevationgraphicsareatopleft_y:
                new_x = -1.0 * (self.scene().elevationgraphicsareatopleft_y - start_point.y()) / azantelev_slope + start_point.x()
                if new_x > self.scene().rangeaxismax_x:
                    new_x = self.scene().rangeaxismax_x
                
                delta_x = new_x - start_point.x()
                azantelev_end_point = QtCore.QPointF(new_x, start_point.y() - azantelev_slope*delta_x)
            
            azantelev_line = QtCore.QLineF(start_point, azantelev_end_point)

            self.azantelev_item = QtGui.QGraphicsLineItem(azantelev_line)
            self.azantelev_item.setPen(self.scene().coverage_pen)

            self.addToGroup(self.azantelev_item)
        
        else:
            #print 'ERROR - ElevationCoverage created without necessary inputs'
            pass







class AzimuthCoverage(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene):
        super(AzimuthCoverage, self).__init__(scene=scene)
        
        self.lower_line_item = None
        self.upper_line_item = None
        self.middle_line_item = None
        
        self.rangescale = None
        #self.elevationscale = None
        self.azimuthscale = None
        self.elantazim = None
        
        self.setVisible(self.scene().radarcover_active)
        self.setZValue(self.scene().coverage_zvalue)
        
        self.create()


    def draw(self):
        
        # If the rangescale or azimuthscale differs from the last creation, create new line items.
        #if (self.scene().rangescale != self.rangescale) or (self.scene().azimuthscale != self.azimuthscale):
        self.create()
        # The if statement above is commented out due to erroneous behavior when changing runway. Inefficiency before error.
        
        # Set visibility
        self.setVisible(self.scene().radarcover_active and self.scene().connected)
        

    def create(self):
        
        if self.lower_line_item != None and self.upper_line_item != None:   # These really either both exists, or not.
            self.removeFromGroup(self.lower_line_item)
            self.removeFromGroup(self.upper_line_item)
            self.removeFromGroup(self.middle_line_item)
            self.upper_line_item = None                 # Let the garbage collector do its job
            self.lower_line_item = None
            self.middle_line_item = None
        
        if self.scene().rangescale and self.scene().azimuthscale and self.scene().gca_azimuth_point:# and self.scene().radarcover_active:
            
            self.rangescale = self.scene().rangescale
            #self.elevationscale = self.scene().elevationscale
            self.azimuthscale = self.scene().azimuthscale
            self.elantazim = self.scene().elantazim         # Build on this !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
            m_per_x_pixel = self.scene().rangescale*1852.0 / (self.scene().rangeaxismax_x - self.scene().rangeaxiszero_x)
            m_per_y_pixel = self.scene().azimuthscale*0.3048 / (self.scene().azimuthaxiszero_y - self.scene().azimuthaxismax_y)
        
            start_point = self.scene().gca_azimuth_point
            
            upper_slope = np.tan((15.0 - self.elantazim)*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            lower_slope = np.tan((-15.0 - self.elantazim)*np.pi/180) * m_per_x_pixel / m_per_y_pixel
            middle_slope = np.tan((0.0 - self.elantazim)*np.pi/180) * m_per_x_pixel / m_per_y_pixel

            delta_x = self.scene().rangeaxismax_x - start_point.x()
            
            upper_end_point = QtCore.QPointF(self.scene().rangeaxismax_x, start_point.y() - upper_slope*delta_x)
            lower_end_point = QtCore.QPointF(self.scene().rangeaxismax_x, start_point.y() - lower_slope*delta_x)
            middle_end_point = QtCore.QPointF(self.scene().rangeaxismax_x, start_point.y() - middle_slope*delta_x)
        
            # Keep upper coverage line inside the azimuth graphics area
            if upper_end_point.y() < self.scene().azimuthgraphicsareatopleft_y:

                new_x = -1.0 * (self.scene().azimuthgraphicsareatopleft_y - start_point.y()) / upper_slope + start_point.x()
                if new_x > self.scene().rangeaxismax_x:
                    new_x = self.scene().rangeaxismax_x
                
                delta_x = new_x - start_point.x()
                upper_end_point = QtCore.QPointF(new_x, start_point.y() - upper_slope*delta_x)
            
            upper_line = QtCore.QLineF(start_point, upper_end_point)

            # Keep lower coverage line inside the azimuth graphics area
            if lower_end_point.y() > self.scene().azimuthgraphicsareabottomright_y:

                new_x = -1.0 * (self.scene().azimuthgraphicsareabottomright_y - start_point.y()) / lower_slope + start_point.x()
                if new_x > self.scene().rangeaxismax_x:
                    new_x = self.scene().rangeaxismax_x
                
                delta_x = new_x - start_point.x()
                lower_end_point = QtCore.QPointF(new_x, start_point.y() - lower_slope*delta_x)
            
            lower_line = QtCore.QLineF(start_point, lower_end_point)

            # Keep middle coverage line inside the azimuth graphics area
            if middle_end_point.y() < self.scene().azimuthgraphicsareatopleft_y:

                new_x = -1.0 * (self.scene().azimuthgraphicsareatopleft_y - start_point.y()) / middle_slope + start_point.x()
                if new_x > self.scene().rangeaxismax_x:
                    new_x = self.scene().rangeaxismax_x
                
                delta_x = new_x - start_point.x()
                middle_end_point = QtCore.QPointF(new_x, start_point.y() - middle_slope*delta_x)
            
            elif middle_end_point.y() > self.scene().azimuthgraphicsareabottomright_y:

                new_x = -1.0 * (self.scene().azimuthgraphicsareabottomright_y - start_point.y()) / middle_slope + start_point.x()
                if new_x > self.scene().rangeaxismax_x:
                    new_x = self.scene().rangeaxismax_x
                
                delta_x = new_x - start_point.x()
                middle_end_point = QtCore.QPointF(new_x, start_point.y() - middle_slope*delta_x)

            middle_line = QtCore.QLineF(start_point, middle_end_point)


            self.upper_line_item = QtGui.QGraphicsLineItem(upper_line)
            self.upper_line_item.setPen(self.scene().coverage_pen)

            self.lower_line_item = QtGui.QGraphicsLineItem(lower_line)
            self.lower_line_item.setPen(self.scene().coverage_pen)

            self.middle_line_item = QtGui.QGraphicsLineItem(middle_line)
            self.middle_line_item.setPen(self.scene().coverage_pen)


            
            self.addToGroup(self.upper_line_item)
            self.addToGroup(self.lower_line_item)
            self.addToGroup(self.middle_line_item)
            
        else:
            #print 'ERROR - AzimuthCoverage created without necessary inputs'
            pass