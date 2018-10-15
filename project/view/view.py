#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright © 2016, 2017 Oscar Franzén <oscarfranzen@yahoo.se>
#
#    This file is part of GCA Simulator.




from PySide import QtGui, QtCore
from scene import MyScene
from window import WindowArea, WindowTopBorder, StatusWindowArea, InputWindowArea
from button import Button, InvertingButton, ExpandingButton, FlashingButton, PendingButton
from mygraphicstextitem import MyGraphicsTextItem



class MyView(QtGui.QGraphicsView):

    quit = QtCore.Signal()

    def __init__(self):
        super(MyView, self).__init__()

        self.resize(1920, 1080)
        self.scene = MyScene()
        self.setScene(self.scene)

        # **** CREATE ALL THE BUTTON WINDOWS WITH ALL THEIR BUTTONS

        self.leaddir_window = self.createLeadDirWindow()
        self.status_window = self.createStatusWindow()
        self.seldbfld_window = self.createSelDBFldWindow()
        
        self.decsnheight_entry_window = self.createDecsnHeightEntryWindow()
        
        self.decsnheight_window = self.createDecsnHeightWindow()
        self.elantazim_window = self.createSetElAntAzimWindow()
        
        self.glideslope_entry_window = self.createGlideSlopeEntryWindow()
        
        self.glideslope_window = self.createSetGlideSlopeWindow()
        self.azantelev_window = self.createSetAzAntElevWindow()
        self.stc_window = self.createSTCWindow()
        self.nhist_window = self.createSetNHistWindow()
        self.elscale_window = self.createElScaleWindow()
        self.azscale_window = self.createAzScaleWindow()
        self.ac_window = self.createACWindow()
        self.displaycontrol_window = self.createDisplayControlWindow()
        
        self.acid_entry_window = self.createACIDEntryWindow()
        
        self.radarcontrol_window = self.createRadarControlWindow()
        self.radarmode_window = self.createRadarModeWindow()
        self.runwayselect_window = self.createRunwaySelectWindow()
        self.main_window = self.createMainWindow()
        
        self.main_window.setZValue(self.scene.getNewZVal())


        self.fullscreen = False


        # **** CREATE THE 


    def createDecsnHeightEntryWindow(self):
        self.decsnheight_entry_window_area = InputWindowArea()
        self.scene.addItem(self.decsnheight_entry_window_area)

        self.decsnheight_entry_window_area.newTextRowLeft('HeightT')
        self.decsnheight_entry_window_area.endRow()
        self.decsnheight_entry_window_area.newTextRowLeft('Height = Decision Height')
        self.decsnheight_entry_window_area.endRow()
        self.decsnheight_entry_window_area.newTextRowLeft('In XXX Feet')
        self.decsnheight_entry_window_area.endRow()
        self.decsnheight_entry_window_area.newTextRowLeft('Height = 0-999')
        self.decsnheight_entry_window_area.endRow()
        self.decsnheight_entry_window_area.newTextRowLeft('')
        self.decsnheight_entry_window_area.endRow()
        self.decsnheight_entry_window_area.newTextRowLeft('ERROR')
        self.decsnheight_entry_window_area.endRow()
        
        self.decsnheight_error_text_item = MyGraphicsTextItem(editable=False)
        self.decsnheight_entry_window_area.registerGraphicsTextItem(self.decsnheight_error_text_item)
        self.decsnheight_entry_window_area.endRow()

        self.decsnheight_entry_window_area.newTextRowLeft('INPUT')
        self.decsnheight_entry_window_area.endRow()

        self.decsnheight_input_text_item = MyGraphicsTextItem(editable=True)
        self.decsnheight_entry_window_area.registerGraphicsTextItem(self.decsnheight_input_text_item)
        self.decsnheight_entry_window_area.endRow()

        self.decsnheight_entry_window_area.newTextRowLeft('RESPONSE')
        self.decsnheight_entry_window_area.endRow()

        self.decsnheight_response_text_item = MyGraphicsTextItem(editable=False)
        self.decsnheight_entry_window_area.registerGraphicsTextItem(self.decsnheight_response_text_item)
        self.decsnheight_entry_window_area.endRow()

        self.decsnheight_entry_window_area.newFullButtonRow(4)
        self.decsnheight_entry_window_area.skipNextButton()

        self.button_decsnheight_accept = FlashingButton('Accept')
        self.decsnheight_entry_window_area.registerNextButton(self.button_decsnheight_accept)
        self.button_decsnheight_clear = FlashingButton('Clear')
        self.decsnheight_entry_window_area.registerNextButton(self.button_decsnheight_clear)
        self.button_decsnheight_cancel = FlashingButton('Cancel')
        self.decsnheight_entry_window_area.registerNextButton(self.button_decsnheight_cancel)
        self.decsnheight_entry_window_area.endRow()
        
        self.decsnheight_entry_window_area.fixWindow()
        
        self.decsnheight_entry_window_topborder = WindowTopBorder('Decision Height Entry XX:XX:XX')
        self.scene.addItem(self.decsnheight_entry_window_topborder)
        self.scene.registerWindowTopBorder(self.decsnheight_entry_window_topborder)
        self.decsnheight_entry_window_area.attachTo(self.decsnheight_entry_window_topborder)
        return self.decsnheight_entry_window_topborder







    def createGlideSlopeEntryWindow(self):
        self.glideslope_entry_window_area = InputWindowArea()
        self.scene.addItem(self.glideslope_entry_window_area)

        #self.glideslope_entry_window_area.newTextRowLeft('')
        #self.glideslope_entry_window_area.endRow()
        self.glideslope_entry_window_area.newTextRowLeft('Angle')
        self.glideslope_entry_window_area.endRow()
        self.glideslope_entry_window_area.newTextRowLeft(' Angle = Glide Slope Angle')
        self.glideslope_entry_window_area.endRow()
        self.glideslope_entry_window_area.newTextRowLeft('In XX.X Degrees')
        self.glideslope_entry_window_area.endRow()
        self.glideslope_entry_window_area.newTextRowLeft('Angle = 1.0-15.0')
        self.glideslope_entry_window_area.endRow()
        self.glideslope_entry_window_area.newTextRowLeft('')
        self.glideslope_entry_window_area.endRow()
        self.glideslope_entry_window_area.newTextRowLeft('ERROR')
        self.glideslope_entry_window_area.endRow()
        
        self.glideslope_error_text_item = MyGraphicsTextItem(editable=False)
        self.glideslope_entry_window_area.registerGraphicsTextItem(self.glideslope_error_text_item)
        self.glideslope_entry_window_area.endRow()

        self.glideslope_entry_window_area.newTextRowLeft('INPUT')
        self.glideslope_entry_window_area.endRow()

        self.glideslope_input_text_item = MyGraphicsTextItem(editable=True)
        self.glideslope_entry_window_area.registerGraphicsTextItem(self.glideslope_input_text_item)
        self.glideslope_entry_window_area.endRow()

        self.glideslope_entry_window_area.newTextRowLeft('RESPONSE')
        self.glideslope_entry_window_area.endRow()

        self.glideslope_response_text_item = MyGraphicsTextItem(editable=False)
        self.glideslope_entry_window_area.registerGraphicsTextItem(self.glideslope_response_text_item)
        self.glideslope_entry_window_area.endRow()

        self.glideslope_entry_window_area.newFullButtonRow(4)
        self.glideslope_entry_window_area.skipNextButton()

        self.button_glideslope_accept = FlashingButton('Accept')
        self.glideslope_entry_window_area.registerNextButton(self.button_glideslope_accept)
        self.button_glideslope_clear = FlashingButton('Clear')
        self.glideslope_entry_window_area.registerNextButton(self.button_glideslope_clear)
        self.button_glideslope_cancel = FlashingButton('Cancel')
        self.glideslope_entry_window_area.registerNextButton(self.button_glideslope_cancel)
        self.glideslope_entry_window_area.endRow()
        
        self.glideslope_entry_window_area.fixWindow()
        
        self.glideslope_entry_window_topborder = WindowTopBorder('Glideslope Entry XX:XX:XX')
        self.scene.addItem(self.glideslope_entry_window_topborder)
        self.scene.registerWindowTopBorder(self.glideslope_entry_window_topborder)
        self.glideslope_entry_window_area.attachTo(self.glideslope_entry_window_topborder)
        return self.glideslope_entry_window_topborder


    def createACIDEntryWindow(self):
        self.acid_entry_window_area = InputWindowArea()
        self.scene.addItem(self.acid_entry_window_area)

        self.acid_entry_window_area.newTextRowLeft('1) Pick Designated AC.')
        self.acid_entry_window_area.endRow()
        self.acid_entry_window_area.newTextRowLeft('2) Enter ACID.')
        self.acid_entry_window_area.endRow()
        self.acid_entry_window_area.newTextRowLeft('')
        self.acid_entry_window_area.endRow()
        self.acid_entry_window_area.newTextRow('ACID = AXXXXXX')
        self.acid_entry_window_area.endRow()
        self.acid_entry_window_area.newTextRowLeft('')
        self.acid_entry_window_area.endRow()
        self.acid_entry_window_area.newTextRowLeft('ERROR')
        self.acid_entry_window_area.endRow()
        
        self.acid_error_text_item = MyGraphicsTextItem(editable=False)
        self.acid_entry_window_area.registerGraphicsTextItem(self.acid_error_text_item)
        self.acid_entry_window_area.endRow()

        self.acid_entry_window_area.newTextRowLeft('INPUT')
        self.acid_entry_window_area.endRow()

        self.acid_input_text_item = MyGraphicsTextItem(editable=True)
        self.acid_entry_window_area.registerGraphicsTextItem(self.acid_input_text_item)
        self.acid_entry_window_area.endRow()

        self.acid_entry_window_area.newTextRowLeft('RESPONSE')
        self.acid_entry_window_area.endRow()

        self.acid_response_text_item = MyGraphicsTextItem(editable=False)
        self.acid_entry_window_area.registerGraphicsTextItem(self.acid_response_text_item)
        self.acid_entry_window_area.endRow()

        self.acid_entry_window_area.newFullButtonRow(4)
        self.acid_entry_window_area.skipNextButton()

        self.button_acid_accept = FlashingButton('Accept')
        self.acid_entry_window_area.registerNextButton(self.button_acid_accept)
        self.button_acid_clear = FlashingButton('Clear')
        self.acid_entry_window_area.registerNextButton(self.button_acid_clear)
        self.button_acid_cancel = FlashingButton('Cancel')
        self.acid_entry_window_area.registerNextButton(self.button_acid_cancel)
        self.acid_entry_window_area.endRow()
        
        self.acid_entry_window_area.fixWindow()
        
        self.acid_entry_window_topborder = WindowTopBorder('Acid Entry XX:XX:XX')
        self.scene.addItem(self.acid_entry_window_topborder)
        self.scene.registerWindowTopBorder(self.acid_entry_window_topborder)
        self.acid_entry_window_area.attachTo(self.acid_entry_window_topborder)
        return self.acid_entry_window_topborder






    def createStatusWindow(self, airport=None):

        self.status_window_area = StatusWindowArea()
        self.scene.addItem(self.status_window_area)
        
        if airport:
        
            self.status_window_area.newTextRowLeft('ICAO/IATA: ' + airport.icao + '/' + airport.iata)
            self.status_window_area.endRow()
        
            #counter = 1
            for runway_number in airport.runways:
                
                self.status_window_area.newTextRowLeft('RWY' + str(runway_number) + ': ' + airport.runways[runway_number]['name'])
                self.status_window_area.endRow()
                
                self.status_window_area.newTextRowLeft('  THR Lon, Lat, El: ' + str(airport.runways[runway_number]['thr_lon']) + ', ' + str(airport.runways[runway_number]['thr_lat']) + ', ' + str(airport.runways[runway_number]['thr_el']) )
                self.status_window_area.endRow()
                self.status_window_area.newTextRowLeft('  Dist to TD (m): ' + str(airport.runways[runway_number]['td']))
                self.status_window_area.endRow()
                
                #self.status_window_area.newTextRowLeft('  TD: ' + str(counter) + ': ' + each['name'])
                #self.status_window_area.endRow()
                #self.status_window_area.newTextRowLeft('  TD: ' + str(counter) + ': ' + each['name'])
                #self.status_window_area.endRow()
                
                
                #counter += 1
        
            self.status_window_area.newTextRowLeft('Plot Bias Z (ft): ' + '0.0')
            self.status_window_area.endRow()
        
        else:
            self.status_window_area.newTextRowLeft('ICAO/IATA: ')
            self.status_window_area.endRow()

        self.status_window_area.newWhiteLineSeparator()
        self.status_window_area.endRow()
        
        self.status_window_area.newFullButtonRow(3)
        self.button_load_new_airport = Button('Load\nAirport')
        self.status_window_area.registerNextButton(self.button_load_new_airport)
        
        self.button_connect = PendingButton('Connect')
        self.status_window_area.registerNextButton(self.button_connect)
        
        self.button_demo = Button('Demo\nMode')
        self.status_window_area.registerNextButton(self.button_demo)
        
        self.status_window_area.endRow()
        
        self.status_window_area.newHalfButtonRow(3)                     # TEMPORARY
        self.button_record = Button('Record')                  #
        self.status_window_area.registerNextButton(self.button_record)  #
        self.button_status_fullscreen = InvertingButton('Fullscreen')                  #
        self.status_window_area.registerNextButton(self.button_status_fullscreen)  #
        self.status_window_area.endRow()

        self.status_window_area.newWhiteLineSeparator()
        self.status_window_area.endRow()

        self.status_window_area.newTextRowLeft('IP address:     ', dynamic=True, identifier='ip')
        self.status_window_area.endRow()
        self.status_window_area.newTextRowLeft('Message count:  ', dynamic=True, identifier='count')
        self.status_window_area.endRow()
        self.status_window_area.newTextRowLeft('Latest delay:   ', dynamic=True, identifier='delay')
        self.status_window_area.endRow()
        self.status_window_area.newTextRowLeft('Mean delay:     ', dynamic=True, identifier='mean')
        self.status_window_area.endRow()
        self.status_window_area.newTextRowLeft('Std dev:        ', dynamic=True, identifier='std')
        self.status_window_area.endRow()
        
        self.status_window_area.fixWindow()
        
        self.status_window_topborder = WindowTopBorder('Status')
        self.scene.addItem(self.status_window_topborder)
        self.scene.registerWindowTopBorder(self.status_window_topborder)
        self.status_window_area.attachTo(self.status_window_topborder)
        return self.status_window_topborder


    def createLeadDirWindow(self):
        self.leaddir_window_area = WindowArea()
        self.scene.addItem(self.leaddir_window_area)
        
        self.leaddir_window_area.newHalfButtonRow(5)
        self.leaddir_window_area.skipNextButton()
        self.leaddir_window_area.skipNextButton()
        self.button_north = FlashingButton('N')
        self.leaddir_window_area.registerNextButton(self.button_north)
        self.leaddir_window_area.endRow()
        
        self.leaddir_window_area.newHalfButtonRow(5)
        self.leaddir_window_area.skipNextButton()
        self.button_northwest = FlashingButton('NW')
        self.leaddir_window_area.registerNextButton(self.button_northwest)
        self.leaddir_window_area.skipNextButton()
        self.button_northeast = FlashingButton('NE')
        self.leaddir_window_area.registerNextButton(self.button_northeast)
        self.leaddir_window_area.endRow()
        
        self.leaddir_window_area.newHalfButtonRow(5)
        self.button_west = FlashingButton('W')
        self.leaddir_window_area.registerNextButton(self.button_west)
        self.leaddir_window_area.skipNextButton()
        self.leaddir_window_area.skipNextButton()
        self.leaddir_window_area.skipNextButton()
        self.button_east = FlashingButton('E')
        self.leaddir_window_area.registerNextButton(self.button_east)
        self.leaddir_window_area.endRow()
        
        self.leaddir_window_area.newHalfButtonRow(5)
        self.leaddir_window_area.skipNextButton()
        self.button_southwest = FlashingButton('SW')
        self.leaddir_window_area.registerNextButton(self.button_southwest)
        self.leaddir_window_area.skipNextButton()
        self.button_southeast = FlashingButton('SE')
        self.leaddir_window_area.registerNextButton(self.button_southeast)
        self.leaddir_window_area.endRow()
        
        self.leaddir_window_area.newHalfButtonRow(5)
        self.leaddir_window_area.skipNextButton()
        self.leaddir_window_area.skipNextButton()
        self.button_south = FlashingButton('S')
        self.leaddir_window_area.registerNextButton(self.button_south)
        self.leaddir_window_area.skipNextButton()
        self.button_all = FlashingButton('ALL')
        self.leaddir_window_area.registerNextButton(self.button_all)
        self.leaddir_window_area.endRow()

        self.leaddir_window_area.fixWindow()
        self.leaddir_window_topborder = WindowTopBorder('Leader Direction')
        self.scene.addItem(self.leaddir_window_topborder)
        self.scene.registerWindowTopBorder(self.leaddir_window_topborder)
        self.leaddir_window_area.attachTo(self.leaddir_window_topborder)
        return self.leaddir_window_topborder


    def createSelDBFldWindow(self):
        self.seldbfld_window_area = WindowArea()
        self.scene.addItem(self.seldbfld_window_area)
        self.seldbfld_window_area.newFullButtonRow(3)
        self.button_line1 = InvertingButton('TOGGLE\nLINE 1')
        self.seldbfld_window_area.registerNextButton(self.button_line1)
        self.button_line2 = InvertingButton('TOGGLE\nLINE 2')
        self.seldbfld_window_area.registerNextButton(self.button_line2)
        self.button_line3 = InvertingButton('TOGGLE\nLINE 3')
        self.seldbfld_window_area.registerNextButton(self.button_line3)
        self.seldbfld_window_area.endRow()
        self.seldbfld_window_area.newFullButtonRow(3)
        self.button_leader = InvertingButton('TOGGLE\nLEADER')
        self.seldbfld_window_area.registerNextButton(self.button_leader)
        self.button_fdb = InvertingButton('TOGGLE\nFDB')
        self.seldbfld_window_area.registerNextButton(self.button_fdb)
        self.seldbfld_window_area.skipNextButton()
        self.seldbfld_window_area.endRow()
        self.seldbfld_window_area.fixWindow()
        self.seldbfld_window_topborder = WindowTopBorder('SELECT FEATURES')
        self.scene.addItem(self.seldbfld_window_topborder)
        self.scene.registerWindowTopBorder(self.seldbfld_window_topborder)
        self.seldbfld_window_area.attachTo(self.seldbfld_window_topborder)
        return self.seldbfld_window_topborder



    def createDecsnHeightWindow(self):
        self.decsnheight_window_area = WindowArea()
        self.scene.addItem(self.decsnheight_window_area)
        self.decsnheight_window_area.newHalfButtonRow(4)
        self.decsnheightexclusivegrouplist = []
        self.button_select_decsnheight_100 = InvertingButton('100', value=100, exclusivegroup=self.decsnheightexclusivegrouplist)
        self.decsnheight_window_area.registerNextButton(self.button_select_decsnheight_100)
        self.button_select_decsnheight_150 = InvertingButton('150', value=150, exclusivegroup=self.decsnheightexclusivegrouplist)
        self.decsnheight_window_area.registerNextButton(self.button_select_decsnheight_150)
        self.button_select_decsnheight_200 = InvertingButton('200', value=200, exclusivegroup=self.decsnheightexclusivegrouplist)
        self.decsnheight_window_area.registerNextButton(self.button_select_decsnheight_200)
        self.button_select_decsnheight_250 = InvertingButton('250', value=250, exclusivegroup=self.decsnheightexclusivegrouplist)
        self.decsnheight_window_area.registerNextButton(self.button_select_decsnheight_250)
        self.decsnheight_window_area.endRow()
        self.decsnheight_window_area.newHalfButtonRow(4)
        self.button_select_decsnheight_300 = InvertingButton('300', value=300, exclusivegroup=self.decsnheightexclusivegrouplist)
        self.decsnheight_window_area.registerNextButton(self.button_select_decsnheight_300)
        self.button_select_decsnheight_350 = InvertingButton('350', value=350, exclusivegroup=self.decsnheightexclusivegrouplist)
        self.decsnheight_window_area.registerNextButton(self.button_select_decsnheight_350)
        self.button_select_decsnheight_400 = InvertingButton('400', value=400, exclusivegroup=self.decsnheightexclusivegrouplist)
        self.decsnheight_window_area.registerNextButton(self.button_select_decsnheight_400)
        self.button_select_decsnheight_450 = InvertingButton('450', value=450, exclusivegroup=self.decsnheightexclusivegrouplist)
        self.decsnheight_window_area.registerNextButton(self.button_select_decsnheight_450)
        self.decsnheight_window_area.endRow()
        self.decsnheight_window_area.newFullButtonRow(4)
        self.button_select_decsnheight_Kbd = ExpandingButton('Kbd', self.decsnheight_entry_window)
        self.decsnheight_window_area.registerNextButton(self.button_select_decsnheight_Kbd)
        self.decsnheight_window_area.skipNextButton()
        self.decsnheight_window_area.skipNextButton()
        self.decsnheight_window_area.skipNextButton()
        self.decsnheight_window_area.endRow()
        self.decsnheight_window_area.fixWindow()
        self.decsnheight_window_topborder = WindowTopBorder('Decision Height')
        self.scene.addItem(self.decsnheight_window_topborder)
        self.scene.registerWindowTopBorder(self.decsnheight_window_topborder)
        self.decsnheight_window_area.attachTo(self.decsnheight_window_topborder)
        return self.decsnheight_window_topborder
 


    def createSetElAntAzimWindow(self):
        self.elantazim_window_area = WindowArea()
        self.scene.addItem(self.elantazim_window_area)
        self.elantazim_window_area.newHalfButtonRow(3)
        self.setelantazimexclusivegrouplist = []
        self.button_select_elantazim_left = InvertingButton('LEFT', value=1, exclusivegroup=self.setelantazimexclusivegrouplist)
        self.elantazim_window_area.registerNextButton(self.button_select_elantazim_left)
        self.button_select_elantazim_center = InvertingButton('CENTER', value=2, exclusivegroup=self.setelantazimexclusivegrouplist)
        self.elantazim_window_area.registerNextButton(self.button_select_elantazim_center)
        self.button_select_elantazim_right = InvertingButton('RIGHT', value=3, exclusivegroup=self.setelantazimexclusivegrouplist)
        self.elantazim_window_area.registerNextButton(self.button_select_elantazim_right)
        self.elantazim_window_area.endRow()
        self.elantazim_window_area.fixWindow()
        self.elantazim_window_topborder = WindowTopBorder('Elevation Ant Azimuth')
        self.scene.addItem(self.elantazim_window_topborder)
        self.scene.registerWindowTopBorder(self.elantazim_window_topborder)
        self.elantazim_window_area.attachTo(self.elantazim_window_topborder)
        return self.elantazim_window_topborder

        

    def createSetGlideSlopeWindow(self):
        self.glideslope_window_area = WindowArea()
        self.scene.addItem(self.glideslope_window_area)
        self.setglideslopeexclusivegrouplist = []
        self.glideslope_window_area.newHalfButtonRow(5)
        self.button_select_glideslope_21 = InvertingButton('2.1', value=2.1, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_21)
        self.button_select_glideslope_22 = InvertingButton('2.2', value=2.2, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_22)
        self.button_select_glideslope_23 = InvertingButton('2.3', value=2.3, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_23)
        self.button_select_glideslope_24 = InvertingButton('2.4', value=2.4, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_24)
        self.button_select_glideslope_25 = InvertingButton('2.5', value=2.5, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_25)
        self.glideslope_window_area.endRow()
        self.glideslope_window_area.newHalfButtonRow(5)
        self.button_select_glideslope_26 = InvertingButton('2.6', value=2.6, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_26)
        self.button_select_glideslope_27 = InvertingButton('2.7', value=2.7, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_27)
        self.button_select_glideslope_28 = InvertingButton('2.8', value=2.8, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_28)
        self.button_select_glideslope_29 = InvertingButton('2.9', value=2.9, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_29)
        self.button_select_glideslope_30 = InvertingButton('3', value=3.0, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_30)
        self.glideslope_window_area.endRow()
        self.glideslope_window_area.newHalfButtonRow(5)
        self.button_select_glideslope_31 = InvertingButton('3.1', value=3.1, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_31)
        self.button_select_glideslope_32 = InvertingButton('3.2', value=3.2, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_32)
        self.button_select_glideslope_33 = InvertingButton('3.3', value=3.3, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_33)
        self.button_select_glideslope_34 = InvertingButton('3.4', value=3.4, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_34)
        self.button_select_glideslope_35 = InvertingButton('3.5', value=3.5, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_35)
        self.glideslope_window_area.endRow()
        self.glideslope_window_area.newHalfButtonRow(5)
        self.button_select_glideslope_36 = InvertingButton('3.6', value=3.6, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_36)
        self.button_select_glideslope_37 = InvertingButton('3.7', value=3.7, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_37)
        self.button_select_glideslope_38 = InvertingButton('3.8', value=3.8, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_38)
        self.button_select_glideslope_39 = InvertingButton('3.9', value=3.9, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_39)
        self.button_select_glideslope_40 = InvertingButton('4', value=4.0, exclusivegroup=self.setglideslopeexclusivegrouplist)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_40)
        self.glideslope_window_area.endRow()
        self.glideslope_window_area.newFullButtonRow(5)
        self.button_select_glideslope_Kbd = ExpandingButton('Kbd', self.glideslope_entry_window)
        self.glideslope_window_area.registerNextButton(self.button_select_glideslope_Kbd)
        self.glideslope_window_area.skipNextButton()
        self.glideslope_window_area.skipNextButton()
        self.glideslope_window_area.skipNextButton()
        self.glideslope_window_area.skipNextButton()
        self.glideslope_window_area.endRow()
        self.glideslope_window_area.fixWindow()
        self.glideslope_window_topborder = WindowTopBorder('Select Glide Slope')
        self.scene.addItem(self.glideslope_window_topborder)
        self.scene.registerWindowTopBorder(self.glideslope_window_topborder)
        self.glideslope_window_area.attachTo(self.glideslope_window_topborder)
        return self.glideslope_window_topborder



    def createSetAzAntElevWindow(self):
        self.azantelev_window_area = WindowArea()
        self.scene.addItem(self.azantelev_window_area)
        self.setazantelevexclusivegrouplist = []
        self.azantelev_window_area.newHalfButtonRow(5)
        self.button_select_azantalev_000 = InvertingButton('0', value=0.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_000)
        self.button_select_azantalev_005 = InvertingButton('0.5', value=0.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_005)
        self.button_select_azantalev_010 = InvertingButton('1', value=1.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_010)
        self.button_select_azantalev_015 = InvertingButton('1.5', value=1.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_015)
        self.button_select_azantalev_020 = InvertingButton('2', value=2.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_020)
        self.azantelev_window_area.endRow()
        self.azantelev_window_area.newHalfButtonRow(5)
        self.button_select_azantalev_025 = InvertingButton('2.5', value=2.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_025)
        self.button_select_azantalev_030 = InvertingButton('3', value=3.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_030)
        self.button_select_azantalev_035 = InvertingButton('3.5', value=3.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_035)
        self.button_select_azantalev_040 = InvertingButton('4', value=4.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_040)
        self.button_select_azantalev_045 = InvertingButton('4.5', value=4.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_045)
        self.azantelev_window_area.endRow()
        self.azantelev_window_area.newHalfButtonRow(5)
        self.button_select_azantalev_050 = InvertingButton('5', value=5.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_050)
        self.button_select_azantalev_055 = InvertingButton('5.5', value=5.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_055)
        self.button_select_azantalev_060 = InvertingButton('6', value=6.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_060)
        self.button_select_azantalev_065 = InvertingButton('6.5', value=6.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_065)
        self.button_select_azantalev_070 = InvertingButton('7', value=7.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_070)
        self.azantelev_window_area.endRow()
        self.azantelev_window_area.newHalfButtonRow(5)
        self.button_select_azantalev_075 = InvertingButton('7.5', value=7.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_075)
        self.button_select_azantalev_080 = InvertingButton('8', value=8.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_080)
        self.button_select_azantalev_085 = InvertingButton('8.5', value=8.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_085)
        self.button_select_azantalev_090 = InvertingButton('9', value=9.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_090)
        self.button_select_azantalev_095 = InvertingButton('9.5', value=9.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_095)
        self.azantelev_window_area.endRow()
        self.azantelev_window_area.newHalfButtonRow(5)
        self.button_select_azantalev_100 = InvertingButton('10', value=10.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_100)
        self.button_select_azantalev_105 = InvertingButton('10.5', value=10.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_105)
        self.button_select_azantalev_110 = InvertingButton('11', value=11.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_110)
        self.button_select_azantalev_115 = InvertingButton('11.5', value=11.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_115)
        self.button_select_azantalev_120 = InvertingButton('12', value=12.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_120)
        self.azantelev_window_area.endRow()
        self.azantelev_window_area.newHalfButtonRow(5)
        self.button_select_azantalev_125 = InvertingButton('12.5', value=12.5, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_125)
        self.button_select_azantalev_130 = InvertingButton('13', value=13.0, exclusivegroup=self.setazantelevexclusivegrouplist)
        self.azantelev_window_area.registerNextButton(self.button_select_azantalev_130)
        self.azantelev_window_area.skipNextButton()
        self.azantelev_window_area.skipNextButton()
        self.azantelev_window_area.skipNextButton()
        self.azantelev_window_area.endRow()
        self.azantelev_window_area.fixWindow()
        self.azantelev_window_topborder = WindowTopBorder('Az Ant Elevation')
        self.scene.addItem(self.azantelev_window_topborder)
        self.scene.registerWindowTopBorder(self.azantelev_window_topborder)
        self.azantelev_window_area.attachTo(self.azantelev_window_topborder)
        return self.azantelev_window_topborder



    def createSTCWindow(self):
        self.stc_window_area = WindowArea()
        self.scene.addItem(self.stc_window_area)
        self.setstcexclusivegrouplist = []
        self.stc_window_area.newFullButtonRow(4)
        self.button_select_stc_1 = InvertingButton('1\n12 dB', value=1, exclusivegroup=self.setstcexclusivegrouplist)
        self.stc_window_area.registerNextButton(self.button_select_stc_1)
        self.button_select_stc_2 = InvertingButton('2\n11 dB', value=2, exclusivegroup=self.setstcexclusivegrouplist)
        self.stc_window_area.registerNextButton(self.button_select_stc_2)
        self.button_select_stc_3 = InvertingButton('3\n10 dB', value=3, exclusivegroup=self.setstcexclusivegrouplist)
        self.stc_window_area.registerNextButton(self.button_select_stc_3)
        self.button_select_stc_4 = InvertingButton('4\n9 dB', value=4, exclusivegroup=self.setstcexclusivegrouplist)
        self.stc_window_area.registerNextButton(self.button_select_stc_4)
        self.stc_window_area.endRow()
        self.stc_window_area.newFullButtonRow(4)
        self.button_select_stc_5 = InvertingButton('5\n8 dB', value=5, exclusivegroup=self.setstcexclusivegrouplist)
        self.stc_window_area.registerNextButton(self.button_select_stc_5)
        self.button_select_stc_6 = InvertingButton('6\n7 dB', value=6, exclusivegroup=self.setstcexclusivegrouplist)
        self.stc_window_area.registerNextButton(self.button_select_stc_6)
        self.button_select_stc_7 = InvertingButton('7\n6 dB', value=7, exclusivegroup=self.setstcexclusivegrouplist)
        self.stc_window_area.registerNextButton(self.button_select_stc_7)
        self.button_select_stc_8 = InvertingButton('8\n5 dB', value=8, exclusivegroup=self.setstcexclusivegrouplist)
        self.stc_window_area.registerNextButton(self.button_select_stc_8)
        self.stc_window_area.endRow()
        self.stc_window_area.fixWindow()
        self.stc_window_topborder = WindowTopBorder('STC Slope (dB/Octave)')
        self.scene.addItem(self.stc_window_topborder)
        self.scene.registerWindowTopBorder(self.stc_window_topborder)
        self.stc_window_area.attachTo(self.stc_window_topborder)
        return self.stc_window_topborder



    def createSetNHistWindow(self):
        self.nhist_window_area = WindowArea()
        self.scene.addItem(self.nhist_window_area)
        self.setnhistexclusivegrouplist = []
        self.nhist_window_area.newHalfButtonRow(5)
        self.button_select_nhist_1 = InvertingButton('1', value=1, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_1)
        self.button_select_nhist_2 = InvertingButton('2', value=2, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_2)
        self.button_select_nhist_3 = InvertingButton('3', value=3, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_3)
        self.button_select_nhist_4 = InvertingButton('4', value=4, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_4)
        self.button_select_nhist_5 = InvertingButton('5', value=5, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_5)
        self.nhist_window_area.endRow()
        self.nhist_window_area.newHalfButtonRow(5)
        self.button_select_nhist_6 = InvertingButton('6', value=6, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_6)
        self.button_select_nhist_7 = InvertingButton('7', value=7, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_7)
        self.button_select_nhist_8 = InvertingButton('8', value=8, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_8)
        self.button_select_nhist_9 = InvertingButton('9', value=9, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_9)
        self.button_select_nhist_10 = InvertingButton('10', value=10, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_10)
        self.nhist_window_area.endRow()
        self.nhist_window_area.newHalfButtonRow(5)
        self.button_select_nhist_11 = InvertingButton('11', value=11, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_11)
        self.button_select_nhist_12 = InvertingButton('12', value=12, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_12)
        self.button_select_nhist_13 = InvertingButton('13', value=13, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_13)
        self.button_select_nhist_14 = InvertingButton('14', value=14, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_14)
        self.button_select_nhist_15 = InvertingButton('15', value=15, exclusivegroup=self.setnhistexclusivegrouplist)
        self.nhist_window_area.registerNextButton(self.button_select_nhist_15)
        self.nhist_window_area.endRow()
        self.nhist_window_area.fixWindow()
        self.nhist_window_topborder = WindowTopBorder('Select Histories')
        self.scene.addItem(self.nhist_window_topborder)
        self.scene.registerWindowTopBorder(self.nhist_window_topborder)
        self.nhist_window_area.attachTo(self.nhist_window_topborder)
        return self.nhist_window_topborder



    def createElScaleWindow(self):
        self.elscale_window_area = WindowArea()
        self.scene.addItem(self.elscale_window_area)
        self.elscaleexclusivegrouplist = []
        self.elscale_window_area.newHalfButtonRow(2)
        self.button_select_elscale_1000 = InvertingButton('1000', value=1000, exclusivegroup=self.elscaleexclusivegrouplist)
        self.elscale_window_area.registerNextButton(self.button_select_elscale_1000)
        self.button_select_elscale_2000 = InvertingButton('2000', value=2000, exclusivegroup=self.elscaleexclusivegrouplist)
        self.elscale_window_area.registerNextButton(self.button_select_elscale_2000)
        self.elscale_window_area.endRow()
        self.elscale_window_area.newHalfButtonRow(2)
        self.button_select_elscale_4000 = InvertingButton('4000', value=4000, exclusivegroup=self.elscaleexclusivegrouplist)
        self.elscale_window_area.registerNextButton(self.button_select_elscale_4000)
        self.button_select_elscale_8000 = InvertingButton('8000', value=8000, exclusivegroup=self.elscaleexclusivegrouplist)
        self.elscale_window_area.registerNextButton(self.button_select_elscale_8000)
        self.elscale_window_area.endRow()
        self.elscale_window_area.newHalfButtonRow(2)
        self.button_select_elscale_12000 = InvertingButton('12000', value=12000, exclusivegroup=self.elscaleexclusivegrouplist)
        self.elscale_window_area.registerNextButton(self.button_select_elscale_12000)
        self.button_select_elscale_16000 = InvertingButton('16000', value=16000, exclusivegroup=self.elscaleexclusivegrouplist)
        self.elscale_window_area.registerNextButton(self.button_select_elscale_16000)
        self.elscale_window_area.endRow()
        self.elscale_window_area.newHalfButtonRow(2)
        self.button_select_elscale_32000 = InvertingButton('32000', value=32000, exclusivegroup=self.elscaleexclusivegrouplist)
        self.elscale_window_area.registerNextButton(self.button_select_elscale_32000)
        self.button_select_elscale_64000 = InvertingButton('64000', value=64000, exclusivegroup=self.elscaleexclusivegrouplist)
        self.elscale_window_area.registerNextButton(self.button_select_elscale_64000)
        self.elscale_window_area.endRow()
        self.elscale_window_area.fixWindow()
        self.elscale_window_topborder = WindowTopBorder('Elevation Scale')
        self.scene.addItem(self.elscale_window_topborder)
        self.scene.registerWindowTopBorder(self.elscale_window_topborder)
        self.elscale_window_area.attachTo(self.elscale_window_topborder)
        return self.elscale_window_topborder



    def createAzScaleWindow(self):
        self.azscale_window_area = WindowArea()
        self.scene.addItem(self.azscale_window_area)
        self.azscaleexclusivegrouplist = []
        self.azscale_window_area.newHalfButtonRow(2)
        self.button_select_azscale_2000 = InvertingButton('+/-2000', value=2000, exclusivegroup=self.azscaleexclusivegrouplist)
        self.azscale_window_area.registerNextButton(self.button_select_azscale_2000)
        self.button_select_azscale_4000 = InvertingButton('+/-4000', value=4000, exclusivegroup=self.azscaleexclusivegrouplist)
        self.azscale_window_area.registerNextButton(self.button_select_azscale_4000)
        self.azscale_window_area.endRow()
        self.azscale_window_area.newHalfButtonRow(2)
        self.button_select_azscale_8000 = InvertingButton('+/-8000', value=8000, exclusivegroup=self.azscaleexclusivegrouplist)
        self.azscale_window_area.registerNextButton(self.button_select_azscale_8000)
        self.button_select_azscale_16000 = InvertingButton('+/-16000', value=16000, exclusivegroup=self.azscaleexclusivegrouplist)
        self.azscale_window_area.registerNextButton(self.button_select_azscale_16000)
        self.azscale_window_area.endRow()
        self.azscale_window_area.newHalfButtonRow(2)
        self.button_select_azscale_24000 = InvertingButton('+/-24000', value=24000, exclusivegroup=self.azscaleexclusivegrouplist)
        self.azscale_window_area.registerNextButton(self.button_select_azscale_24000)
        self.button_select_azscale_32000 = InvertingButton('+/-32000', value=32000, exclusivegroup=self.azscaleexclusivegrouplist)
        self.azscale_window_area.registerNextButton(self.button_select_azscale_32000)
        self.azscale_window_area.endRow()
        self.azscale_window_area.fixWindow()
        self.azscale_window_topborder = WindowTopBorder('Azimuth Scale')
        self.scene.addItem(self.azscale_window_topborder)
        self.scene.registerWindowTopBorder(self.azscale_window_topborder)
        self.azscale_window_area.attachTo(self.azscale_window_topborder)
        return self.azscale_window_topborder



    def createACWindow(self):
        self.ac_window_area = WindowArea()
        self.scene.addItem(self.ac_window_area)
        self.ac_window_area.newFullButtonRow(3)
        self.button_select_ac_small = FlashingButton('Small', value='S')
        self.ac_window_area.registerNextButton(self.button_select_ac_small)
        self.button_select_ac_medium = FlashingButton('Medium', value='M')
        self.ac_window_area.registerNextButton(self.button_select_ac_medium)
        self.button_select_ac_large = FlashingButton('Large', value='L')
        self.ac_window_area.registerNextButton(self.button_select_ac_large)
        self.ac_window_area.endRow()
        self.ac_window_area.fixWindow()
        self.ac_window_topborder = WindowTopBorder('Aircraft Size')
        self.scene.addItem(self.ac_window_topborder)
        self.scene.registerWindowTopBorder(self.ac_window_topborder)
        self.ac_window_area.attachTo(self.ac_window_topborder)
        return self.ac_window_topborder



    def createDisplayControlWindow(self):
        self.displaycontrol_window_area = WindowArea()
        self.scene.addItem(self.displaycontrol_window_area)
        self.displaycontrol_window_area.newFullButtonRow(4)
        self.button_wx = InvertingButton('Wx')
        self.displaycontrol_window_area.registerNextButton(self.button_wx)
        self.button_obs = InvertingButton('Obs')
        self.displaycontrol_window_area.registerNextButton(self.button_obs)
        self.button_map = InvertingButton('Map')
        self.displaycontrol_window_area.registerNextButton(self.button_map)
        self.button_whi = InvertingButton('WHI')
        self.displaycontrol_window_area.registerNextButton(self.button_whi)
        self.displaycontrol_window_area.endRow()
        self.displaycontrol_window_area.newFullButtonRow(4)
        self.button_hist = InvertingButton('Hist')
        self.displaycontrol_window_area.registerNextButton(self.button_hist)
        self.button_radarcover = InvertingButton('Radar\nCover')
        self.displaycontrol_window_area.registerNextButton(self.button_radarcover)
        self.button_syn_video = InvertingButton('Syn\nVideo')
        self.displaycontrol_window_area.registerNextButton(self.button_syn_video)
        self.displaycontrol_window_area.skipNextButton()
        self.displaycontrol_window_area.endRow()
        self.displaycontrol_window_area.newFullButtonRow(4)
        self.button_dbfld = ExpandingButton('Sel\nDBFld', self.seldbfld_window)
        self.displaycontrol_window_area.registerNextButton(self.button_dbfld)
        self.button_lead_dir = ExpandingButton('Lead\nDir', self.leaddir_window)
        self.displaycontrol_window_area.registerNextButton(self.button_lead_dir)
        self.button_color_legnd = Button('Color\nLegnd')
        self.displaycontrol_window_area.registerNextButton(self.button_color_legnd)
        self.displaycontrol_window_area.skipNextButton()
        self.displaycontrol_window_area.endRow()
        self.displaycontrol_window_area.newFullButtonRow(4)
        self.button_azscale = ExpandingButton('Az\nScale', self.azscale_window)
        self.displaycontrol_window_area.registerNextButton(self.button_azscale)
        self.button_elscale = ExpandingButton('El\nScale', self.elscale_window)
        self.displaycontrol_window_area.registerNextButton(self.button_elscale)
        self.button_az_offset = InvertingButton('Az\nOffset')
        self.displaycontrol_window_area.registerNextButton(self.button_az_offset)
        self.displaycontrol_window_area.skipNextButton()
        self.displaycontrol_window_area.endRow()
        self.displaycontrol_window_area.newFullButtonRow(4)
        self.button_clear_hist = FlashingButton('Clear\nHist')
        self.displaycontrol_window_area.registerNextButton(self.button_clear_hist)
        self.button_nhist = ExpandingButton('Set #\nHist', self.nhist_window)
        self.displaycontrol_window_area.registerNextButton(self.button_nhist)
        self.displaycontrol_window_area.skipNextButton()
        self.button_shutdown = Button('Shut\nDown')
        self.displaycontrol_window_area.registerNextButton(self.button_shutdown)
        self.displaycontrol_window_area.endRow()
        self.displaycontrol_window_area.fixWindow()
        self.displaycontrol_window_topborder = WindowTopBorder('Display Controls')
        self.scene.addItem(self.displaycontrol_window_topborder)
        self.scene.registerWindowTopBorder(self.displaycontrol_window_topborder)
        self.displaycontrol_window_area.attachTo(self.displaycontrol_window_topborder)
        return self.displaycontrol_window_topborder



    def createRadarControlWindow(self):
        self.radarcontrol_window_area = WindowArea()
        self.scene.addItem(self.radarcontrol_window_area)
        self.radarcontrol_window_area.newFullButtonRow(4)
        self.button_ant_drive = InvertingButton('Ant\nDrive')
        self.radarcontrol_window_area.registerNextButton(self.button_ant_drive)
        self.button_radiate = InvertingButton('Rad-\niate')
        self.radarcontrol_window_area.registerNextButton(self.button_radiate)
        self.button_rain_mode = InvertingButton('Rain\nMode')
        self.radarcontrol_window_area.registerNextButton(self.button_rain_mode)
        self.button_stc = ExpandingButton('STC', self.stc_window)
        self.radarcontrol_window_area.registerNextButton(self.button_stc)
        self.radarcontrol_window_area.endRow()
        self.radarcontrol_window_area.newFullButtonRow(4)
        self.button_maint_mode = InvertingButton('Maint\nMode')
        self.radarcontrol_window_area.registerNextButton(self.button_maint_mode)
        self.radarcontrol_window_area.skipNextButton()
        self.button_altim = Button('Altim')
        self.radarcontrol_window_area.registerNextButton(self.button_altim)
        self.button_wind = Button('Wind')
        self.radarcontrol_window_area.registerNextButton(self.button_wind)
        self.radarcontrol_window_area.endRow()
        self.radarcontrol_window_area.newFullButtonRow(4)
        self.button_azantelev = ExpandingButton('AzAnt\nElev', self.azantelev_window)
        self.radarcontrol_window_area.registerNextButton(self.button_azantelev)
        self.button_elantazim = ExpandingButton('ElAnt\nAzim', self.elantazim_window)
        self.radarcontrol_window_area.registerNextButton(self.button_elantazim)
        self.button_glideslope = ExpandingButton('Glide\nSlope', self.glideslope_window)
        self.radarcontrol_window_area.registerNextButton(self.button_glideslope)
        self.button_decsn_hgt = ExpandingButton('Decsn\nHgt', self.decsnheight_window)
        self.radarcontrol_window_area.registerNextButton(self.button_decsn_hgt)
        self.radarcontrol_window_area.endRow()
        self.radarcontrol_window_area.fixWindow()
        self.radarcontrol_window_topborder = WindowTopBorder('Radar Controls')
        self.scene.addItem(self.radarcontrol_window_topborder)
        self.scene.registerWindowTopBorder(self.radarcontrol_window_topborder)
        self.radarcontrol_window_area.attachTo(self.radarcontrol_window_topborder)
        return self.radarcontrol_window_topborder



    def createRadarModeWindow(self):
        self.radarmode_window_area = WindowArea()
        self.scene.addItem(self.radarmode_window_area)
        self.radarmode_window_area.newHalfButtonRow(3)
        self.radarmodeexclusivegrouplist = []
        self.button_par = InvertingButton('PAR', value=1, exclusivegroup=self.radarmodeexclusivegrouplist)
        self.radarmode_window_area.registerNextButton(self.button_par)

        self.button_asr = Button('ASR', value=2)                        # This is just to make choosing ASR and Combined impossible
        self.radarmode_window_area.registerNextButton(self.button_asr)
        self.button_comb = Button('Comb', value=3)
        self.radarmode_window_area.registerNextButton(self.button_comb)

        #self.button_asr = InvertingButton('ASR', value=2, exclusivegroup=self.radarmodeexclusivegrouplist)
        #self.radarmode_window_area.registerNextButton(self.button_asr)
        #self.button_comb = InvertingButton('Comb', value=3, exclusivegroup=self.radarmodeexclusivegrouplist)
        #self.radarmode_window_area.registerNextButton(self.button_comb)

        self.radarmode_window_area.endRow()
        self.radarmode_window_area.fixWindow()
        self.radarmode_window_topborder = WindowTopBorder('Radar Mode')
        self.scene.addItem(self.radarmode_window_topborder)
        self.scene.registerWindowTopBorder(self.radarmode_window_topborder)
        self.radarmode_window_area.attachTo(self.radarmode_window_topborder)
        return self.radarmode_window_topborder




    # This pairwise thinking is obsolete. Change!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def createRunwaySelectWindow(self, rwy_name={}):
        # Observe that runways must occur in pairs: 1 and 2, 1 and 2 and 3 and 4 or all six. 
        self.runwayselect_window_area = WindowArea()
        self.scene.addItem(self.runwayselect_window_area)
        self.runwayselect_window_area.newHalfButtonRow(3)
        self.rwyexclusivegrouplist = []
        
        if 1 in rwy_name.keys():
            self.button_select_runway_1 = InvertingButton(rwy_name[1], value=1, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_1)
        else:
            self.button_select_runway_1 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_1)

        if 2 in rwy_name.keys():
            self.button_select_runway_2 = InvertingButton(rwy_name[2], value=2, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_2)
        else:
            self.button_select_runway_2 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_2)


        if 3 in rwy_name.keys():
            self.button_select_runway_3 = InvertingButton(rwy_name[3], value=3, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_3)
        else:
            self.button_select_runway_3 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_3)

        self.runwayselect_window_area.endRow()
        self.runwayselect_window_area.newHalfButtonRow(3)

        if 4 in rwy_name.keys():
            self.button_select_runway_4 = InvertingButton(rwy_name[4], value=4, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_4)
        else:
            self.button_select_runway_4 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_4)


        if 5 in rwy_name.keys():
            self.button_select_runway_5 = InvertingButton(rwy_name[5], value=5, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_5)
        else:
            self.button_select_runway_5 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_5)

        if 6 in rwy_name.keys():
            self.button_select_runway_6 = InvertingButton(rwy_name[6], value=6, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_6)
        else:
            self.button_select_runway_6 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_6)



        """
        if rwy1 and rwy2:
            self.button_select_runway_1 = InvertingButton(rwy1, value=0, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_1)
            self.button_select_runway_2 = InvertingButton(rwy2, value=1, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_2)
        else:
            self.button_select_runway_1 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_1)
            self.button_select_runway_2 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_2)
        if rwy3 and rwy4:
            self.button_select_runway_3 = InvertingButton(rwy3, value=2, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_3)
            self.runwayselect_window_area.endRow()
            self.runwayselect_window_area.newHalfButtonRow(3)
            self.button_select_runway_4 = InvertingButton(rwy4, value=3, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_4)
        else:
            self.button_select_runway_3 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_3)
            self.runwayselect_window_area.endRow()
            self.runwayselect_window_area.newHalfButtonRow(3)
            self.button_select_runway_4 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_4)
        if rwy5 and rwy6:
            self.button_select_runway_5 = InvertingButton(rwy5, value=4, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_5)
            self.button_select_runway_6 = InvertingButton(rwy6, value=5, exclusivegroup=self.rwyexclusivegrouplist)
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_6)
        else:
            self.button_select_runway_5 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_5)
            self.button_select_runway_6 = Button('')
            self.runwayselect_window_area.registerNextButton(self.button_select_runway_6)
        
        """

        self.runwayselect_window_area.endRow()
        self.runwayselect_window_area.fixWindow()
        self.runwayselect_window_topborder = WindowTopBorder('Runway Select')
        self.scene.addItem(self.runwayselect_window_topborder)
        self.scene.registerWindowTopBorder(self.runwayselect_window_topborder)
        self.runwayselect_window_area.attachTo(self.runwayselect_window_topborder)
        return self.runwayselect_window_topborder



    def createMainWindow(self):
        self.main_window_area = WindowArea()
        self.scene.addItem(self.main_window_area)
        self.main_window_area.newTextRow('Range Scale (nmi)')
        self.main_window_area.endRow()
        self.main_window_area.newHalfButtonRow(4)
        self.button_select_rangescale_down = Button('<---')
        self.main_window_area.registerNextButton(self.button_select_rangescale_down)
        self.button_select_rangescale_up = Button('--->')
        self.main_window_area.registerNextButton(self.button_select_rangescale_up)
        self.scaleexclusivegrouplist = []
        self.button_select_rangescale_1 = InvertingButton('1', value=1, exclusivegroup=self.scaleexclusivegrouplist)
        self.main_window_area.registerNextButton(self.button_select_rangescale_1)
        self.button_select_rangescale_3 = InvertingButton('3', value=3, exclusivegroup=self.scaleexclusivegrouplist)
        self.main_window_area.registerNextButton(self.button_select_rangescale_3)
        self.main_window_area.endRow()
        self.main_window_area.newHalfButtonRow(4)
        self.button_select_rangescale_5 = InvertingButton('5', value=5, exclusivegroup=self.scaleexclusivegrouplist)
        self.main_window_area.registerNextButton(self.button_select_rangescale_5)
        self.button_select_rangescale_10 = InvertingButton('10', value=10, exclusivegroup=self.scaleexclusivegrouplist)
        self.main_window_area.registerNextButton(self.button_select_rangescale_10)
        self.button_select_rangescale_15 = InvertingButton('15', value=15, exclusivegroup=self.scaleexclusivegrouplist)
        self.main_window_area.registerNextButton(self.button_select_rangescale_15)
        self.button_select_rangescale_20 = InvertingButton('20', value=20, exclusivegroup=self.scaleexclusivegrouplist)
        self.main_window_area.registerNextButton(self.button_select_rangescale_20)
        self.main_window_area.endRow()
        self.main_window_area.newWhiteLineSeparator()
        self.main_window_area.endRow()
        self.main_window_area.newTextRow('Main Controls                       ')
        self.main_window_area.endRow()
        self.main_window_area.newFullButtonRow(3)
        self.button_acid_entry = ExpandingButton('ACID\nEntry', self.acid_entry_window)
        self.main_window_area.registerNextButton(self.button_acid_entry)
        self.button_ac_size = ExpandingButton('AC\nSize', self.ac_window)
        self.main_window_area.registerNextButton(self.button_ac_size)
        self.button_whi_tgt_exchange = FlashingButton('WHI Tgt\nExchange')
        self.main_window_area.registerNextButton(self.button_whi_tgt_exchange)
        self.main_window_area.endRow()
        self.main_window_area.newFullButtonRow(3)
        self.button_displaycontrol = ExpandingButton('Display\nControl', self.displaycontrol_window)
        self.main_window_area.registerNextButton(self.button_displaycontrol)
        self.button_radarcontrol = ExpandingButton('Radar\nControl', self.radarcontrol_window)
        self.main_window_area.registerNextButton(self.button_radarcontrol)
        self.button_status = ExpandingButton('Status', self.status_window)
        self.main_window_area.registerNextButton(self.button_status)
        self.main_window_area.endRow()
        self.main_window_area.newFullButtonRow(3)
        self.main_window_area.skipNextButton()
        self.main_window_area.skipNextButton()
        self.button_radar_mode = ExpandingButton('Radar\nMode', self.radarmode_window)
        self.main_window_area.registerNextButton(self.button_radar_mode)
        self.main_window_area.endRow()
        self.main_window_area.newFullButtonRow(3)
        self.button_clear_alerts = FlashingButton('Clear\nAlerts')
        self.main_window_area.registerNextButton(self.button_clear_alerts)
        self.button_ppi_mode = FlashingButton('PPI\nMode')
        self.main_window_area.registerNextButton(self.button_ppi_mode)
        self.button_runway_select = ExpandingButton('Runway\nSelect', self.runwayselect_window)
        self.main_window_area.registerNextButton(self.button_runway_select)
        self.main_window_area.endRow()
        self.main_window_area.fixWindow()
        self.main_window_area.putWindowAtBottom()
        return self.main_window_area



    def close(self):
        self.quit.emit()

    def closeEvent(self, event):
        event.ignore()
        self.quit.emit()
