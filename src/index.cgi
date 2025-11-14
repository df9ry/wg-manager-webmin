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
our %access = &get_module_acl();

# Template für die Ausgabe
my $template = <<'EOF';
[% HEADER -%]

<div class="ui-tabs">
    <ul class="ui-tabs-nav">
        <li><a href="#add-client">Client hinzufügen</a></li>
        <li><a href="#client-list">Client Liste</a></li>
    </ul>

    <div id="add-client">
        <h3>Neuen WireGuard Client erstellen</h3>
        
        [% IF message %]
        <div class="ui-info-box">[% message %]</div>
        [% END %]
        
        <form method="post" action="add_client.cgi">
        <table class="form">
            <tr>
                <td width="150"><label for="name">Client Name:</label></td>
                <td><input type="text" name="name" id="name" size="30" required></td>
            </tr>
            <tr>
                <td><label for="ipv4">IPv4 Adresse:</label></td>
                <td><input type="text" name="ipv4" id="ipv4" value="10.7.0.x/32" size="30" required></td>
            </tr>
            <tr>
                <td><label for="ipv6">IPv6 Adresse:</label></td>
                <td><input type="text" name="ipv6" id="ipv6" value="fddd:2c4:2c4:2c4::x/128" size="30" required></td>
            </tr>
            <tr>
                <td colspan="2" align="center">
                    <input type="submit" value="Client erstellen" class="ui-button">
                </td>
            </tr>
        </table>
        </form>
    </div>

    <div id="client-list">
        <h3>Bestehende Clients</h3>
        [% IF clients && clients.size > 0 %]
        <table class="list">
            <tr>
                <th>Name</th>
                <th>IPv4</th>
                <th>IPv6</th>
                <th>Aktionen</th>
            </tr>
            [% FOREACH client IN clients %]
            <tr>
                <td>[% client.name %]</td>
                <td>[% client.ipv4 %]</td>
                <td>[% client.ipv6 %]</td>
                <td>
                    <a href="delete_client.cgi?name=[% client.name %]" 
                       onclick="return confirm('Client [% client.name %] wirklich löschen?')"
                       class="ui-button ui-button-delete">Löschen</a>
                </td>
            </tr>
            [% END %]
        </table>
        [% ELSE %]
        <p>Keine Clients vorhanden.</p>
        [% END %]
    </div>
</div>

<script>
// Einfaches Tab-Script
document.addEventListener('DOMContentLoaded', function() {
    var tabs = document.querySelectorAll('.ui-tabs-nav a');
    var panes = document.querySelectorAll('.ui-tabs > div');
    
    tabs.forEach(function(tab, index) {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Alle Tabs deaktivieren
            tabs.forEach(function(t) { t.parentNode.classList.remove('ui-tabs-active'); });
            panes.forEach(function(p) { p.style.display = 'none'; });
            
            // Aktiven Tab aktivieren
            this.parentNode.classList.add('ui-tabs-active');
            panes[index].style.display = 'block';
        });
    });
    
    // Ersten Tab aktivieren
    if (tabs.length > 0) tabs[0].click();
});
</script>

<style>
.ui-tabs > div { display: none; }
.ui-tabs-active { background: #e0e0e0; }
.ui-button-delete { background: #d9534f !important; }
</style>

[% FOOTER -%]
EOF

# Clients aus wg0.conf parsen
my @clients = parse_wg_clients();

# Template rendern
my %vars = (
    clients => \@clients,
    message => $in{'message'}
);
&ui_print_template($template, \%vars);

exit 0;

# Hilfsfunktion zum Parsen der Clients
sub parse_wg_clients {
    my @clients;
    my $wg_conf = '/etc/wireguard/wg0.conf';
    
    if (open(my $fh, '<', $wg_conf)) {
        my $current_client;
        while (my $line = <$fh>) {
            if ($line =~ /^#\s*(.+)$/) {
                $current_client = { name => $1 };
            }
            elsif ($line =~ /^AllowedIPs\s*=\s*(.+)$/ && $current_client) {
                my @ips = split(', ', $1);
                $current_client->{ipv4} = $ips[0] if $ips[0];
                $current_client->{ipv6} = $ips[1] if $ips[1];
                push @clients, $current_client;
                $current_client = undef;
            }
        }
        close $fh;
    }
    
    return @clients;
}