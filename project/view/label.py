#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.




from PySide import QtGui, QtCore
#import weakref
import numpy as np


class Label(QtGui.QGraphicsItemGroup):
    
    def __init__(self, scene, parent_track):
        super(Label, self).__init__(scene=scene)
        self.parent_track = parent_track
        self.label_currently_pressed = False
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

        self.setVisible(False)

        self.x_offset = 150.0
        self.y_offset = -150.0

        self.plot_x_scene_coordinate = 0.0
        self.plot_y_scene_coordinate = 0.0

        self.leader_line_item = None

        self.fictive_callsign_text_item = QtGui.QGraphicsSimpleTextItem('UA12345')
        self.fictive_callsign_text_item.setFont(self.scene().active_label_font)
        self.max_callsign_text_item_width = self.fictive_callsign_text_item.boundingRect().width()
        self.text_row_height = self.fictive_callsign_text_item.boundingRect().height()
        
        self.height = 3*self.text_row_height
        
        del self.fictive_callsign_text_item

        self.fictive_size_text_item = QtGui.QGraphicsSimpleTextItem('M')
        self.fictive_size_text_item.setFont(self.scene().active_label_font)
        
        self.width = self.max_callsign_text_item_width + self.scene().text_distance_x + self.fictive_size_text_item.boundingRect().width()
        
        del self.fictive_size_text_item
        
        self.setZValue(self.scene().active_label_zvalue)
    
    
    def resetOffsets(self):
        self.x_offset = 150.0
        self.y_offset = -150.0
    
    
    def centerPoint(self):
        top_left_point = self.scenePos()
        top_left_x = top_left_point.x()
        top_left_y = top_left_point.y()
        
        center_x = top_left_x + self.width / 2
        center_y = top_left_y + self.height / 2
        
        return QtCore.QPointF(center_x, center_y)
    
    def leftPoint(self):
        top_left_point = self.scenePos()
        top_left_x = top_left_point.x()
        top_left_y = top_left_point.y()
        
        left_x = top_left_x
        left_y = top_left_y + self.height / 2
        
        return QtCore.QPointF(left_x, left_y)
    
    def rightPoint(self):
        top_left_point = self.scenePos()
        top_left_x = top_left_point.x()
        top_left_y = top_left_point.y()
        
        right_x = top_left_x + self.width
        right_y = top_left_y + self.height / 2
        
        return QtCore.QPointF(right_x, right_y)
    
    def topPoint(self):
        top_left_point = self.scenePos()
        top_left_x = top_left_point.x()
        top_left_y = top_left_point.y()
        
        top_x = top_left_x + self.width / 2
        top_y = top_left_y
        
        return QtCore.QPointF(top_x, top_y)
    
    def bottomPoint(self):
        top_left_point = self.scenePos()
        top_left_x = top_left_point.x()
        top_left_y = top_left_point.y()
        
        bottom_x = top_left_x + self.width / 2
        bottom_y = top_left_y + self.height
    
        return QtCore.QPointF(bottom_x, bottom_y)

    def bottomLeftPoint(self):
        top_left_point = self.scenePos()
        top_left_x = top_left_point.x()
        top_left_y = top_left_point.y()
        
        bottom_left_x = top_left_x
        bottom_left_y = top_left_y + self.height
        
        return QtCore.QPointF(bottom_left_x, bottom_left_y)
    
    def topLeftPoint(self):
        top_left_point = self.scenePos()
        top_left_x = top_left_point.x()
        top_left_y = top_left_point.y()
        
        return QtCore.QPointF(top_left_x, top_left_y)
    
    def topRightPoint(self):
        top_left_point = self.scenePos()
        top_left_x = top_left_point.x()
        top_left_y = top_left_point.y()
        
        top_right_x = top_left_x + self.width
        top_right_y = top_left_y
        
        return QtCore.QPointF(top_right_x, top_right_y)
    
    def bottomRightPoint(self):
        top_left_point = self.scenePos()
        top_left_x = top_left_point.x()
        top_left_y = top_left_point.y()
        
        bottom_right_x = top_left_x + self.width
        bottom_right_y = top_left_y + self.height
    
        return QtCore.QPointF(bottom_right_x, bottom_right_y)



    def updateLabelPosition(self):
        if not self.label_currently_pressed:
            
            #plot_point = self.scene().getElevationPoint(self.parent_track().list_of_coords[0])
            # This is not correct if an extrapolated coordinate is beeing used. FIX.
            
            self.setPos(self.plot_point.x() + self.x_offset, self.plot_point.y() + self.y_offset)


    def getAngle(self, delta_x, delta_y):
        
        if delta_x > 0.0:
            return 90.0 + np.arctan(delta_y/delta_x) / np.pi * 180.0
        
        if delta_x < 0.0:
            return 270.0 + np.arctan(delta_y/delta_x) / np.pi * 180.0
        
        elif delta_y < 0.0 and delta_x == 0.0:
            return 0.0
        
        elif delta_y > 0.0 and delta_x == 0.0:
            return 180.0
        
        else:
            return 0.0


    def drawLeader(self):
        if self.leader_line_item:
            del self.leader_line_item
            self.leader_line_item = None
        
        # Leader should now be drawn, if and only if the leader is activated
        
        if self.parent_track.designated and self.scene().leader_visible:
        
            #plot_point = self.scene().getElevationPoint(self.parent_track().list_of_coords[0])
            plot_x = self.plot_point.x()
            plot_y = self.plot_point.y()
            # This is not correct if an extrapolated coordinate is beeing used. FIX.
    
            label_center_point = self.centerPoint()
            center_x = label_center_point.x()
            center_y = label_center_point.y()
            
            # zero degrees straight up
            angle = self.getAngle(center_x-plot_x, center_y-plot_y)
            delta_angle = 360.0/16
            
            if angle >= 1*delta_angle and angle < 3*delta_angle:
                end_point = self.bottomLeftPoint()
            elif angle >= 3*delta_angle and angle < 5*delta_angle:
                end_point = self.leftPoint()
            elif angle >= 5*delta_angle and angle < 7*delta_angle:
                end_point = self.topLeftPoint()
            elif angle >= 7*delta_angle and angle < 9*delta_angle:
                end_point = self.topPoint()
            elif angle >= 9*delta_angle and angle < 11*delta_angle:
                end_point = self.topRightPoint()
            elif angle >= 11*delta_angle and angle < 13*delta_angle:
                end_point = self.rightPoint()
            elif angle >= 13*delta_angle and angle < 15*delta_angle:
                end_point = self.bottomRightPoint()
            else:
                end_point = self.bottomPoint()

            end_x = end_point.x()
            end_y = end_point.y()
            
            self.leader_line_item = QtGui.QGraphicsLineItem(self.plot_point.x(), self.plot_point.y(), end_x, end_y, parent=None, scene=self.scene())
        
            self.leader_line_item.setPen(self.scene().active_leader_pen)
            self.leader_line_item.setZValue(self.scene().active_leader_zvalue)


    def update(self):
        
        # New posistion should be set to the plots position plus the x and y offset if plot is not pressed
        #       if pressed the position should be left unchanged
        # Draw the leader if it is activated
        # Set visibility True or False to the three lines
        # Update the contents in the three lines, always
        
        if len(self.parent_track.list_of_coords) > 0:
        
            self.updatePlotPoint()
        
            self.updateCallsign()
        
            self.updateSize()
        
            self.updateVelocity()
        
            self.updateDistance()
        
            self.updateDeviation()
        
            self.updateLabelPosition()
        
            self.drawLeader()
        



    def updateCallsign(self):
        self.callsign_text_item.setText(self.parent_track.callsign_string)


    def updateSize(self):
        self.size_text_item.setText(self.parent_track.size_string)


    def updateVelocity(self):
        
        velocity_string = str(int(round(self.parent_track.velocity)))
        
        if len(velocity_string) == 1:
            velocity_string = '00' + velocity_string
        elif len(velocity_string) == 2:
            velocity_string = '0' + velocity_string
        elif len(velocity_string) > 3:
            velocity_string = '999'
        
        self.velocity_text_item.setText(velocity_string)


    def updateDistance(self):
        self.distance_text_item.setText(str(round(self.parent_track.distance_to_td, 1)))

        



    def toggleCallsignVisibility(self):
        if self.callsign_text_item.isVisible():
            self.callsign_text_item.setVisible(False)
        else:
            self.callsign_text_item.setVisible(True)

    def toggleSizeVisibility(self):
        if self.size_text_item.isVisible():
            self.size_text_item.setVisible(False)
        else:
            self.size_text_item.setVisible(True)

    def toggleVelocityVisibility(self):
        if self.velocity_text_item.isVisible():
            self.velocity_text_item.setVisible(False)
        else:
            self.velocity_text_item.setVisible(True)

    def toggleDistanceVisibility(self):
        if self.distance_text_item.isVisible():
            self.distance_text_item.setVisible(False)
        else:
            self.distance_text_item.setVisible(True)

    def toggleDeviationVisibility(self):
        if self.deviation_text_item.isVisible():
            self.deviation_text_item.setVisible(False)
        else:
            self.deviation_text_item.setVisible(True)




    def mousePressEvent(self, event):
        super(Label, self).mousePressEvent(event)
        self.label_currently_pressed = True
        #print 'label currently pressed'
        # Not needed!?!

    def mouseReleaseEvent(self, event):
        super(Label, self).mouseReleaseEvent(event)
        self.label_currently_pressed = False
        
        #plot_point = self.scene().getElevationPoint(self.parent_track().list_of_coords[0])
        
        self.x_offset = self.scenePos().x() - self.plot_point.x()
        self.y_offset = self.scenePos().y() - self.plot_point.y()
        # Calculate the new offset values, x and y

    def mouseMoveEvent(self, event):
        super(Label, self).mouseMoveEvent(event)
        self.drawLeader()




