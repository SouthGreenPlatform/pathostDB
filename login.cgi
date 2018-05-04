#!/usr/bin/perl
use warnings;
use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use File::Spec;
use Data::Dumper;
use Exporter;
use Digest::SHA qw(sha1_hex);

use Configuration;

my $cgi = CGI->new;
my $session = $cgi->param('session');
my $session_dir = "$Configuration::HTML_DIR/tmp/";

my $identifiant    = $cgi->param('identifiant');
my $motdepasse       = $cgi->param('motdepasse');
my $message_erreur = '';
my $cookie = $cgi->cookie( -name => $session );
my $file_session = File::Spec->catfile( $session_dir , 'sess_' . $cookie );



#file to know is the user is log in or not
my $LOG = "$Configuration::TMP_DIR/log.info";
open (F , ">", $LOG) or die ("erreur: \n $!\n");

#file with account informations
my $FILE = "$Configuration::TMP_DIR/log_account.txt";
open (FILE , "<", $FILE) or die ("erreur: \n $!\n");
my @list_id;
my @list_password;
while(my $line = <FILE>){
  chomp $line;
  my ($id, $pass) = split(/\t/, $line);
  push (@list_id, $id);
  push (@list_password, $pass);
}

#crypt the password entered by user
my $crypt = sha1_hex($motdepasse);
chomp $crypt;

#check if id and password are in the database
#if in database, will redirect to the upload page
#if not will redirect to the fail page
if ( $cgi->request_method() eq 'POST'and $cgi->param('connexion')){
  if ( ($identifiant ~~ @list_id) &&(grep /$crypt/, @list_password)) 
  {
  identifiant => $identifiant ;
  #print $cgi->redirect('http://bioinfo-test.ird.fr:84/cgi-bin/file_upload.cgi?session=$session');
  print F "yes \n";
  print $cgi->redirect('file_upload.cgi?session=$session');
  }
  else {
  print $cgi->redirect('log_fail.cgi?session=$session');
  # "Mauvaise session ou bouton connexion non pressé => page normale";
  }
}

else {
  print $cgi->redirect('log_fail.cgi?session=$session');
  # "Mauvaise session ou bouton connexion non pressé => page normale";
}


close(F);