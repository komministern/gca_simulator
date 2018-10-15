﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-


#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.

import functools
from PySide import QtCore, QtGui
from view.myipdialog import MyIPDialog


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
        self.view.button_select_elantazim_center.mousePressEvent(None)
        self.view.button_select_ac_medium.mousePressEvent(None)
        self.view.button_par.mousePressEvent(None)
        # ...more to follow
        
        self.trying_to_connect = False

    def connectSignals(self):
        self.view.quit.connect(self.model.quit)
        
        # Elevation Antenna Azimuth buttons
        self.view.button_select_elantazim_right.pressed.connect(self.newElAntAzimChosen)
        self.view.button_select_elantazim_left.pressed.connect(self.newElAntAzimChosen)
        self.view.button_select_elantazim_center.pressed.connect(self.newElAntAzimChosen)

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

        # Acid entry buttons
        self.view.button_acid_accept.pressed.connect(self.acid_accept)
        self.view.button_acid_clear.pressed.connect(self.acid_clear)
        self.view.button_acid_cancel.pressed.connect(self.acid_cancel)
        self.view.acid_input_text_item.return_pressed.connect(self.acid_return_pressed)
        self.view.acid_entry_window.window_gets_focus.connect(self.acid_window_focused)
        self.view.acid_entry_window.window_gets_shown.connect(self.acid_window_shown)

        # Glideslope entry buttons
        self.view.button_glideslope_accept.pressed.connect(self.glideslope_accept)
        self.view.button_glideslope_clear.pressed.connect(self.glideslope_clear)
        self.view.button_glideslope_cancel.pressed.connect(self.glideslope_cancel)
        self.view.glideslope_input_text_item.return_pressed.connect(self.glideslope_return_pressed)
        self.view.glideslope_entry_window.window_gets_focus.connect(self.glideslope_window_focused)
        self.view.glideslope_entry_window.window_gets_shown.connect(self.glideslope_window_shown)

        # Decsnheight entry buttons
        self.view.button_decsnheight_accept.pressed.connect(self.decsnheight_accept)
        self.view.button_decsnheight_clear.pressed.connect(self.decsnheight_clear)
        self.view.button_decsnheight_cancel.pressed.connect(self.decsnheight_cancel)
        self.view.decsnheight_input_text_item.return_pressed.connect(self.decsnheight_return_pressed)
        self.view.decsnheight_entry_window.window_gets_focus.connect(self.decsnheight_window_focused)
        self.view.decsnheight_entry_window.window_gets_shown.connect(self.decsnheight_window_shown)


        self.connectACSizeButtons()
        self.connectNHistButtons()
        self.connectStatusButtons()
        self.connectRunwaySelectButtons()
        self.connectRangeScaleButtons()
        self.connectElScaleButtons()
        self.connectAzScaleButtons()
        self.connectGlideSlopeButtons()
        self.connectDecisionHeightButtons()
        self.connectAzAntElevButtons()
        self.connectSelDBFldButtons()
        self.connectLeadDirButtons()

        #self.model.new_plot_extracted.connect(self.view.scene.processReceivedPlot)
        self.model.new_plots_extracted.connect(self.view.scene.processReceivedPlots)


        
        
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
        self.view.button_connect.pressed.connect(self.toggleSendingToPlugin)
        #self.view.button_connect.pressed.connect(self.connectToXPlane)
        
        self.view.button_record.pressed.connect(self.toggleRecording)
        self.view.button_demo.pressed.connect(self.toggleDemoMode)
        
        self.view.button_status_fullscreen.pressed.connect(self.fullScreen)
        

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

    def connectDecisionHeightButtons(self):
        self.view.button_select_decsnheight_100.pressed.connect(self.newDecisionHeightChosen)
        self.view.button_select_decsnheight_150.pressed.connect(self.newDecisionHeightChosen)
        self.view.button_select_decsnheight_200.pressed.connect(self.newDecisionHeightChosen)
        self.view.button_select_decsnheight_250.pressed.connect(self.newDecisionHeightChosen)
        self.view.button_select_decsnheight_300.pressed.connect(self.newDecisionHeightChosen)
        self.view.button_select_decsnheight_350.pressed.connect(self.newDecisionHeightChosen)
        self.view.button_select_decsnheight_400.pressed.connect(self.newDecisionHeightChosen)
        self.view.button_select_decsnheight_450.pressed.connect(self.newDecisionHeightChosen)


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

    def toggleSendingToPlugin(self):

        if self.view.scene.active_airport != None and not self.demo_mode:
            if (not self.model.connected) and (not self.trying_to_connect):

                self.dialog = MyIPDialog(self.view)
                ok = self.dialog.exec_()
                if ok:
                
                    
                    self.model.UDP_IP = self.dialog.active_ip_adress()

                    self.model.startSendingToPlugin()
                    self.view.button_connect.setPending(True)
                    self.trying_to_connect = True
                else:
                    #print 'No Hepp'
                    pass
                
            elif (not self.model.connected) and self.trying_to_connect:
                self.model.stopSendingToPlugin()
                self.view.button_connect.setPending(False)
                self.trying_to_connect = False

            elif self.model.connected:
                self.model.connected = False
                self.model.stopSendingToPlugin()
                self.trying_to_connect = False
                self.view.button_connect.setPending(False)
                self.view.button_connect.setInverted(False)
                self.model.connection_lost.emit()


    def fullScreen(self):
        #self.view.status_window.updateTopBorderText('Jesus Lever!')
        if self.view.button_status_fullscreen.inverted:
            self.view.fullscreen = True
            self.view.showFullScreen()
            #self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            #self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        else:
            self.view.showNormal()
            self.view.fullscreen = False
            #self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            #self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)



    # ACID entry
    
    def acid_accept(self, button):
        str = self.view.acid_input_text_item.toPlainText().upper()
        if str[0].isalpha() and str[1:].isalnum() and len(str) <= 7:

            if len(self.view.scene.designated_tracks) > 0:
                self.view.scene.designated_tracks[0].callsign_string = str
                self.view.scene.drawAllTracks()

            self.view.acid_response_text_item.setPlainText(str)
            self.view.acid_error_text_item.setPlainText('')
        else:
            self.view.acid_error_text_item.setPlainText('ERROR')
            self.view.acid_response_text_item.setPlainText('')
        self.view.acid_input_text_item.setFocus()
    
    def acid_clear(self, button):
        self.view.acid_input_text_item.setPlainText('')
        self.view.acid_error_text_item.setPlainText('')
        self.view.acid_response_text_item.setPlainText('')
        self.view.acid_input_text_item.setFocus()
    
    def acid_cancel(self, button):
        if self.view.acid_entry_window.activatingbutton:
            self.view.acid_entry_window.activatingbutton.toggleExpanded()
            self.view.acid_entry_window.activatingbutton = None
        self.view.acid_entry_window.hideWindow()
        button.hoverLeaveEvent(None)    # Just to get rid of some non esthetic things

    def acid_return_pressed(self):
        self.view.button_acid_accept.mousePressEvent(None)
        
    def acid_window_shown(self):
        self.acid_clear(None)
        self.view.acid_input_text_item.setFocus()
        
    def acid_window_focused(self):
        self.view.acid_input_text_item.setFocus()


    # Elevation Antenna Azimuth
    
    def newElAntAzimChosen(self, button):
        if button.value == 1:
            self.view.scene.elantazim = -5.0
            self.model.elantazim = -5.0
            
        elif button.value == 2:
            self.view.scene.elantazim = 0.0
            self.model.elantazim = 0.0
            
        else:
            self.view.scene.elantazim = 5.0
            self.model.elantazim = 5.0
        self.view.scene.drawAzimuthCoverage()

        print self.model.elantazim



    # GlideSlope entry
    
    def glideslope_accept(self, button):
        str = self.view.glideslope_input_text_item.toPlainText()
        
        try:
            angle = float(str)
            
            if angle >= 1.0 and angle <= 15.0:
                angle = round(angle, 1)
                # New glideslope value
                self.view.glideslope_response_text_item.setPlainText(unicode(angle))
                self.view.glideslope_error_text_item.setPlainText('')
                
                # Fix buttons
                if angle >= 2.1 and angle <= 4.0:
                    n = int(round(angle / 0.1)) - 21
                    buttons = [self.view.button_select_glideslope_21, self.view.button_select_glideslope_22,
                               self.view.button_select_glideslope_23, self.view.button_select_glideslope_24,
                               self.view.button_select_glideslope_25, self.view.button_select_glideslope_26,
                               self.view.button_select_glideslope_27, self.view.button_select_glideslope_28,
                               self.view.button_select_glideslope_29, self.view.button_select_glideslope_30,
                               self.view.button_select_glideslope_31, self.view.button_select_glideslope_32,
                               self.view.button_select_glideslope_33, self.view.button_select_glideslope_34,
                               self.view.button_select_glideslope_35, self.view.button_select_glideslope_36,
                               self.view.button_select_glideslope_37, self.view.button_select_glideslope_38,
                               self.view.button_select_glideslope_39, self.view.button_select_glideslope_40]
                    button = buttons[n]
                    button.mousePressEvent(None)
                else:
                    self.view.button_select_glideslope_21.resetExclusiveGroupButtons()
                    
                    self.view.scene.glideslope = angle
                    self.view.scene.drawGlideSlope()
                    self.view.scene.drawDecisionHeight()
                    self.view.scene.drawAllElevationTracks()
                    
            else:
                self.view.glideslope_error_text_item.setPlainText('ERROR')
                self.view.glideslope_response_text_item.setPlainText('')
                
            
        except ValueError:
            self.view.glideslope_error_text_item.setPlainText('VALUE ERROR')
            self.view.glideslope_response_text_item.setPlainText('')

        self.view.glideslope_input_text_item.setFocus()
    
    def glideslope_clear(self, button):
        self.view.glideslope_input_text_item.setPlainText('')
        self.view.glideslope_error_text_item.setPlainText('')
        self.view.glideslope_response_text_item.setPlainText('')
        self.view.glideslope_input_text_item.setFocus()
    
    def glideslope_cancel(self, button):
        if self.view.glideslope_entry_window.activatingbutton:
            self.view.glideslope_entry_window.activatingbutton.toggleExpanded()
            self.view.glideslope_entry_window.activatingbutton = None
        self.view.glideslope_entry_window.hideWindow()
        button.hoverLeaveEvent(None)    # Just to get rid of some non esthetic things

    def glideslope_return_pressed(self):
        self.view.button_glideslope_accept.mousePressEvent(None)
        
    def glideslope_window_shown(self):
        self.glideslope_clear(None)
        self.view.glideslope_input_text_item.setFocus()
        
    def glideslope_window_focused(self):
        self.view.glideslope_input_text_item.setFocus()
        



    # DecsnHeight entry
    
    def decsnheight_accept(self, button):
        str = self.view.decsnheight_input_text_item.toPlainText()
        
        try:
            height = int(str)
            
            if height >= 0 and height <= 999:
                
                self.view.decsnheight_response_text_item.setPlainText(unicode(height))
                self.view.decsnheight_error_text_item.setPlainText('')
                
                # Fix buttons
                if height in [100, 150, 200, 250, 300, 350, 400, 450]:
                    n = (height / 50) - 2
                    buttons = [self.view.button_select_decsnheight_100, self.view.button_select_decsnheight_150,
                               self.view.button_select_decsnheight_200, self.view.button_select_decsnheight_250,
                               self.view.button_select_decsnheight_300, self.view.button_select_decsnheight_350,
                               self.view.button_select_decsnheight_400, self.view.button_select_decsnheight_450]
                    button = buttons[n]
                    button.mousePressEvent(None)
                else:
                    self.view.button_select_decsnheight_100.resetExclusiveGroupButtons()
                    
                    self.view.scene.decisionheight = height
                    self.view.scene.drawDecisionHeight()
                    #self.view.scene.drawAllElevationTracks()
                    
                    #print height
                    
            else:
                self.view.decsnheight_error_text_item.setPlainText('ERROR')
                self.view.decsnheight_response_text_item.setPlainText('')
                
            
        except ValueError:
            self.view.decsnheight_error_text_item.setPlainText('VALUE ERROR')
            self.view.decsnheight_response_text_item.setPlainText('')

        self.view.decsnheight_input_text_item.setFocus()
    
    def decsnheight_clear(self, button):
        self.view.decsnheight_input_text_item.setPlainText('')
        self.view.decsnheight_error_text_item.setPlainText('')
        self.view.decsnheight_response_text_item.setPlainText('')
        self.view.decsnheight_input_text_item.setFocus()
    
    def decsnheight_cancel(self, button):
        if self.view.decsnheight_entry_window.activatingbutton:
            self.view.decsnheight_entry_window.activatingbutton.toggleExpanded()
            self.view.decsnheight_entry_window.activatingbutton = None
        self.view.decsnheight_entry_window.hideWindow()
        button.hoverLeaveEvent(None)    # Just to get rid of some non esthetic things

    def decsnheight_return_pressed(self):
        self.view.button_decsnheight_accept.mousePressEvent(None)
        
    def decsnheight_window_shown(self):
        self.decsnheight_clear(None)
        self.view.decsnheight_input_text_item.setFocus()
        
    def decsnheight_window_focused(self):
        self.view.decsnheight_input_text_item.setFocus()











    def toggleDemoMode(self):
        # button_demo is a normal Button
        if not self.demo_mode and not self.connected:
            #if not self.view.button_demo.inverted:
            
            self.model.initDemoMode()
            
            #print self.view.button_demo.inverted
            self.view.button_demo.toggleInverted()
            #print self.view.button_demo.inverted
            
            #print 'enter demo mode'
            #self.model.initDemoMode()
        elif self.demo_mode:
            #print 'exit demo mode'
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
        
        rwy_names = {}
        for runway_number in airport.runways:
            rwy_names[runway_number] = airport.runways[runway_number]['name']
        self.view.runwayselect_window = self.view.createRunwaySelectWindow(rwy_names)
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
        if self.view.fullscreen:
            self.view.button_status_fullscreen.toggleInverted()
        self.view.status_window.showWindow(self.view.button_status)


    def updateStatusWindow(self, count, latest_delay, mean_delay, std_delay):
        self.view.status_window_area.updateDynamicTextItem('ip','IP address:\t\t' + self.model.UDP_IP )
        self.view.status_window_area.updateDynamicTextItem('count', 'Message count:\t' + str(count) )
        self.view.status_window_area.updateDynamicTextItem('delay', 'Latest delay:\t\t{0:.3f}'.format(latest_delay) )
        self.view.status_window_area.updateDynamicTextItem('mean', 'Mean delay:\t\t{0:.3f}'.format(mean_delay) )
        self.view.status_window_area.updateDynamicTextItem('std', 'Std dev:\t\t{0:.3f}'.format(std_delay) )


    def updateConnectedState(self, new_connected_state):

        # The self.connected property actually IS the self.view.button_connect.inverted value!!! NOOOOOOOOOOOOOOOOOOO, this i STUPID!!!
        
        print self.trying_to_connect

        if new_connected_state == True:
            self.view.button_connect.setPending(False)
            self.view.button_connect.setInverted(True)

        elif new_connected_state == False:

            self.view.button_connect.setInverted(False)
            
            if self.trying_to_connect == True:
                self.view.button_connect.setPending(True)
                
            else:
                self.view.button_connect.setPending(False)
                

        #if self.connected ^ new_connected_state:
        #    self.view.button_connect.toggleInverted()

        #if not self.connected and self.trying_to_connect:
        #    self.view.button_connect.

        if self.connected:
            self.view.scene.alerts_field.addAlert('RADAR READY FOR USE')
            self.view.scene.connected = True                                            # ????????????????????
        
        elif not self.connected:
            self.view.status_window_area.updateDynamicTextItem('ip','IP address:')
            self.view.status_window_area.updateDynamicTextItem('count', 'Message count:')
            self.view.status_window_area.updateDynamicTextItem('delay', 'Latest delay:')
            self.view.status_window_area.updateDynamicTextItem('mean', 'Mean delay:')
            self.view.status_window_area.updateDynamicTextItem('std', 'Std dev:')
            
            if self.radiating:
                self.view.button_radiate.mousePressEvent(None)
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
            
            #self.view.scene.removeAllTracks()
            
            self.view.scene.removeAllTracks()
            self.view.scene.drawAllGraphics()
            
            

            

                
    def newACSizeChosen(self, button):

        if len(self.view.scene.designated_tracks) > 0:
            
            self.view.scene.designated_tracks[0].size_string = button.value

            self.view.scene.drawAllTracks()

    def newLeadDirChosen(self, button):

        if len(self.view.scene.designated_tracks) > 0:

            if button.text == 'ALL':
                for each in self.view.scene.designated_tracks[1:]:
                    each.elevation_label.x_offset = self.view.scene.designated_tracks[0].elevation_label.x_offset
                    each.elevation_label.y_offset = self.view.scene.designated_tracks[0].elevation_label.y_offset
                    
                    each.azimuth_label.x_offset = self.view.scene.designated_tracks[0].azimuth_label.x_offset
                    each.azimuth_label.y_offset = self.view.scene.designated_tracks[0].azimuth_label.y_offset
                
            else:

                index = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW').index(button.text)
                dx, dy = ((0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1))[index]
                x_offset, y_offset = self.view.scene.label_standard_x_offset_magnitude*dx, self.view.scene.label_standard_y_offset_magnitude*dy
                
                self.view.scene.designated_tracks[0].elevation_label.x_offset = x_offset
                self.view.scene.designated_tracks[0].elevation_label.y_offset = y_offset
                
                self.view.scene.designated_tracks[0].azimuth_label.x_offset = x_offset
                self.view.scene.designated_tracks[0].azimuth_label.y_offset = y_offset
                
            self.view.scene.drawAllTracks()


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
        self.view.button_select_elantazim_center.mousePressEvent(None)



        
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
            
            self.model.azantelev = self.view.scene.azantelev    # This is not good. States like this one should reside in the model only!
                #self.view.scene.drawElevationCoverage()


    def newGlideSlopeChosen(self, button):
        if button.value != self.view.scene.glideslope:
            self.view.scene.glideslope = button.value
            self.view.scene.drawGlideSlope()
            self.view.scene.drawDecisionHeight()
            self.view.scene.drawAllElevationTracks()


    def newDecisionHeightChosen(self, button):
        if button.value != self.view.scene.decisionheight:
            self.view.scene.decisionheight = button.value
            self.view.scene.drawDecisionHeight()
            #self.view.scene.drawDecisionHeight()




    def newRunwayChosen(self, button):
        if self.model.active_runway != None:
            # No runway change should register when loading airport for the first time! Why?
            
            #if not self.demo_mode:
            self.view.scene.alerts_field.addAlert('RUNWAY CHANGE IN PROGRESS', delay=100.0)
            self.view.scene.alerts_field.addAlert('RUNWAY CHANGE COMPLETED', delay=1100.0)
                
            if self.radiating:
                self.view.button_radiate.mousePressEvent(None)
                self.view.scene.drawAllTracks()
                laterRadiate = functools.partial(self.view.button_radiate.mousePressEvent, None)
                self.radiate_timer = QtCore.QTimer.singleShot(1200.0, laterRadiate)
        
        #print(self.model.active_runway)

        if button.value != self.model.active_runway:

            self.model.active_runway = button.value
            self.view.scene.active_runway = button.value

            gs = int(round(10 * self.model.airport.runways[self.model.active_runway]['gs'])) - 21

            buttons = [self.view.button_select_glideslope_21, self.view.button_select_glideslope_22, self.view.button_select_glideslope_23, self.view.button_select_glideslope_24, 
                        self.view.button_select_glideslope_25, self.view.button_select_glideslope_26, self.view.button_select_glideslope_27, self.view.button_select_glideslope_28,
                        self.view.button_select_glideslope_29, self.view.button_select_glideslope_30, self.view.button_select_glideslope_31, self.view.button_select_glideslope_32,
                        self.view.button_select_glideslope_33, self.view.button_select_glideslope_34, self.view.button_select_glideslope_35, self.view.button_select_glideslope_36,
                        self.view.button_select_glideslope_37, self.view.button_select_glideslope_38, self.view.button_select_glideslope_39, self.view.button_select_glideslope_40]

            buttons[gs].mousePressEvent(None)
            #self.view.scene.active_airport[]
            
            self.view.scene.removeAllTracks()
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




    # Radar Control buttons
    
    def toggleRadiation(self, button):
        if (not self.antenna_drive_on) and self.radiating:
            # If antenna drive is off, turn radiation off as well
            button.toggleInverted()
            self.view.scene.alerts_field.addAlert('ANTENNA DRIVE NOT READY')
        if not self.radiating:
            # If radiate just was turned off, clear the tracks
            self.view.scene.removeAllTracks()
        
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






