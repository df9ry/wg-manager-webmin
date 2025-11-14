#!/usr/bin/perl
# /usr/share/webmin/wg-manager/delete_client.cgi

use strict;
use warnings;
use WebminCore;

init_config();

my $name = $in{'name'};

if ($name) {
    # Lösch-Tool aufrufen (das bauen wir später)
    my $output = sudo /usr/share/webmin/wg-manager/wg-removeclient "$name" 2>&1;
    my $success = $? == 0;
    
    if ($success) {
        redirect("index.cgi?message=" . &url_encode("Client $name erfolgreich gelöscht"));
    } else {
        redirect("index.cgi?message=" . &url_encode("Fehler: $output"));
    }
} else {
    redirect("index.cgi?message=" . &url_encode("Kein Client Name angegeben"));
}

exit 0;