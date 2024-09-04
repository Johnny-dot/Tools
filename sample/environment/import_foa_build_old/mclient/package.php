<?php
function get_args( $a ) {
    unset($a[0]);
    $rtn = array( );
    foreach ($a as $key => $value) {
        $b = explode('=', $value);
        $rtn[$b[0]] = $b[1];
    }
    return $rtn;
}
print_r($argv);
$param = get_args( $argv );
print_r($param);
$pdir = $param['path'];

$svn_number = $param['svnnumber'];
// $svn_number = intval(system( 'svnversion '. $pdir));

$params_for_run = <<<EOT
_app.isdebug = false
_app.use_sdk = true
_app.use_localserverlist = {$param['use_localserverlist']}
_app.isweiduan = true
_app.version = $svn_number
_app.bigversion = '{$param['bigversion']}'
_app.sysversion = '{$param['sysversion']}'
_app.toapple = '{$param['toapple']}'
EOT;
file_put_contents( 'version.lua', $params_for_run );

$nowdate = $param['nowtime'];
$outdir = "output/{$param['platform']}_{$param['tag']}_{$svn_number}_{$nowdate}";

$sys_cmd = "fancy-dev.exe -d \"codefile|_build.lua|respath|" . $pdir . "|version|" . $svn_number . "|out|" . $outdir . "|\"";
print_r($sys_cmd);
system($sys_cmd);
