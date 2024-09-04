<?php
function iprint( $s ) {
    echo $s;
    echo "\n";
}
$svn_number = intval(system( 'svnversion '. $pdir ));
iprint('svn_number:' . $svn_number);
?>