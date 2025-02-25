# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2014 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Downloads a reservoir to the Crazyflie and verifies its checksum
"""
import logging
import time
from threading import Timer

import random
import cflib.crtp  # noqa
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


class ReservoirDownloadExample:
    """
    Downloads a reservoir to the Crazyflie and verifies its checksum
    """

    checksum = 0

    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie(rw_cache='./cache')

        # Connect some callbacks from the Crazyflie API
        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        print('Connecting to %s' % link_uri)

        # Try to connect to the Crazyflie
        self._cf.open_link(link_uri)

        # Variable used to keep main loop occupied until disconnect
        self.is_connected = True

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        print('Connected to %s' % link_uri)

        # The definition of the logconfig can be made before connecting
        self._lg_res = LogConfig(name='Reservoir', period_in_ms=100)
        self._lg_res.add_variable('reservoir.checksum', 'uint32_t')
        self._lg_res.add_variable('reservoir.data', 'uint32_t')
        self._lg_res.add_variable('reservoir.index', 'uint32_t')
        self._lg_res.add_variable('reservoir.size0', 'uint8_t')
        self._lg_res.add_variable('reservoir.conn0', 'uint16_t')

        # Adding the configuration cannot be done until a Crazyflie is
        # connected, since we need to check that the variables we
        # would like to log are in the TOC.
        try:
            self._cf.log.add_config(self._lg_res)
            # This callback will receive the data
            self._lg_res.data_received_cb.add_callback(self._res_log_data)
            # This callback will be called on errors
            self._lg_res.error_cb.add_callback(self._res_log_error)

            self._cf.reservoir.clear()

            print('Allocating reservoir with 50 neurons, '
                  '250 internal connections.')
            self._cf.reservoir.alloc_reservoir(0, 50, 250)

            print('Setting input weights\t\t', end='')
            for i in range(0, 50):
                for j in range(0, 3):
                    self._cf.reservoir.set_input_weight_bytes(
                        0, j, i, (i * j + 63))
                    self.checksum = 0xFFFFFFFF & (
                        (self.checksum ^ (i * j + 63)) + (i * j + 63))
                print('.', end='')
            print('')

            print('Setting output weights\t\t', end='')
            for i in range(0, 50):
                for j in range(0, 4):
                    self._cf.reservoir.set_output_weight_bytes(
                        0, j, i, (i * j + 17))
                    self.checksum = 0xFFFFFFFF & (
                        (self.checksum ^ (i * j + 17)) + (i * j + 17))
                print('.', end='')
            print('')

            print('Setting internal weights\t', end='')
            for i in range(0, 250):
                self._cf.reservoir.append_internal_weight_bytes(
                    0, i, 7, 3, i)
                self.checksum = 0xFFFFFFFF & (
                    (self.checksum ^ (i)) + (i))
                self.checksum = 0xFFFFFFFF & (
                    (self.checksum ^ (3)) + (3))
                self.checksum = 0xFFFFFFFF & (
                    (self.checksum ^ (7)) + (7))
                print('.', end='')
            print('')

            print('Computed checksum: ' + str(self.checksum))
            time.sleep(0.2)
            self._cf.reservoir.compute_checksum()

            # Start the logging
            self._lg_res.start()
        except KeyError as e:
            print('Could not start log configuration,'
                  '{} not found in TOC'.format(str(e)))
        except AttributeError:
            print('Could not add reservoir log config, bad configuration.')

        time.sleep(1)
        # Start a timer to disconnect in 10s
        t = Timer(0.2, self._cf.close_link)
        t.start()

    def _res_log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print('Error when logging %s: %s' % (logconf.name, msg))

    def _res_log_data(self, timestamp, data, logconf):
        """Callback froma the log API when data arrives"""
        print('[%d][%s]: %s' % (timestamp, logconf.name, data))
        if (data['reservoir.checksum'] != self.checksum):
            print('\033[91m' + 'Test failed! Checksum mismatch.' + '\x1b[0m')
        else:
            print('\033[92m' + 'Test passed! Checksums match.' + '\x1b[0m')

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the speficied address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))
        self.is_connected = False

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)
        self.is_connected = False


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    # Scan for Crazyflies and use the first one found
    print('Scanning interfaces for Crazyflies...')
    available = cflib.crtp.scan_interfaces()
    print('Crazyflies found:')
    for i in available:
        print(i[0])

    if len(available) > 0:
        le = ReservoirDownloadExample(available[0][0])
    else:
        print('No Crazyflies found. Cannot run.')

    # The Crazyflie lib doesn't contain anything to keep the application alive,
    # so this is where your application should do something. In our case we
    # are just waiting until we are disconnected.
    while le.is_connected:
        time.sleep(1)
