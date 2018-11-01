# This script remove the unneccesary headers e.g. date, place, newswire (e.g. afp) from the news.
# Chong Tze Yuang

# Path of the news to be read and write
$pi = "3_split_snt";
$po = "4_remove_pnc";

# Year and month of the news
my $yr = $ARGV[0];
my $mn = $ARGV[1];
my $source = $ARGV[2];

# Open files to read and write
open $fo , ">", "output\\$source\\$yr\\$mn\\normalised\\_$mn.tmp3" or die "Couldn't open file to write, $!";
open $fi , "<", "output\\$source\\$yr\\$mn\\normalised\\$mn$yr.txt";

while($line = <$fi>)
{
	# Remove the parentheses
	# To be refined: the parentheses should embrace any character except parenthesis (!!!!!)
	$line =~ s/\([\w\d\s\.\,\-]+\)/ /g;
	# Remove the punctuations
	#$line =~ s/[\,\.\!\?\-\\\&\*"':;`]+ / /g;	# remove punctuation that follows a space
	#$line =~ s/[\,\.\!\?\-\\\&\*"':;`]+$//g;	# remove punctuation that follows a boundary
	#$line =~ s/ [\,\.\!\?\-\\\&\*"':;`]+/ /g;	# remove punctuation that precedes a space
	#$line =~ s/^[\,\.\!\?\-\\\&\*"':;`]+//g;	# remove punctuation that precedes a boundary
	# Remove the hyphens
	# To be refined: the expression may not be general enough (!!!!!)
	#$line =~ s/([\w\d])\-([\w\d])/$1 $2/g;
	# Remove other noises
	$line =~ s/[^\w\d\s]/ /g;
	# Remove duplicate spaces
	$line =~ s/ +/ /g;
	$line =~ s/ $//g;
	$line =~ s/^ //g;
	# Convert all charaters to lowercase
	$line = lc $line;
	# Write to file
	print $fo $line;
}

# Close files
close $fi;
close $fo;


open(my $fh, '>', "output\\$source\\$yr\\$mn\\normalised\\$mn$yr.txt") or die "Could not open file $!";
open(my $fo, '<', "output\\$source\\$yr\\$mn\\normalised\\_$mn.tmp3") or die "Could not open file $!";

while(my $line = <$fo>)
{

	print $fh $line;
}

close $fh;
close $fo;
