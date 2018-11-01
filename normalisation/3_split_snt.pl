# This script remove the uneccesary headers e.g. date, place, newswire (e.g. afp) from the news.
# Chong Tze Yuang

# Path of the news to be read and write
$pi = "2_expand_abb";
$po = "3_split_snt";

# Year and month of the news
my $yr = $ARGV[0];
my $mn = $ARGV[1];
my $source = $ARGV[2];

# Remove the uneccesary headers e.g. date, place, newswire (e.g. afp)
open $fo , ">" , "output\\$source\\$yr\\$mn\\normalised\\_$mn.tmp1" or die "Couldn't open file to write, $!";
open $fi , "output\\$source\\$yr\\$mn\\normalised\\$mn$yr.txt";

while($line = <$fi>)
{
	$line =~ s/\s-\s/\n/g;
	$line =~ s/\.-/\.\n/g;
	print $fo $line;
}

close $fi;
close $fo;

open $fo , ">" , "output\\$source\\$yr\\$mn\\normalised\\_$mn.tmp2" or die "Couldn't open file to write, $!";
open $fi , "output\\$source\\$yr\\$mn\\normalised\\_$mn.tmp1";

while($line = <$fi>)
{
	$line =~ s/\s-\s/\n/g;
	$ll = $line =~ tr/ //;
	if($ll>10){
		print $fo $line;
	}
}

close $fi;
close $fo;

# Split news into sentences
open $fo , ">" , "output\\$source\\$yr\\$mn\\normalised\\$mn$yr.txt" or die "Couldn't open file to write, $!";
open $fi , "output\\$source\\$yr\\$mn\\normalised\\_$mn.tmp2";

while($line = <$fi>)
{
	$line =~ s/([a-z0-9])\.\s/$1.\n/g;
	$line =~ s/([a-z0-9])\!\s/$1!\n/g;
	$line =~ s/([a-z0-9])\?\s/$1?\n/g;
	#$line =~ s/(\S)\.\s/$1.\n/g;
	#$line =~ s/(\S)\!\s/$1!\n/g;
	#$line =~ s/(\S)\?\s/$1?\n/g;
	print $fo $line;
}

close $fi;
close $fo;
