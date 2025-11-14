#!/usr/bin/perl
# /usr/share/webmin/wg-manager/add_client.cgi

use strict;
use warnings;
use WebminCore;

init_config();

my $name = $in{'name'};
my $ipv4 = $in{'ipv4'};
my $ipv6 = $in{'ipv6'};

if ($name && $ipv4 && $ipv6) {
    # Dein Tool aufrufen
    my $output = sudo /usr/share/webmin/wg-manager/wg-addclient "$name" "$ipv4" "$ipv6" 2>&1;
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