class ElevationLabel(Label):
    
    def __init__(self, scene, parent_track):
        super(ElevationLabel, self).__init__(scene, parent_track)
        self.createElevationLabel()


    def createElevationLabel(self):

        self.callsign_text_item = QtGui.QGraphicsSimpleTextItem('', parent=self)
        self.callsign_text_item.setFont(self.scene().active_label_font)
        self.callsign_text_item.setBrush(self.scene().active_label_brush)
        self.callsign_text_item.setPos(0.0, 0.0)

        self.size_text_item = QtGui.QGraphicsSimpleTextItem('', parent=self)
        self.size_text_item.setFont(self.scene().active_label_font)
        self.size_text_item.setBrush(self.scene().active_label_brush)
        self.size_text_item.setPos(self.max_callsign_text_item_width + self.scene().text_distance_x, 0.0)

        self.velocity_text_item = QtGui.QGraphicsSimpleTextItem('', parent=self)
        self.velocity_text_item.setFont(self.scene().active_label_font)
        self.velocity_text_item.setBrush(self.scene().active_label_brush)
        self.velocity_text_item.setPos(0.0, self.text_row_height)

        self.distance_text_item = QtGui.QGraphicsSimpleTextItem('', parent=self)
        self.distance_text_item.setFont(self.scene().active_label_font)
        self.distance_text_item.setBrush(self.scene().active_label_brush)
        self.distance_text_item.setPos(self.max_callsign_text_item_width + self.scene().text_distance_x + self.size_text_item.boundingRect().width() - self.distance_text_item.boundingRect().width(), 
                                      self.text_row_height)

        self.deviation_text_item = QtGui.QGraphicsSimpleTextItem('', parent=self)
        self.deviation_text_item.setFont(self.scene().active_label_font)
        self.deviation_text_item.setBrush(self.scene().active_label_brush)
        self.deviation_text_item.setPos(0.0, 2*self.text_row_height)
        

    
    def updatePlotPoint(self):
        #if len(self.parent_track.list_of_coords) > 0:
        self.plot_point = self.scene().getElevationPoint(self.parent_track.list_of_coords[0])
        #else:
        #    self.plot_point = None


    def updateDeviation(self):
        if self.parent_track.elevation_deviation >= 0.0:
            sign_string = '+'
        else:
            sign_string = ''
        elevation_deviation_string = sign_string + str(int(self.parent_track.elevation_deviation))
        
        self.deviation_text_item.setText(elevation_deviation_string)




        
    # Fictive measurements for all placings in the label!!!!!!!!!!!!!!!!!!!!

 
 
 
