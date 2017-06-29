#!/usr/bin/env python
# -*- coding: utf-8 -*-


#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

import functools
from PySide import QtCore, QtGui


class MyPresenter(QtCore.QObject):

    def __init__(self, model, view):
        super(MyPresenter, self).__init__()

        # Store view and model.
        self.model = model
        self.view = view

        # Setup all signals.
        self.connectSignals()

        # Initialize buttons
        self.view.button_select_rangescale_10.mousePressEvent(None)
        self.view.button_select_glideslope_28.mousePressEvent(None)
        self.view.button_select_azantalev_020.mousePressEvent(None)
        self.view.button_select_nhist_10.mousePressEvent(None)
        self.view.button_hist.mousePressEvent(None)
        self.view.button_radarcover.mousePressEvent(None)
        self.view.button_fdb.mousePressEvent(None)
        self.view.button_whi.mousePressEvent(None)
        # ...more to follow
        
        

    def connectSignals(self):
        self.view.quit.connect(self.model.quit)
        
        # Main Window buttons
        self.view.button_whi_tgt_exchange.pressed.connect(self.exchangeWhiTrack)
        self.view.button_clear_alerts.pressed.connect(self.clearAlerts)
        
        # Radar Control buttons
        self.view.button_ant_drive.pressed.connect(self.toggleAntennaDrive)
        self.view.button_radiate.pressed.connect(self.toggleRadiation)
        self.view.button_rain_mode.pressed.connect(self.toggleRainMode)
        self.view.button_maint_mode.pressed.connect(self.toggleMaintMode)
        
        # Display Control buttons
        self.view.button_wx.pressed.connect(self.toggleWx)
        self.view.button_obs.pressed.connect(self.toggleObs)
        self.view.button_map.pressed.connect(self.toggleMap)
        self.view.button_whi.pressed.connect(self.toggleWhi)
        self.view.button_hist.pressed.connect(self.toggleHist)
        self.view.button_clear_hist.pressed.connect(self.clearHist)
        self.view.button_radarcover.pressed.connect(self.toggleRadarCover)
        self.view.button_syn_video.pressed.connect(self.toggleSynVideo)
        self.view.button_shutdown.pressed.connect(self.model.quit)

        self.connectACSizeButtons()
        self.connectNHistButtons()
        self.connectStatusButtons()
        self.connectRunwaySelectButtons()
        self.connectRangeScaleButtons()
        self.connectElScaleButtons()
        self.connectAzScaleButtons()
        self.connectGlideSlopeButtons()
        self.connectAzAntElevButtons()
        self.connectSelDBFldButtons()
        self.connectLeadDirButtons()

        self.model.new_plot_extracted.connect(self.view.scene.processReceivedPlot)
        
        self.model.new_airport.connect(self.setupNewRunwaySelectWindow)
        self.model.new_airport.connect(self.setupNewStatusWindow)
        self.model.new_airport.connect(self.newAirport)

        self.model.new_communication_data.connect(self.updateStatusWindow)
        
        self.model.new_connected_state.connect(self.updateConnectedState)
        
        self.model.connection_lost.connect(self.connectionLost)

    def connectLeadDirButtons(self):
        self.view.button_north.pressed.connect(self.newLeadDirChosen)
        self.view.button_northwest.pressed.connect(self.newLeadDirChosen)
        self.view.button_northeast.pressed.connect(self.newLeadDirChosen)
        self.view.button_west.pressed.connect(self.newLeadDirChosen)
        self.view.button_east.pressed.connect(self.newLeadDirChosen)
        self.view.button_southwest.pressed.connect(self.newLeadDirChosen)
        self.view.button_southeast.pressed.connect(self.newLeadDirChosen)
        self.view.button_south.pressed.connect(self.newLeadDirChosen)
        self.view.button_all.pressed.connect(self.newLeadDirChosen)
        
        

    def connectSelDBFldButtons(self):
        self.view.button_line1.pressed.connect(self.toggleLine1)
        self.view.button_line2.pressed.connect(self.toggleLine2)
        self.view.button_line3.pressed.connect(self.toggleLine3)
        self.view.button_leader.pressed.connect(self.toggleLeader)
        self.view.button_fdb.pressed.connect(self.toggleFdb)


    def connectACSizeButtons(self):
        self.view.button_select_ac_small.pressed.connect(self.newACSizeChosen)
        self.view.button_select_ac_medium.pressed.connect(self.newACSizeChosen)
        self.view.button_select_ac_large.pressed.connect(self.newACSizeChosen)



    def connectNHistButtons(self):
        self.view.button_select_nhist_1.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_2.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_3.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_4.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_5.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_6.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_7.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_8.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_9.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_10.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_11.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_12.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_13.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_14.pressed.connect(self.newNHistChosen)
        self.view.button_select_nhist_15.pressed.connect(self.newNHistChosen)


    def connectStatusButtons(self):
        self.view.button_load_new_airport.pressed.connect(self.loadAirport)
        self.view.button_connect.pressed.connect(self.connectToXPlane)
        #self.view.button_connect.pressed.connect(self.model.probeXPlanePlugin)
        self.view.button_record.pressed.connect(self.toggleRecording)
        self.view.button_demo.pressed.connect(self.toggleDemoMode)
        

    def connectAzAntElevButtons(self):
        self.view.button_select_azantalev_000.pressed.connect(self.newAzAntElevChosen)
        self.view.button_select_azantalev_005.pressed.connect(self.newAzAntElevChosen)
        self.view.button_select_azantalev_010.pressed.connect(self.newAzAntElevChosen)
        self.view.button_select_azantalev_015.pressed.connect(self.newAzAntElevChosen)
        self.view.button_select_azantalev_020.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_025.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_030.pressed.connect(self.newAzAntElevChosen)
        self.view.button_select_azantalev_035.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_040.pressed.connect(self.newAzAntElevChosen)
        self.view.button_select_azantalev_045.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_050.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_055.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_060.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_065.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_070.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_075.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_080.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_085.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_090.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_095.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_100.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_105.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_110.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_115.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_120.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_125.pressed.connect(self.newAzAntElevChosen)        
        self.view.button_select_azantalev_130.pressed.connect(self.newAzAntElevChosen)        
        
        
    def connectGlideSlopeButtons(self):
        self.view.button_select_glideslope_21.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_22.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_23.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_24.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_25.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_26.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_27.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_28.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_29.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_30.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_31.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_32.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_33.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_34.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_35.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_36.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_37.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_38.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_39.pressed.connect(self.newGlideSlopeChosen)
        self.view.button_select_glideslope_40.pressed.connect(self.newGlideSlopeChosen)

    def connectRunwaySelectButtons(self):
        self.view.button_select_runway_1.pressed.connect(self.newRunwayChosen)
        self.view.button_select_runway_2.pressed.connect(self.newRunwayChosen)
        self.view.button_select_runway_3.pressed.connect(self.newRunwayChosen)
        self.view.button_select_runway_4.pressed.connect(self.newRunwayChosen)
        self.view.button_select_runway_5.pressed.connect(self.newRunwayChosen)
        self.view.button_select_runway_6.pressed.connect(self.newRunwayChosen)
        
    def connectRangeScaleButtons(self):
        self.view.button_select_rangescale_down.pressed.connect(self.scaleDown)
        self.view.button_select_rangescale_up.pressed.connect(self.scaleUp)
        self.view.button_select_rangescale_1.pressed.connect(self.newRangeScaleChosen)
        self.view.button_select_rangescale_3.pressed.connect(self.newRangeScaleChosen)
        self.view.button_select_rangescale_5.pressed.connect(self.newRangeScaleChosen)
        self.view.button_select_rangescale_10.pressed.connect(self.newRangeScaleChosen)
        self.view.button_select_rangescale_15.pressed.connect(self.newRangeScaleChosen)
        self.view.button_select_rangescale_20.pressed.connect(self.newRangeScaleChosen)

    def connectElScaleButtons(self):
        self.view.button_select_elscale_1000.pressed.connect(self.newElevationScaleChosen)
        self.view.button_select_elscale_2000.pressed.connect(self.newElevationScaleChosen)
        self.view.button_select_elscale_4000.pressed.connect(self.newElevationScaleChosen)
        self.view.button_select_elscale_8000.pressed.connect(self.newElevationScaleChosen)
        self.view.button_select_elscale_12000.pressed.connect(self.newElevationScaleChosen)
        self.view.button_select_elscale_16000.pressed.connect(self.newElevationScaleChosen)
        self.view.button_select_elscale_32000.pressed.connect(self.newElevationScaleChosen)
        self.view.button_select_elscale_64000.pressed.connect(self.newElevationScaleChosen)

    def connectAzScaleButtons(self):
        self.view.button_select_azscale_2000.pressed.connect(self.newAzimuthScaleChosen)
        self.view.button_select_azscale_4000.pressed.connect(self.newAzimuthScaleChosen)
        self.view.button_select_azscale_8000.pressed.connect(self.newAzimuthScaleChosen)
        self.view.button_select_azscale_16000.pressed.connect(self.newAzimuthScaleChosen)
        self.view.button_select_azscale_24000.pressed.connect(self.newAzimuthScaleChosen)
        self.view.button_select_azscale_32000.pressed.connect(self.newAzimuthScaleChosen)


    def connectToXPlane(self):
        if self.view.scene.active_airport != None and not self.demo_mode:
            self.model.probeXPlanePlugin()



    def toggleDemoMode(self):
        # button_demo is a normal Button
        if not self.demo_mode and not self.connected:
            #if not self.view.button_demo.inverted:
            
            self.model.initDemoMode()
            
            print self.view.button_demo.inverted
            self.view.button_demo.toggleInverted()
            print self.view.button_demo.inverted
            
            print 'enter demo mode'
            #self.model.initDemoMode()
        elif self.demo_mode:
            print 'exit demo mode'
            #if self.view.button_demo.inverted:
            self.view.button_demo.toggleInverted()
            self.model.exitDemoMode()
            self.clearAlerts()
            self.clearAlerts()
            
            # How do I get rid of all the tracks left on the screen at this stage????????????????????
            


    def toggleRecording(self):
        # button_record is not a InvertingButton, just a Button
        if self.recording and self.connected:
            self.model.record = False
            if self.view.button_record.inverted:
                self.view.button_record.toggleInverted()
        elif not self.recording and self.connected and not self.demo_mode:
            self.model.record = True
            if not self.view.button_record.inverted:
                self.view.button_record.toggleInverted()
        # Yes, the following can happen. If coonection is suddenly dropped, a mousePressEvent from the
        # button_record is dispatched!!!
        elif self.recording and not self.connected:
            self.model.record = False
            if self.view.button_record.inverted:
                self.view.button_record.toggleInverted()


    def clearAlerts(self):
        self.view.scene.alerts_field.clickOnAllAlerts()


    def connectionLost(self):                   # Get this method into play together with the connection_state stuff!!!!!!!!!!!!!!!
        print 'connection with x-plane lost'
        self.updateConnectedState(False)
        
        #self.view.scene.clearAllTracks()
        #self.view.scene.drawAllTracks()
        

    def setupNewRunwaySelectWindow(self, airport):
        position_when_destroyed = self.view.runwayselect_window.scenePos()
        if not self.view.runwayselect_window.isHidden():
            self.view.runwayselect_window.hideWindow()
            show_window_after_creation = True
        else:
            show_window_after_creation = False
            
        self.view.scene.removeItem(self.view.runwayselect_window)
        
        rwy_names = []
        for each in airport.runways:
            rwy_names.append(each['name'])
        while len(rwy_names) <= 6:
            rwy_names.append('')
        self.view.runwayselect_window = self.view.createRunwaySelectWindow(rwy_names[0], rwy_names[1], rwy_names[2], rwy_names[3], rwy_names[4], rwy_names[5])
        # Let the garbage collector deal with the old window.
        
        self.view.button_runway_select.window = self.view.runwayselect_window      # Important. Feed the ExpandingButton its needed parameter.
        self.connectRunwaySelectButtons()
        self.view.runwayselect_window.setPos(position_when_destroyed)
        if show_window_after_creation:
            self.view.runwayselect_window.showWindow(self.view.button_runway_select)
        self.view.button_select_runway_1.mousePressEvent(None)     # Set runway 1 as active



    def setupNewStatusWindow(self, airport):
        self.view.scene.removeItem(self.view.status_window)
        self.view.status_window = self.view.createStatusWindow(airport)
        self.view.button_status.window = self.view.status_window      # Important. Feed the ExpandingButton its needed parameter.
        self.connectStatusButtons()
        if self.model.connected:
            self.view.button_connect.toggleInverted()
        self.view.status_window.showWindow(self.view.button_status)


    def updateStatusWindow(self, count, latest_delay, mean_delay, std_delay):
        self.view.status_window_area.updateDynamicTextItem('count', 'Message count:\t' + str(count) )
        self.view.status_window_area.updateDynamicTextItem('delay', 'Latest delay:\t\t{0:.3f}'.format(latest_delay) )
        self.view.status_window_area.updateDynamicTextItem('mean', 'Mean delay:\t\t{0:.3f}'.format(mean_delay) )
        self.view.status_window_area.updateDynamicTextItem('std', 'Std dev:\t\t{0:.3f}'.format(std_delay) )


    def updateConnectedState(self, new_connected_state):

        # Toggle CONNECT button (this updates the property self.connected) (True or False)
        # The self.connected property actually IS the self.view.button_connect.inverted value!!!
        if self.connected ^ new_connected_state:
            self.view.button_connect.toggleInverted()

        if self.connected:
            self.view.scene.alerts_field.addAlert('RADAR READY FOR USE')
            self.view.scene.connected = True                                            # ????????????????????
        
        elif not self.connected:
            self.view.status_window_area.updateDynamicTextItem('count', 'Message count:')
            self.view.status_window_area.updateDynamicTextItem('delay', 'Latest delay:')
            self.view.status_window_area.updateDynamicTextItem('mean', 'Mean delay:')
            self.view.status_window_area.updateDynamicTextItem('std', 'Std dev:')
            
            if self.radiating:
                self.view.button_ant_drive.mousePressEvent(None)        # This should take care of the radiate button as well
            
            if self.rain_mode_on:
                self.view.button_rain_mode.mousePressEvent(None)
                
            if self.maint_mode_on:
                self.view.button_maint_mode.mousePressEvent(None)
                
            if self.recording:
                self.view.button_record.mousePressEvent(None)
            
            self.view.scene.alerts_field.addAlert('DISPLAY DISCONNECTED FROM GCA', critical=True)
            self.view.scene.connected = False
            
            # Remove all tracks
            #self.view.scene.clearAllTracks()
            self.view.scene.drawAllTracks()
            self.view.scene.clearAllTracks()
            self.view.scene.drawAllGraphics()
            
            


    @property
    def connected(self):
        return self.view.button_connect.inverted
    
    @property
    def radiating(self):
        return self.view.button_radiate.inverted
    
    @property
    def antenna_drive_on(self):
        return self.view.button_ant_drive.inverted
    
    @property
    def rain_mode_on(self):
        return self.view.button_rain_mode.inverted
    
    @property
    def maint_mode_on(self):
        return self.view.button_maint_mode.inverted

    @property
    def recording(self):
        return self.model.record
    
    @property
    def demo_mode(self):
        return self.model.demo_mode


    def loadAirport(self):
        if not self.connected:
        # This method is called when user wants to load a new airport
            filename, _ = QtGui.QFileDialog.getOpenFileName(None, 'Open Airport', './resources/airports', 'Airport Files (*.apt)')
            if filename:
                self.model.readNewAirport(filename)

    
    def newAirport(self, airport):
        # This method is called after a new airport has been succesfully loaded
        self.view.scene.active_airport = airport
        #self.view.scene.alerts_field.addAlert('NEW AIRPORT LOADED')
        # Only standard alerts (as IRL I mean)


    def newACSizeChosen(self, button):
        print button.value
        
        # Some more work here I guess


    def newNHistChosen(self, button):
        if button.value != self.view.scene.nhist:
            self.view.scene.nhist = button.value
            self.view.scene.drawAllTracks()


    def clearHist(self, button):
        self.view.scene.resetAllHistoryPlots()
        self.view.scene.drawAllTracks()


    def newAzAntElevChosen(self, button):
        if button.value != self.view.scene.azantelev:
            self.azant_timer = QtCore.QTimer.singleShot(400.0, self.view.scene.drawElevationCoverage)
            if self.view.scene.azantelev != None:
                self.view.scene.alerts_field.addAlert('AZ ANT ELEV CHANGE IN PROGRESS')
                self.view.scene.alerts_field.addAlert('AZ ANT ELEV CHANGE COMPLETED', delay=500.0)
            self.view.scene.azantelev = button.value
                #self.view.scene.drawElevationCoverage()


    def newGlideSlopeChosen(self, button):
        if button.value != self.view.scene.glideslope:
            self.view.scene.glideslope = button.value
            self.view.scene.drawGlideSlope()
            self.view.scene.drawAllElevationTracks()


    def newRunwayChosen(self, button):
        if self.model.active_runway != None:
            # No runway change should register when loading airport for the first time!
            
            #if not self.demo_mode:
            self.view.scene.alerts_field.addAlert('RUNWAY CHANGE IN PROGRESS', delay=100.0)
            self.view.scene.alerts_field.addAlert('RUNWAY CHANGE COMPLETED', delay=1100.0)
                
            if self.radiating:
                self.view.button_radiate.mousePressEvent(None)
                self.view.scene.drawAllTracks()
                laterRadiate = functools.partial(self.view.button_radiate.mousePressEvent, None)
                self.radiate_timer = QtCore.QTimer.singleShot(1200.0, laterRadiate)
            
        if button.value != self.model.active_runway:
            self.model.active_runway = button.value
            self.view.scene.active_runway = button.value
            
            self.view.scene.clearAllTracks()
            self.view.scene.drawTextInfo()
            
            

                
    def newElevationScaleChosen(self, button):
        self.view.scene.elevationscale = button.value
        self.view.scene.drawElevationAxis()
        self.view.scene.drawElevationGraphics()
        self.view.scene.drawAllElevationTracks()


    def newAzimuthScaleChosen(self, button):
        self.view.scene.azimuthscale = button.value
        self.view.scene.drawAzimuthAxis()
        self.view.scene.drawAzimuthGraphics()
        self.view.scene.drawAllAzimuthTracks()


    def newRangeScaleChosen(self, button):
        self.view.scene.rangescale = button.value

        if button.value == 1:
            self.view.button_select_elscale_1000.mousePressEvent(None)
            self.view.button_select_azscale_2000.mousePressEvent(None)
        elif button.value == 3:
            self.view.button_select_elscale_2000.mousePressEvent(None)
            self.view.button_select_azscale_4000.mousePressEvent(None)
        elif button.value == 5:
            self.view.button_select_elscale_4000.mousePressEvent(None)
            self.view.button_select_azscale_8000.mousePressEvent(None)
        elif button.value == 10:
            self.view.button_select_elscale_8000.mousePressEvent(None)
            self.view.button_select_azscale_16000.mousePressEvent(None)
        if button.value == 15:
            self.view.button_select_elscale_12000.mousePressEvent(None)
            self.view.button_select_azscale_24000.mousePressEvent(None)
        elif button.value == 20:
            self.view.button_select_elscale_16000.mousePressEvent(None)
            self.view.button_select_azscale_32000.mousePressEvent(None)
        self.view.scene.drawRangeAxis()


    def scaleDown(self, button):
        previouslypressedbutton = None
        sortedscaleexclusivegrouplist = sorted(self.view.scaleexclusivegrouplist, key=lambda button: button.value)
        for eachbutton in sortedscaleexclusivegrouplist:
            if eachbutton.inverted:
                previouslypressedbutton = eachbutton
                break
        if previouslypressedbutton != None:
            index = sortedscaleexclusivegrouplist.index(previouslypressedbutton)
            if index > 0:
                sortedscaleexclusivegrouplist[index - 1].mousePressEvent(None)
            elif index == 0:
                sortedscaleexclusivegrouplist[index].mousePressEvent(None)


    def scaleUp(self, button):
        previouslypressedbutton = None
        sortedscaleexclusivegrouplist = sorted(self.view.scaleexclusivegrouplist, key=lambda button: button.value)
        for eachbutton in sortedscaleexclusivegrouplist:
            if eachbutton.inverted:
                previouslypressedbutton = eachbutton
                break
        if previouslypressedbutton != None:
            index = sortedscaleexclusivegrouplist.index(previouslypressedbutton)
            if index < (len(sortedscaleexclusivegrouplist) - 1):
                sortedscaleexclusivegrouplist[index + 1].mousePressEvent(None)
            else:
                sortedscaleexclusivegrouplist[index].mousePressEvent(None)


    def exchangeWhiTrack(self, button):

        if len(self.view.scene.designated_tracks) > 1:
            first_track = self.view.scene.designated_tracks[0]
            self.view.scene.designated_tracks.remove(first_track)
            self.view.scene.designated_tracks.append(first_track)
        
            self.view.scene.designated_tracks[-1].setPassive()
            self.view.scene.designated_tracks[-1].draw(elevation=True, azimuth=True, whi=True)
            #self.view.scene.designated_tracks[-1].drawWhiPlot()
            
            self.view.scene.designated_tracks[0].setActive()
            self.view.scene.designated_tracks[0].draw(elevation=True, azimuth=True, whi=True)
            #self.view.scene.designated_tracks[0].drawWhiPlot()
        
        
    def toggleLine1(self, button):
        #print 'toggle line 1'
        self.view.scene.line_1_visible = button.inverted
        self.view.scene.drawAllTracks()
        self.view.scene.drawWhiPlot()
        
    def toggleLine2(self, button):
        #print 'toggle line 2'
        self.view.scene.line_2_visible = button.inverted
        self.view.scene.drawAllTracks()
        self.view.scene.drawWhiPlot()

    def toggleLine3(self, button):
        #print 'toggle line 3'
        self.view.scene.line_3_visible = button.inverted
        self.view.scene.drawAllTracks()
        self.view.scene.drawWhiPlot()

    def toggleLeader(self, button):
        #print 'toggle leader'
        self.view.scene.leader_visible = button.inverted
        self.view.scene.drawAllTracks()

        
    def toggleFdb(self, button):
        if button.inverted:
            if not self.view.button_line1.inverted:
                self.view.button_line1.mousePressEvent(None)
            if not self.view.button_line2.inverted:
                self.view.button_line2.mousePressEvent(None)
            if not self.view.button_line3.inverted:
                self.view.button_line3.mousePressEvent(None)
            if not self.view.button_leader.inverted:
                self.view.button_leader.mousePressEvent(None)
        else:
            if self.view.button_line1.inverted:
                self.view.button_line1.mousePressEvent(None)
            if self.view.button_line2.inverted:
                self.view.button_line2.mousePressEvent(None)
            if self.view.button_line3.inverted:
                self.view.button_line3.mousePressEvent(None)
            if self.view.button_leader.inverted:
                self.view.button_leader.mousePressEvent(None)


    def newLeadDirChosen(self, button):
        print 'new lead dir ' + button.text


    # Radar Control buttons
    
    def toggleRadiation(self, button):
        if (not self.antenna_drive_on) and self.radiating:
            # If antenna drive is off, turn radiation off as well
            button.toggleInverted()
            self.view.scene.alerts_field.addAlert('ANTENNA DRIVE NOT READY')
        if not self.radiating:
            # If radiate just was turned off, clear the tracks
            self.view.scene.clearAllTracks()
        
        self.view.scene.radiating = self.radiating


    def toggleAntennaDrive(self, button):
        if (not self.antenna_drive_on) and self.radiating:
            # Antenna drive just turned off while radiating
            self.view.button_radiate.mousePressEvent(None)
        elif self.antenna_drive_on and (not self.connected):
            # Antenna drive commanded, but we are not connected
            button.toggleInverted()
        elif self.antenna_drive_on and self.connected:
            # We are connected, and start rotate has just been commanded
            button.toggleInverted()
            self.view.scene.alerts_field.addAlert('STARTING ANTENNA DRIVE')
            self.invert_timer = QtCore.QTimer.singleShot(400.0, button.toggleInverted)
            self.view.scene.alerts_field.addAlert('ANTENNA DRIVE READY', delay=500.0)
            
            

        
    def toggleRainMode(self, button):
        if (not self.connected) and self.rain_mode_on:
            button.toggleInverted()
        #self.view.scene.rain_mode_on = self.rain_mode_on       # Not necessary!?!
        
        
    def toggleMaintMode(self, button):
        if (not self.connected) and self.maint_mode_on:
            # If not connected, and the maint mode button has just been inverted, change back.
            button.toggleInverted()
        elif self.connected:
            if self.maint_mode_on:
                self.view.scene.alerts_field.addAlert('RADAR IN MAINTENANCE MODE')
            else:
                self.view.scene.alerts_field.addAlert('RADAR IN OPERATIONAL MODE')
        
        
        

    # Display Control buttons

    def toggleWx(self, button):
        self.view.scene.wx_active = button.inverted
        print 'toggle wx'

    def toggleObs(self, button):
        self.view.scene.obs_active = button.inverted
        print 'toggle obs'

    def toggleMap(self, button):
        self.view.scene.map_active = button.inverted
        print 'toggle map'

    def toggleWhi(self, button):
        self.view.scene.whi_active = button.inverted
        self.view.scene.drawWhiAxis()
        
        self.view.scene.drawWhiPlot()

    def toggleRadarCover(self, button):
        self.view.scene.radarcover_active = button.inverted
        self.view.scene.drawElevationCoverage()
        self.view.scene.drawAzimuthCoverage()
        self.view.scene.drawElevationGCA()
        self.view.scene.drawAzimuthGCA()

    def toggleHist(self, button):
        self.view.scene.hist_active = button.inverted
        self.view.scene.drawAllTracks()

    def toggleSynVideo(self, button):
        self.view.scene.synvid_active = button.inverted
        print 'toggle syn vid'






