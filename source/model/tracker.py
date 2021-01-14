
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

import os
import sys
import time
import random

import numpy as np
from PySide2 import QtCore, QtWidgets, QtGui, QtNetwork

"""
A target consists of hits in either the az or the el channel (or both) which are magically deemed
to belong to the same target. The 'tracking' is already done, so to speak. If there are hits in both 
the az and the el channel, nothing special needs to be done. But if there is a hit in only one of the
channels, the coordinate for this channel needs to be extrapolated. This is done with the two previous
targets, using the coordinate for the channel (either the real coordinate or extrapolated coordinates if 
that is the case).
So, in the normal case, the el_coordinate and the az_coordinate are just the same. It is only in the
case of false hits that these coordinates gets replaced with extrapolated coordinates for that channel.
A extrapolated target (in either the az or el channel), is drawn as a completely transparent plot. Visible
plots are only from real targets (that is when hit==True).
"""


class Target(QtCore.QObject):

    

    def __init__(self, time_stamp, coordinate, az_hit, el_hit):
        super(Target, self).__init__()
        
        self.time_stamp = time_stamp
        # self.coordinate = coordinate
        self.az_hit = az_hit
        self.el_hit = el_hit
        if self.az_hit:
            self.az_coordinate = coordinate
        else:
            self.az_coordinate = None
        if self.el_hit:
            self.el_coordinate = coordinate
        else:
            self.el_coordinate = None
        # self.extrapolated_coordinate = None
        self.velocity = None
        self.filtered_velocity = None
        
        #@property
        def az_extrapolated(self):
            return not self.az_hit
        
        #@property
        def el_extrapolated(self):
            return not self.el_hit


        


class Track(QtCore.QObject):
    
    def __init__(self):#, time_stamp, coordinate, az_hit, el_hit):
        super(Track, self).__init__()
        self.targets = []

        self.velocity_alpha = 0.2
        self.velocity_window_size = 3
        #self.registerNewHit(time_stamp, coordinate, az_hit, el_hit)



    def qualify_for_active(self):
        if len(self.targets) < 3:
            return False
        else:
            return (self.targets[0].az_hit and self.targets[1].az_hit and self.targets[2].az_hit) and (self.targets[0].el_hit and self.targets[1].el_hit and self.targets[2].el_hit)


    def register_new_target(self, time_stamp, coordinate, az_hit, el_hit):
        target = Target(time_stamp, coordinate, az_hit, el_hit)

        if not az_hit:
            target.az_coordinate = self.extrapolate_coordinate(time_stamp, 'az')
        if not el_hit:
            target.el_coordinate = self.extrapolate_coordinate(time_stamp, 'el')

        target.velocity = self.calculate_velocity(target)

        target.filtered_velocity = self.calculate_filtered_velocity(target)

        #if not (az_hit and el_hit):
        #    target.extrapolated_coordinate = self.extrapolate(time_stamp)
        
        self.targets.insert(0, target)

        if len(self.targets) > 15:
            del self.targets[-1]

    def calculate_velocity(self, target):
        
        last_el_coordinate = self.historic_coordinate(0, 'el')
        last_az_coordinate = self.historic_coordinate(0, 'az')
        new_el_coordinate = target.el_coordinate
        new_az_coordinate = target.az_coordinate

        if not isinstance(last_az_coordinate, type(None)) and not isinstance(last_el_coordinate, type(None)) and not isinstance(new_az_coordinate, type(None)) and not isinstance(new_el_coordinate, type(None)):
        #if last_az_coordinate != None and last_el_coordinate != None and new_az_coordinate != None and new_el_coordinate != None:
            last_coordinate = (last_az_coordinate + last_el_coordinate) / 2
            new_coordinate = (new_az_coordinate + new_el_coordinate) / 2
            delta_distance = new_coordinate - last_coordinate
            delta_time = target.time_stamp - self.targets[0].time_stamp
            velocity = np.linalg.norm(delta_distance) / delta_time
            velocity *= 1.943844
        else:
            velocity = None
        return velocity


    def extrapolate_coordinate(self, latest_time_stamp, target_channel):
        
        if target_channel == 'az':
            latest_coordinate = self.historic_coordinate(0, 'az')
            next_latest_coordinate = self.historic_coordinate(1, 'az')
        else:
            latest_coordinate = self.historic_coordinate(0, 'el')
            next_latest_coordinate = self.historic_coordinate(1, 'el')

        if not isinstance(latest_coordinate, type(None)) and not isinstance(next_latest_coordinate, type(None)):

            next_latest_time_stamp = self.targets[0].time_stamp

            delta_velocity = latest_coordinate - next_latest_coordinate
            delta_time = latest_time_stamp - next_latest_time_stamp

            velocity_vector = delta_velocity / delta_time

            extrapolated_coordinate = latest_coordinate + velocity_vector * (latest_time_stamp - next_latest_time_stamp)

            return extrapolated_coordinate

        else:

            return None

    def historic_coordinate(self, n, target_type):

        if len(self.targets) > n:

            if target_type == 'az':
                coordinate = self.targets[n].az_coordinate
            else:
                coordinate = self.targets[n].el_coordinate

        else:

            coordinate = None
        
        return coordinate

    def historic_velocity(self, n):
        if len(self.targets) > n + 1:

            return self.targets[n].velocity

        else:

            return None

        #     latest_coordinate = self.historic_coordinate(n)
        #     latest_time_stamp = self.targets[n].time_stamp
        #     next_latest_coordinate = self.historic_coordinate(n + 1)
        #     next_latest_time_stamp = self.targets[n + 1].time_stamp
        #     if (not isinstance(latest_coordinate, type(None))) and (not isinstance(next_latest_coordinate, type(None))):
        #         velocity = np.linalg.norm( (latest_coordinate - next_latest_coordinate) / (latest_time_stamp - next_latest_time_stamp) )
        #     else:
        #         velocity = None
        # else:
        #     velocity = None
        # return velocity


    def mean_velocity(self, first_n, last_n):
        velocity_sum = 0.0
        velocity_counter = 0
        for i in range(first_n, last_n + 1):
            v = self.historic_velocity(i)
            if v != None:
                velocity_sum += v
                velocity_counter += 1
        if velocity_counter > 0:
            mean_velocity = velocity_sum / velocity_counter# * 1.943844  # Knots
        else:
            mean_velocity = None
        return mean_velocity

    # def estimated_velocity(self):
    #     return self.historic_velocity(0)

    def calculate_filtered_velocity(self, target):
        momentous_velocity = self.calculate_velocity(target)
        mean_velocity = self.mean_velocity(0, self.velocity_window_size)
        if momentous_velocity != None and mean_velocity != None:
            filtered_velocity = self.velocity_alpha * momentous_velocity + (1.0 - self.velocity_alpha) * mean_velocity# * 1.943844   # Knots
        else:
            filtered_velocity = None
        return filtered_velocity


