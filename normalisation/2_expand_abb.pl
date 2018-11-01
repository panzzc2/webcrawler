# This script expand abbreviations in the text
# Chong Tze Yuang
# Phuah Chee Chong

# Path of the news to be read and write

use Lingua::EN::Numbers qw(num2en num2en_ordinal);

my $pi = "output";

# Year and month of the news
my $yr = $ARGV[0];
my $mn = $ARGV[1];
my $source = $ARGV[2];

# Split news into sentences
my $original = "$pi\\$source\\$yr\\$mn\\normalised\\$mn$yr.txt";
my $expandedAbrv = "$pi\\$source\\$yr\\$mn\\normalised\\_$mn.tmp";

my $abrv = "normalisation\\abrv.txt";

open(my $fh, '<', $original) or die "Could not open file '$original' $!";
open(my $fo, '>', $expandedAbrv) or die "Could not open file '$expandedAbrv' $!";

while(my $line = <$fh>)
{

	open(my $fi, '<', $abrv) or die "Could not open file '$abrv' $!"; # All unwanted characters 

	   		while (my $row = <$fi>) {
	    	# Checks predefined patterns
	    	# Skips comment lines
	    	
	    	next if ($row =~ /^#/);
	    		
	    	chomp $row;
	    	my @abrvList = split("/", $row);
	    	my $pattern = @abrvList[0];
	    	my $rText = @abrvList[1];
	    	
	   	 	$line =~ s/$pattern/$rText/g;
	    }
	    
	    # Convert numbers to words!
   	 	# First we must extract the digits
   	 	my @numbers;
   	 	
   	 	while ($line =~ /(([1-9]\d*((,\d+)|(\.\d+))|\d+))/g) {
			push @numbers, $1;
		}
		foreach (@numbers){ 
			my $origNum = $_; # Temporary Storage
			$_ =~ s/,//g; # Remove commas
			my $numWord = num2en($_);
			$line =~ s/($origNum){1}/$numWord/;
		}

	   	close $fi;
	

	print $fo $line;
}

close $fh;
close $fo;

# Open tmp to write back to original

open(my $fh, '>', $original) or die "Could not open file '$original' $!";
open(my $fo, '<', $expandedAbrv) or die "Could not open file '$expandedAbrv' $!";

while(my $line = <$fo>)
{

	print $fh $line;
}

close $fh;
close $fo;