class AzimuthLabel(Label):
    
    def __init__(self, scene, parent_track):
        super(AzimuthLabel, self).__init__(scene, parent_track)
        self.createAzimuthLabel()


    def createAzimuthLabel(self):

        self.callsign_text_item = QtGui.QGraphicsSimpleTextItem('', parent=self)
        self.callsign_text_item.setFont(self.scene().active_label_font)
        self.callsign_text_item.setBrush(self.scene().active_label_brush)
        self.callsign_text_item.setPos(0.0, 0.0)

        self.size_text_item = QtGui.QGraphicsSimpleTextItem('M', parent=self)
        self.size_text_item.setFont(self.scene().active_label_font)
        self.size_text_item.setBrush(self.scene().active_label_brush)
        self.size_text_item.setPos(self.max_callsign_text_item_width + self.scene().text_distance_x, 0.0)

        self.velocity_text_item = QtGui.QGraphicsSimpleTextItem('000', parent=self)
        self.velocity_text_item.setFont(self.scene().active_label_font)
        self.velocity_text_item.setBrush(self.scene().active_label_brush)
        self.velocity_text_item.setPos(0.0, self.text_row_height)

        self.distance_text_item = QtGui.QGraphicsSimpleTextItem('0.0', parent=self)
        self.distance_text_item.setFont(self.scene().active_label_font)
        self.distance_text_item.setBrush(self.scene().active_label_brush)
        self.distance_text_item.setPos(self.max_callsign_text_item_width + self.scene().text_distance_x + self.size_text_item.boundingRect().width() - self.distance_text_item.boundingRect().width(), 
                                      self.text_row_height)

        self.deviation_text_item = QtGui.QGraphicsSimpleTextItem('000', parent=self)
        self.deviation_text_item.setFont(self.scene().active_label_font)
        self.deviation_text_item.setBrush(self.scene().active_label_brush)
        self.deviation_text_item.setPos(0.0, 2*self.text_row_height)


    def updatePlotPoint(self):
        self.plot_point = self.scene().getAzimuthPoint(self.parent_track.list_of_coords[0])


    def updateDeviation(self):
        if self.parent_track.azimuth_deviation >= 0.0:
            sign_string = '+'
        else:
            sign_string = ''
        azimuth_deviation_string = sign_string + str(int(self.parent_track.azimuth_deviation))
        
        self.deviation_text_item.setText(azimuth_deviation_string)




#class WHILabel(Label):
#    
#    def __init__(self):
#        pass