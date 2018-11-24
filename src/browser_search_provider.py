#!/usr/bin/env python3
# This file is a part of gnome-pass-search-provider.
#
# browser_search_provider is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# browser_search_provider is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gnome-pass-search-provider. If not, see
# <http://www.gnu.org/licenses/>.

# Copyright (C) 2018 Simone Massaro
# Author: Simone Massaro <massaro.simone.it@gmail.com>

# This project was based on gnome-shell-search-github-repositories
# Copyright (C) 2012 Red Hat, Inc.
# Author: Ralph Bean <rbean@redhat.com>
# which itself was based on fedmsg-notify
# Copyright (C) 2012 Red Hat, Inc.
# Author: Luke Macken <lmacken@redhat.com>


import subprocess

import dbus
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)
import dbus.glib

import dbus.service
from gi.repository import GLib

# Convenience shorthand for declaring dbus interface methods.
# s.b.n. -> search_bus_name
search_bus_name = 'org.gnome.Shell.SearchProvider2'
sbn = dict(dbus_interface=search_bus_name)


class BrowserSearchService(dbus.service.Object):
    """ The Browser search daemon.
    This service is started through DBus activation by calling the
    :meth:`Enable` method, and stopped with :meth:`Disable`.
    """
    bus_name = 'org.gnome.Browser.SearchProvider'

    _object_path = '/' + bus_name.replace('.', '/')

    def __init__(self):
        self.session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(self.bus_name, bus=self.session_bus)
        dbus.service.Object.__init__(self, bus_name, self._object_path)
        
    @dbus.service.method(in_signature='sasu', **sbn)
    def ActivateResult(self, id, terms, timestamp):
        self.open_browser(id)

    @dbus.service.method(in_signature='as', out_signature='as', **sbn)
    def GetInitialResultSet(self, terms):
        return terms

    @dbus.service.method(in_signature='as', out_signature='aa{sv}', **sbn)
    def GetResultMetas(self, ids):
        return [dict(id=id, name=id,) for id in ids]

    @dbus.service.method(in_signature='asas', out_signature='as', **sbn)
    def GetSubsearchResultSet(self, previous_results, new_terms):
        return new_terms
    @dbus.service.method(in_signature='asu', terms='as', timestamp='u', **sbn)
    def LaunchSearch(self, terms, timestamp):
        pass

    @staticmethod
    def open_browser(name):
        subprocess.Popen(["firefox", f"https://duckduckgo.com/?q={name}"])


def main():
    BrowserSearchService()
    GLib.MainLoop().run()


if __name__ == '__main__':
    main()
