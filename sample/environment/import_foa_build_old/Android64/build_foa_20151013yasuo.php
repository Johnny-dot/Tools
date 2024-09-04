<?php
/*
 * !!!参数中不要有空格
 * platform = ios|android 目标平台
 * isdebug = true|false 是否调试模式
 * tag = 标记 说明
 * path = res的地址
 * use_sdk = true|false 是否使用sdk
 * use_localserverlist = true|false 是否使用本地服务器
 * lang = zh 语言包标识 ar, be, da, de, en, es, fr, it, pt, th, tr; tw
 * php build_foa_20151013.php platform=android bigversion=v1 isdebug=true tag=dev use_sdk=false use_localserverlist=true lang=zh path=C:\Users\Aoktian\fancy3d\chengxu\trunk\XA sandbox=true toapple=false foc=null
 * testapp=true 测试服专用包参数
 * innetpath = 内网foa地址 F:\nginx-1.8.0\html，自动拷贝foa到内网地址，不加不拷贝
 * outnetpath = 外网foa地址 F:\hyres\inner，自动拷贝foa到外网地址，不加不拷贝
*/

date_default_timezone_set('Asia/Shanghai');
function iprint( $s ) {
    echo $s;
    echo "\n";
}

function get_args( $a ) {
    unset($a[0]);
    $rtn = array( );
    foreach ($a as $key => $value) {
        $b = explode('=', $value);
        $rtn[$b[0]] = $b[1];
    }
    return $rtn;
}
$param = get_args( $argv );

print_r($param);

$pdir = $param['path'];
iprint('path:' . $pdir);

$svn_number = intval(system( 'svnversion '. $pdir ));
iprint('svn_number:' . $svn_number);

iprint( "remove temp ..." );
system( 'rmdir /s/q temp' );
mkdir('./temp');

iprint( "Copy files from " . $pdir . " to temp ..." );
system( 'xcopy /s/q ' . $pdir . '\\code temp\\code\\ /e' );

if ($param['platform'] == 'ios') {
    $res = $pdir . '\\res_pvr_bf';
    if (!file_exists($res)) {
        $res = $pdir . '\\res';
    }
} elseif ($param['platform'] == 'android') {
    $res = $pdir . '\\res_etc_bf';
    if (!file_exists($res)) {
        $res = $pdir . '\\res';
    }
} else {
    $res = $pdir . '\\res';
}

iprint( "Copy " . $res . " ..." );
system( 'xcopy /s/q ' . $res . ' temp\\res\\ /e' );

$params_for_run = <<<EOT
_app.isdebug = {$param['isdebug']}
_app.use_sdk = {$param['use_sdk']}
_app.use_localserverlist = {$param['use_localserverlist']}
_app.version = $svn_number
_app.channel = '{$param['tag']}'
_app.lang = '{$param['lang']}'
_app.sandbox = '{$param['sandbox']}'
_app.isAppleStoreReview = {$param['toapple']}
_app.bigversion = '{$param['bigversion']}'
_app.istestapp = '{$param['testapp']}'
_app.sysversion = '{$param['sysversion']}'
_app.istoiran = {$param['istoiran']}
EOT;
file_put_contents( 'temp/code/version.lua', $params_for_run );

iprint( "change jit version ..." );

$foaname = 'foa';
system( 'rmdir /s/q jit' );
system( 'del /q luajit.exe' );
if ($param['platform'] == 'android') {
    $foaname = 'afoa';
    system( 'xcopy luajit200 %cd% /e' );
} else {
    system( 'xcopy luajit201 %cd% /e' );
}

$nowdate = date('mdHi');
$outdir = "output/{$param['platform']}_{$param['tag']}_{$svn_number}";
$focName = "{$param['foc']}";

$params_for_build = <<<EOT
time = '$nowdate'
version = $svn_number
mainPlugin = 'plugin.fob'
name = 'rghw'
path = 'temp'
platform = "{$param['platform']}"
out = '{$outdir}'
code = 'code/main.lua'
foaName = '$foaname'
focName = ''
EOT;
file_put_contents( 'version.lua', $params_for_build );

system( 'fancy-dev.exe' );

chmod($outdir, 777);

file_put_contents( $outdir . '/build.lua', $params_for_build );
file_put_contents( $outdir . '/run.lua', $params_for_run );


$tempdir = dir('./' . $outdir);
$platform_simplify = $param['platform'] == 'android' ? 'and' : 'ios';
$foaname_final = "{$platform_simplify}_{$param['tag']}_{$svn_number}.foa";
while($file = $tempdir->read()) {
    $arr = explode('.', $file);
    $type = $arr[1];
    if ($type == 'foa' ) {
        rename($outdir . '/' . $file, $outdir . '/' . $foaname_final);
        break;
    }
}
$tempdir->close();

if ($param['outnetpath']) {
    if (copy($outdir . '/' . $foaname_final, $param['outnetpath'] . '\\' . $foaname_final))
        iprint( 'Copy foa to app_foa Success!' );
}

exit();
