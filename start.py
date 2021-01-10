
"""
Copyright (C) 2020 Oscar Franzén <oscarfranzen@protonmail.com>

This file is part of Mil i-ATC Eavesdropper.

Mil i-ATC Eavesdropper is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Mil i-ATC Eavesdropper is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Mil i-ATC Eavesdropper.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import shutil
from mycommonfunctions import path as mypath
import mycommonfunctions.basicconfig as myconfig

def initFileStructure():
    # DIRECTORIES
    application_directory = mypath.current_working_directory()
    user_home_directory = mypath.user_home_directory()

    # Try to find the Documents directory
    user_documents_directory = None

    if os.path.exists(os.path.join(user_home_directory, 'Documents')):
        user_documents_directory = os.path.join(user_home_directory, 'Documents')
    elif os.path.exists(os.path.join(user_home_directory, 'Dokument')):
        user_documents_directory = os.path.join(user_home_directory, 'Dokument')

    if user_documents_directory != None:
        local_data_root_directory = os.path.join(user_documents_directory, 'GCA Simulator Data')
    else:
        local_data_root_directory = os.path.join(user_home_directory, 'GCA Simulator Data')

    # self.local_data_config_directory = self.local_data_root_directory
    # self.local_data_log_directory = os.path.join(self.local_data_root_directory, 'logs')
    local_data_sys_directory = os.path.join(local_data_root_directory, 'sys')
    local_data_recordings_directory = os.path.join(local_data_root_directory, 'recordings')
    local_data_airports_directory = os.path.join(local_data_root_directory, 'airports')
    local_data_videos_directory = os.path.join(local_data_root_directory, 'videos')
    local_data_plugins_directory = os.path.join(local_data_root_directory, 'plugins')
    local_data_dcs_plugin_directory = os.path.join(local_data_plugins_directory, 'dcs')
    local_data_xplane_plugin_directory = os.path.join(local_data_plugins_directory, 'xpl')

    default_resources_directory = os.path.join(application_directory, 'resources')
    default_misc_directory = os.path.join(default_resources_directory, 'misc')
    default_recordings_directory = os.path.join(default_resources_directory, 'recordings')
    default_airports_directory = os.path.join(default_resources_directory, 'airports')
    default_videos_directory = os.path.join(default_resources_directory, 'videos')
    default_plugins_directory = os.path.join(default_resources_directory, 'plugins')
    default_dcs_plugin_directory = os.path.join(default_plugins_directory, 'dcs')
    default_xplane_plugin_directory = os.path.join(default_plugins_directory, 'xpl')
    default_sounds_directory = os.path.join(default_resources_directory, 'sounds')
    default_images_directory = os.path.join(default_resources_directory, 'images')
    default_config_directory = os.path.join(default_resources_directory, 'config')

    # Initialize directories and stuff
    if not os.path.exists(local_data_root_directory):
        os.mkdir(local_data_root_directory)

    # if not os.path.exists(self.local_data_log_directory):
    #     os.mkdir(self.local_data_log_directory)

    # sys
    if not os.path.exists(local_data_sys_directory):
        os.mkdir(local_data_sys_directory)
    shutil.copyfile(os.path.join(default_misc_directory, 'sysreadme.txt'), os.path.join(local_data_sys_directory, 'readme.txt'))

    # recordings
    if not os.path.exists(local_data_recordings_directory):
        os.mkdir(local_data_recordings_directory)
    shutil.copyfile(os.path.join(default_recordings_directory, 'demo.rcd'), os.path.join(local_data_recordings_directory, 'demo.rcd'))
    shutil.copyfile(os.path.join(default_recordings_directory, 'readme.txt'), os.path.join(local_data_recordings_directory, 'readme.txt'))

    # airports
    if not os.path.exists(local_data_airports_directory):
        os.mkdir(local_data_airports_directory)
    shutil.copyfile(os.path.join(default_airports_directory, 'dcs_batumi.apt'), os.path.join(local_data_airports_directory, 'dcs_batumi.apt'))
    shutil.copyfile(os.path.join(default_airports_directory, 'xpl_batumi.apt'), os.path.join(local_data_airports_directory, 'xpl_batumi.apt'))
    shutil.copyfile(os.path.join(default_airports_directory, 'readme.txt'), os.path.join(local_data_airports_directory, 'readme.txt'))

    # videos
    if not os.path.exists(local_data_videos_directory):
        os.mkdir(local_data_videos_directory)
        shutil.copyfile(os.path.join(default_videos_directory, 'demo.mp4'), os.path.join(local_data_videos_directory, 'demo.mp4'))  # Too large?
    shutil.copyfile(os.path.join(default_videos_directory, 'readme.txt'), os.path.join(local_data_videos_directory, 'readme.txt'))

    # plugins
    if not os.path.exists(local_data_plugins_directory):
        os.mkdir(local_data_plugins_directory)

    if os.path.exists(local_data_dcs_plugin_directory):
        shutil.rmtree(local_data_dcs_plugin_directory)
    shutil.copytree(default_dcs_plugin_directory, local_data_dcs_plugin_directory)
    if os.path.exists(local_data_xplane_plugin_directory):
        shutil.rmtree(local_data_xplane_plugin_directory)
    shutil.copytree(default_xplane_plugin_directory, local_data_xplane_plugin_directory)
    shutil.copyfile(os.path.join(default_plugins_directory, 'readme.txt'), os.path.join(local_data_plugins_directory, 'readme.txt'))

    # config
    config_file = os.path.join(local_data_root_directory, 'config.txt')
    if not os.path.exists(config_file):
        shutil.copyfile(os.path.join(default_config_directory, 'defaultconfig.txt'), os.path.join(local_data_root_directory, 'config.txt'))

    ip_file = os.path.join(local_data_sys_directory, 'ip.txt')

    icon_file = os.path.join(default_images_directory, 'icon.ico')

    beep_file = os.path.join(default_sounds_directory, 'beep.wav')

    #copying_file = os.path.join(application_directory, 'COPYING.rtf')

    globalvars['version'] = 'v0.92b'
    globalvars['local_data_root_directory'] = local_data_root_directory
    globalvars['local_data_airports_directory'] = local_data_airports_directory
    globalvars['local_data_recordings_directory'] = local_data_recordings_directory
    globalvars['ip_file'] = ip_file
    globalvars['config_file'] = config_file
    globalvars['icon_file'] = icon_file
    globalvars['beep_file'] = beep_file

myconfig.initGlobals()
globalvars = myconfig.getGlobals()
globalvars['rds_install'] = False

initFileStructure()

myconfig.initConfig('config', globalvars['config_file'])

from source.main import main

if __name__ == '__main__':
    main()

# I think this file stuff should happen in main instead.....?