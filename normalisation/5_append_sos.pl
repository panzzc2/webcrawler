# This script remove the uneccesary headers e.g. date, place, newswire (e.g. afp) from the news.
# Chong Tze Yuang

# Path of the news to be read and write
$pi = "4_remove_pnc";
$po = "5_append_sos";

# Year and month of the news
my $yr = $ARGV[0];
my $mn = $ARGV[1];
my $source = $ARGV[2];

# Split news into sentences
open $fo , ">", "output\\$source\\$yr\\$mn\\normalised\\_$mn.tmp4" or die "Couldn't open file to write, $!";
open $fi , "<", "output\\$source\\$yr\\$mn\\normalised\\$mn$yr.txt";

while($line = <$fi>)
{
	$line =~ s/^/\<s\> /;		# sos
	$line =~ s/$/ \<\/s\>/;		# eos
	print $fo $line
}

close $fi;
close $fo;

open(my $fh, '>', "output\\$source\\$yr\\$mn\\normalised\\$mn$yr.txt") or die "Could not open file $!";
open(my $fo, '<', "output\\$source\\$yr\\$mn\\normalised\\_$mn.tmp4") or die "Could not open file $!";

while(my $line = <$fo>)
{

	print $fh $line;
}

close $fh;
close $fo;