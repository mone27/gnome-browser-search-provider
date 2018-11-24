#!/usr/bin/env bash
set -eu -o pipefail
cd "$(dirname "$(realpath "${0}")")"

DATADIR=${DATADIR:-/usr/share}
LIBDIR=${LIBDIR:-/usr/lib}
LIBEXECDIR=${LIBEXECDIR:-/usr/lib/}
SYSCONFDIR=${SYSCONFDIR:-/etc}

install -Dm 0755 browser_search_provider.py "${LIBEXECDIR}"/browser_search_provider/browser_search_provider.py

# Search provider definition
install -Dm 0644 conf/org.gnome.Browser.SearchProvider.ini "${DATADIR}"/gnome-shell/search-providers/org.gnome.Browser.SearchProvider.ini

# Desktop file
install -Dm 0644 conf/org.gnome.Browser.SearchProvider.desktop "${DATADIR}"/applications/org.gnome.Browser.SearchProvider.desktop

# DBus configuration
install -Dm 0644 conf/org.gnome.Browser.SearchProvider.service.dbus "${DATADIR}"/dbus-1/services/org.gnome.Browser.SearchProvider.service
install -Dm 0644 conf/org.gnome.Browser.SearchProvider.service.systemd "${LIBDIR}"/systemd/user/org.gnome.Browser.SearchProvider.service