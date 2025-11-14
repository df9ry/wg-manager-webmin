#!/usr/bin/perl
#
# WebMin WireGuard Manager - Client management for WireGuard VPN
# Copyright (C) 2024 Reiner Hagn (df9ry)
# Copyright (C) 2024 DeepSeek AI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

use strict;
use warnings;

# WebMin Core Pfad hinzufügen
BEGIN {
    unshift @INC, '/usr/share/webmin';
}

use WebminCore;
init_config();

my $name = $in{'name'};
my $ipv4 = $in{'ipv4'};
my $ipv6 = $in{'ipv6'};

if ($name && $ipv4 && $ipv6) {
    my $script_path = '/usr/share/webmin/wg-manager/wg-addclient';
    my $command = "sudo $script_path \"$name\" \"$ipv4\" \"$ipv6\" 2>&1";
    my $output = $command;
    my $success = $? == 0;
    
    if ($success) {
        redirect("index.cgi?message=" . &url_encode("Client $name erfolgreich erstellt"));
    } else {
        redirect("index.cgi?message=" . &url_encode("Fehler: $output"));
    }
} else {
    redirect("index.cgi?message=" . &url_encode("Bitte alle Felder ausfüllen"));
}

exit 0;