class Tracker(QtCore.QObject):

    mti_lost = QtCore.Signal()
    report_tracks = QtCore.Signal(object, object, object, object, object, object)

    def __init__(self, model):
        super(Tracker, self).__init__()
        
        self.model = model

        self.active_tracks = {}
        self.passive_tracks = {}

    def reset_tracks(self):
        self.active_tracks = {}
        self.passive_tracks = {}
        # for name in tracks_which_have_become_null_and_void:
        #     #self.passive_tracks[name] = self.active_tracks[name]
        #     del self.active_tracks[name]
        #     print('deleted ' + name + ' from active tracks')

    def process_hits(self, new_time_stamp, thr_coordinate, eor_coordinate, gca_coordinate, aircraft_coordinates, aircraft_hits):
        
        for name in aircraft_coordinates:

            el_hit, az_hit = aircraft_hits[name]

            if name in self.active_tracks:
                
                self.active_tracks[name].register_new_target(new_time_stamp, aircraft_coordinates[name], az_hit, el_hit)
            
            elif name in self.passive_tracks:

                self.passive_tracks[name].register_new_target(new_time_stamp, aircraft_coordinates[name], az_hit, el_hit)
                
                if self.passive_tracks[name].qualify_for_active():
                    self.active_tracks[name] = self.passive_tracks[name]
                    del self.passive_tracks[name]
                    print('moved ' + name + ' from passive to active tracks')

            else:

                self.passive_tracks[name] = Track()
                self.passive_tracks[name].register_new_target(new_time_stamp, aircraft_coordinates[name], az_hit, el_hit)
                print('added ' + name + ' to passive tracks')

        # if 'mti' in self.active_tracks:
        #     if len(self.active_tracks['mti'].targets) > 2:
                
        #         if not (self.active_tracks['mti'].targets[0].az_hit or self.active_tracks['mti'].targets[1].az_hit or self.active_tracks['mti'].targets[2].az_hit):
        #             #print('az mti lost')
        #             self.mti_lost.emit()
        #         if not (self.active_tracks['mti'].targets[0].el_hit or self.active_tracks['mti'].targets[1].el_hit or self.active_tracks['mti'].targets[2].el_hit):
        #             #print('el mti lost')
        #             self.mti_lost.emit()

        

        tracks_which_have_become_null_and_void = []
        
        for name in self.active_tracks:
            if len(self.active_tracks[name].targets) > 2:
                if (not self.active_tracks[name].targets[0].az_hit and not self.active_tracks[name].targets[1].az_hit and not self.active_tracks[name].targets[2].az_hit) or (not self.active_tracks[name].targets[0].el_hit and not self.active_tracks[name].targets[1].el_hit and not self.active_tracks[name].targets[2].el_hit):
                #if self.active_tracks[name].targets[0].time_stamp < new_time_stamp - 2.5:
                    tracks_which_have_become_null_and_void.append(name)
        
        for name in tracks_which_have_become_null_and_void:
            #self.passive_tracks[name] = self.active_tracks[name]
            del self.active_tracks[name]
            print('deleted ' + name + ' from active tracks')
        
        # print(time.time() - self.model.time_stamp_radiate_on)

        if ('mti' not in self.active_tracks) and (time.time() - self.model.time_stamp_radiate_on) > 4.0 and self.model.radiating:
            self.mti_lost.emit()
            # This is the way to go with the mti alarm.....

        if self.model.demo_has_restarted:
            print('all active and passive tracks deleted due to demo loop')
            self.passive_tracks = {}
            self.active_tracks = {}
            self.model.demo_has_restarted = False

        #print('passive: ' + repr(self.passive_tracks))
        #print('active: ' + repr(self.active_tracks))

        self.report_tracks.emit(new_time_stamp, thr_coordinate, eor_coordinate, gca_coordinate, self.active_tracks, self.passive_tracks)
    
        # Should get some signal when a demo file resets, so that all targets are dropped.
        # Targets behind the radar should never get to send hits!!!!!
