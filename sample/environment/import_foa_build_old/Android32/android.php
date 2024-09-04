<?php
date_default_timezone_set('Asia/Shanghai');
$channel = $argv[1];

$channels = array(
    'dev' => array(
        'name' => '狂暴之翼-dev',
        'package' => 'fwdev'
        ),
    'test' => array(
        'name' => '狂暴之翼-test',
        'package' => 'fwtest'
        ),
    'neice' => array(
        'name' => '狂暴之翼',
        'package' => 'furiouswings'
        ),
    'yinqing1' => array(
        'name' => '狂暴之翼-yinqing1',
        'package' => 'fwyinqing1'
        ),
    'yinqing2' => array(
        'name' => '狂暴之翼-yinqing2',
        'package' => 'fwyinqing2'
        ),
    'banshu' => array(
        'name' => '狂暴之翼',
        'package' => 'fwbanshu'
        ),
);
if ( !isset( $channels[$channel] ) ) {
    echo 'arg error';
    exit();
}
$appname = $channels[$channel]['name'];
$package = $channels[$channel]['package'];

abc( 'tpl/loading.lua', 'android/assets/loader.fod/loading.lua', 'dev=xxx&c=xxx', 'dev=android&c='.$channel );
abc( 'tpl/strings.xml', 'android/res/values/strings.xml', '<string name="app_name">xxx</string>', '<string name="app_name">'.$appname.'</string>' );
abc( 'tpl/AndroidManifest.xml', 'android/AndroidManifest.xml', 'package="com.Fancy.xxx"', 'package="com.Fancy.'.$package.'"' );

system( 'build_android_apk.bat' );

system( 'move android\\xxx.apk output\\'.$channel.'_'.date('Y_md_Hi').'.apk' );

function abc( $fromfile, $tofile, $search, $replace ) {
    $content = file_get_contents( $fromfile );

    $content = str_replace($search, $replace, $content);
    file_put_contents( $tofile, $content );
}