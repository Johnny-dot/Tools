<?php
date_default_timezone_set('Asia/Shanghai');
function iprint( $s ) {
    echo $s;
    echo "\n";
}

function build($argv, $debug, $dev, $itime, $pvr) {
    $channels = array(
        'dev' => array(
            'igamehost' => '10.1.1.103',
            ),
        'test' => array(
            'igamehost' => '10.1.1.103',
            ),
        'neice' => array(
            'igamehost' => '123.59.40.194',
            ),
        'yinqing' => array(
            'igamehost' => '10.1.1.103',
            ),
        'kb' => array(
            'igamehost' => '123.59.46.6',
            ),
        'youzu' => array(
            'igamehost' => '120.132.69.194',
            ),
        'banshu' => array(
            'igamehost' => '10.1.1.103',
            ),
    );
    if ( !isset( $channels[$argv[1]] ) ) {
        echo 'arg error';
        exit();
    }

    $channel = $argv[1];
    iprint('channel:'.$channel);
    $pdir = $argv[2];
    iprint('path:'.$pdir);
    $desc = $argv[3];
    iprint('desc:'.$desc);
    $version = intval(system( 'svnversion '. $pdir ));
    iprint('version:'.$version);
    $igamehost = $channels[$channel]['igamehost'];
    iprint('igamehost:'.$igamehost);

    iprint( "-----------start-build---------" . $debug . '--' . $dev);
    iprint( "remove temp ..." );
    system( 'rmdir /s/q temp' );
    mkdir('./temp');
    iprint( "Copy files from ".$pdir." to temp ..." );
    iprint( "Copy code ..." );
    system( 'xcopy /s/q '.$pdir.'\\code temp\\code\\ /e' );
    $res = $pdir.'\\res'.$pvr;
    if (!file_exists($res)){
        $res = $pdir.'\\res';
    }
    iprint( "Copy ".$res." ..." );
    system( 'xcopy /s/q '.$res. ' temp\\res\\ /e' );

$version_lua = <<<EOT
_app.isdebug = $debug
_app.igamehost = '$igamehost'
_app.version = '$version'
_app.channel = '$channel'
_app.bigversion = _sys:getGlobal('bigversion')
EOT;
file_put_contents( 'temp/code/version.lua', $version_lua );

    $foaname = 'foa';
    iprint( "change jit version ..." );
    system( 'rmdir /s/q jit' );
    system( 'del /q luajit.exe' );
    if($dev == 'android'){
        $foaname = 'afoa';
        system( 'xcopy luajit200 %cd% /e' );
    }else{
        system( 'xcopy luajit201 %cd% /e' );
    }

    $foasign = '';
    if($debug == 'true') {
        $foasign = '_debug';
    }

$version_lua = <<<EOT
time = '$itime'
version = $version
desc =  '$desc'
mainPlugin = 'plugin.fob'
name = 'rg'
path = 'temp'
out = 'output/$channel'..'_'..'$itime'..'_'..'$version'..'_'..'$desc'
code = 'code/main.lua'
foaName = '$foaname'..'$foasign'
EOT;
    file_put_contents( 'version.lua', $version_lua );

    system( 'fancy-dev.exe' );
    iprint( "--------------foa-end---------------" );
}

$itime = date('mdHi');
iprint('itime:'.$itime);
if ($argv[4] == 'ios'){
    if ($argv[5] == 'true'){
        build($argv, 'true', 'ios', $itime, '_pvr');
    }else{
        build($argv, 'true', 'ios', $itime, '_pvr');
        build($argv, 'false', 'ios', $itime, '_pvr');
    }
}elseif ($argv[4] == 'android'){
    if ($argv[5] == 'true'){
        build($argv, 'true', 'android', $itime, '');
    }else{
        build($argv, 'true', 'android', $itime, '');
        build($argv, 'false', 'android', $itime, '');
    }
}elseif ($argv[4] == 'all'){
    if ($argv[5] == 'true'){
        build($argv, 'true', 'ios', $itime, '_pvr');
        build($argv, 'true', 'android', $itime, '');
    }else{
        build($argv, 'true', 'ios', $itime, '_pvr');
        build($argv, 'false', 'ios', $itime, '_pvr');
        build($argv, 'true', 'android', $itime, '');
        build($argv, 'false', 'android', $itime, '');
    }
}

exit();