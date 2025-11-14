#!/usr/bin/perl
print "Content-type: text/plain\n\n";

my @paths = (
    '/usr/share/webmin',
    '/usr/libexec/webmin', 
    '/opt/webmin',
    '/usr/local/webmin'
);

foreach my $path (@paths) {
    if (-d $path) {
        print "✅ Found: $path\n";
        if (-f "$path/WebminCore.pm") {
            print "   📁 WebminCore.pm exists!\n";
        }
    } else {
        print "❌ Not found: $path\n";
    }
}