use XML::LibXML;
# Paths
my $pi = "output";

# Year and month of the news
my $yr = $ARGV[0];
my $mn = $ARGV[1];
my $source = $ARGV[2];

$parser = XML::LibXML->new();

mkdir "$pi/$source/$yr/$mn/normalised";
	    
my $filename = "$pi\\$source\\$yr\\$mn\\normalised\\$mn$yr.txt";
open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
	      
for my $dy (1..31) {
	$dy = sprintf("%02d", $dy);
	$mn = sprintf("%02d", $mn);
	
	my $file = "$pi\\$source\\$yr\\$mn\\$dy$mn$yr.xml";

	if (-e $file) {
	
	$corpus = XML::LibXML->load_xml(
	      location => $file
	      # parser options ...
	    );
	     my $unwantedChars = 'normalisation\\regex.txt';
	     
	    
     
	foreach my $article ($corpus->findnodes('//article//p/text()')) {
	    
	    open(my $fi, '<', $unwantedChars) or die "Could not open file '$unwantedChars' $!"; # All unwanted characters 
	    
	    while (my $row = <$fi>) {
	    	# Checks predefined patterns
	    	chomp $row;
	   	 	$article =~ s/$row//g;
	    }
	    
	   	close $fi;
		print $fh $article."\n"; # Write to file
	    
	  }
	}
	
	else {
	next;
	}
}
	  
	  close $fh;