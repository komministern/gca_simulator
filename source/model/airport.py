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

class Airport(object):

    def __init__(self, filename):
        super(Airport, self).__init__()

        self.filename = filename

        self.runways = {}

        self.dostuff(filename)

    def dostuff(self, filename):

        with open(filename) as f:
            s = f.read()
        f.close()

        entries_with_float_as_value = ['thr_lon', 'thr_lat', 'thr_el', 'eor_lon', 'eor_lat', 'eor_el', 'td', 'gs', 'true', 'dcs_thr_x', 'dcs_thr_y', 'dcs_thr_z', 'dcs_eor_x', 'dcs_eor_y', 'dcs_eor_z']
        
        runway_number = None

        lines = s.splitlines()

        for line in lines:

            # print(line)

            strings = line.split()
            
            if len(strings) > 0:

                if not strings[0][0] == '#':

                    assert(len(strings) > 1), 'Malformed line "%s" in %s' % (line, filename)

                    if len(strings) > 2:
                        assert(strings[2][0] == '#'), 'Malformed line "%s" in %s' % (line, filename)

                    entry = strings[0]
                    value = strings[1]

                    if entry == 'iata':
                        self.iata = value

                    elif entry == 'icao':
                        self.icao = value

                    elif entry[0:3] == 'rwy':
                        runway_number = int(entry[3:4])
                        assert(runway_number >= 1 and runway_number <= 6) , 'Erroneous runway number in line "%s" in %s' % (line, filename)
                        self.runways[runway_number] = {}
                        self.runways[runway_number]['name'] = value

                    elif entry in entries_with_float_as_value:
                        assert(runway_number != None), 'Runway must be specified before "%s" in %s' % (line, filename)
                        self.runways[runway_number][entry] = float(value)

                    else:
                        raise Exception('Erroneous entry "%s" in %s' % (entry, filename))
