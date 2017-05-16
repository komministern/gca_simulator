﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-


#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.


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
        
        # ...more to follow
        
        
        #self.slask_var = 0


    def connectSignals(self):
        self.view.quit.connect(self.model.quit)
                
        # Radar Control buttons
        self.view.button_ant_drive.pressed.connect(self.view.scene.toggleAntennaDrive)
        self.view.button_radiate.pressed.connect(self.view.scene.toggleRadiation)
        self.view.button_rain_mode.pressed.connect(self.view.scene.toggleRainMode)
        self.view.button_maint_mode.pressed.connect(self.view.scene.toggleMaintMode)
        
        # Display Control buttons
        self.view.button_wx.pressed.connect(self.view.scene.toggleWx)
        self.view.button_obs.pressed.connect(self.view.scene.toggleObs)
        self.view.button_map.pressed.connect(self.view.scene.toggleMap)
        self.view.button_whi.pressed.connect(self.view.scene.toggleWhi)
        self.view.button_hist.pressed.connect(self.view.scene.toggleHist)
        self.view.button_radarcover.pressed.connect(self.view.scene.toggleRadarCover)
        self.view.button_syn_video.pressed.connect(self.view.scene.toggleSynVideo)
        self.view.button_shutdown.pressed.connect(self.model.quit)

        
        self.connectNHistButtons()
        self.connectStatusButtons()
        self.connectRunwaySelectButtons()
        self.connectRangeScaleButtons()
        self.connectElScaleButtons()
        self.connectAzScaleButtons()
        self.connectGlideSlopeButtons()
        self.connectAzAntElevButtons()

        self.model.new_plot_extracted.connect(self.view.scene.processReceivedPlot)
        self.model.new_airport.connect(self.setupNewRunwaySelectWindow)
        self.model.new_airport.connect(self.setupNewStatusWindow)
        self.model.new_airport.connect(self.view.scene.newAirport)

        self.model.new_communication_data.connect(self.updateStatusWindow)
        self.model.new_connected_state.connect(self.updateConnectButton)


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
        self.view.button_connect.pressed.connect(self.model.probeXPlanePlugin_)
        

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
        
        #self.view.status_window_area.updateDynamicTextItem('airport', 'Airport:         ' + airport.iata)



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


    def updateConnectButton(self, connected):
        if self.view.button_connect.inverted ^ connected:
            self.view.button_connect.toggleInverted()
            
        if not connected:
            self.view.status_window_area.updateDynamicTextItem('count', 'Message count:')
            self.view.status_window_area.updateDynamicTextItem('delay', 'Latest delay:')
            self.view.status_window_area.updateDynamicTextItem('mean', 'Mean delay:')
            self.view.status_window_area.updateDynamicTextItem('std', 'Std dev:')


    def loadAirport(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(None, 'Open Airport', '~', 'Airport Files (*.apt)')
        if filename:
            self.model.readNewAirport(filename)


        




#    def processReceivedPlots(self, listofplots): 
#        self.view.scene.processReceivedPlots(listofplots)

    def newNHistChosen(self, button):
        if button.value != self.view.scene.nhist:
            self.view.scene.nhist = button.value
            self.view.scene.drawAllElevationTracks()
            self.view.scene.drawAllAzimuthTracks()



    def newAzAntElevChosen(self, button):
        if button.value != self.view.scene.azantelev:
            self.view.scene.azantelev = button.value
            self.view.scene.drawAzAntElev()


    def newGlideSlopeChosen(self, button):
        if button.value != self.view.scene.glideslope:
            self.view.scene.glideslope = button.value
            self.view.scene.drawGlideSlope()


    def newRunwayChosen(self, button):
        if button.value != self.model.active_runway:
            self.model.active_runway = button.value
            self.view.scene.active_runway = button.value
            
            self.view.scene.airplane_track.clear()
            self.view.scene.mti_1_track.clear()
            self.view.scene.mti_2_track.clear()
            
            
            #self.view.scene.airplane_elevation_track.clear()
            #self.view.scene.drawElevationGraphics()
            #self.view.scene.drawAzimuthGraphics()
                

    def newElevationScaleChosen(self, button):
        self.view.scene.elevationscale = button.value
        
        self.view.scene.createElevationAxis()
        
        #self.view.scene.airplane_elevation_track.clear()           # Get rid of obsolete history plots
        
        self.view.scene.drawElevationGraphics()


    def newAzimuthScaleChosen(self, button):
        self.view.scene.azimuthscale = button.value
        
        self.view.scene.createAzimuthAxis()
        
        #self.view.scene.airplane_azimuth_track.clear()
        
        self.view.scene.drawAzimuthGraphics()


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
        self.view.scene.createElevationAndAzimuthRangeAxis()



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
    
    

