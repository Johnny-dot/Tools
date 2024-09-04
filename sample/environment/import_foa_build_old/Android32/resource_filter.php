<?php
// tag = pvr or etc
// path = H:\test-Yoh\XA
$tag = $argv[1];
$xapath = $argv[2];

function ismd5changed($directory, $filename) {
    $tag = $GLOBALS["tag"];
    $md5 = md5_file($directory);
    if (!file_exists("./md5_". $tag .".txt")) return true;
    $content = file_get_contents("./md5_". $tag .".txt");
    $array = explode("\n", $content);
    $GLOBALS["originallist"] = $array;
    $is = true;
    for($i = 0; $i < count($array); $i++)
    {
        if ( $array[$i] == "" ) continue;
        $elementarr = explode("=", $array[$i]);
        if ($elementarr[0] == $filename ) {
            $is = $elementarr[1] != $md5;
            break;
        }
    }
    return $is;
 }

function createmd5file($directory) {
    $md5file = $GLOBALS["md5file"];
    $current_dir = opendir($directory);
    while(($file = readdir($current_dir)) !== false) {
        $sub_dir = $directory . "/" . $file;
        if($file == "." || $file == "..") {
            continue;
        } else if(is_dir($sub_dir)) {
            createmd5file($sub_dir);
        } else {
            fwrite($md5file, "$file=" . md5_file($sub_dir) . "\n");
        }
    }
}

function opreateupdatefile($directory) {
    $updatefile = $GLOBALS["updatefile"];
    $current_dir = opendir($directory);
    while(($file = readdir($current_dir)) !== false) {
        $sub_dir = $directory . "/" . $file;
        if($file == "." || $file == "..") {
            continue;
        } else if(is_dir($sub_dir)) {
            copytoclientpvr($sub_dir);
            opreateupdatefile($sub_dir);
        } else {
            if ( ismd5changed($sub_dir, $file) ) {
                echo "$file\n";
                fwrite($updatefile, "['$file']='" . md5_file($sub_dir) . "',\n");
                copytoclientpvr($sub_dir);
            }
        }
    }
}

function copytoclientpvr ($sub_dir) {
    $fileto = str_replace("../redgold_oversea/XA/", "./client_". $GLOBALS["tag"] ."_new/", $sub_dir);
    if (is_dir($sub_dir)) {
        if (!file_exists($fileto)) {
            mkdir($fileto);
        }
        return;
    }

    copy($sub_dir, $fileto);
}


function deletefile() {
    $tag = $GLOBALS["tag"];
    if (!file_exists("./md5_". $tag .".txt")) return true;
    $content = file_get_contents("./md5_". $tag .".txt");
    $newlist = explode("\n", $content);
    $originallist = $GLOBALS["originallist"];

    for($i = 0; $i < count($originallist); $i++)
    {
        $is = true;
        if ($originallist[$i] == "") continue;
        $elementarr = explode("=", $originallist[$i]);
        for ($j = 0; $j < count($newlist); $j++) {
            if ($newlist[$j] == "") continue;
            $newarr = explode("=", $newlist[$j]);
            if ($elementarr[0] == $newarr[0]) {
                $is = false;
                break;
            }
        }
        if ($is) {
            echo "********** remove file ************ \n";
            echo "$elementarr[0]\n";
            $path = removefilepath("./client_". $tag ."_new/res", $elementarr[0]);
            unlink($path);
        }
    }
}

function removefilepath($directory,$filename)
{
    $current_dir = opendir($directory);
    $res = null;
    while(($file = readdir($current_dir)) !== false) {
        $sub_dir = $directory . "/" . $file;
        if($file == "." || $file == "..") {
            continue;
        } else if(is_dir($sub_dir)) {
            $res = removefilepath($sub_dir, $filename);
            if ($res != null) break;
        } else {
            if ($filename == $file) {
                $res = $sub_dir;
                break;
            }
        }
    }
    return $res;
}

$originallist = array();

if (!file_exists("./client_" . $tag . "_new/res")) {
    mkdir("./client_" . $tag . "_new/res");
}

echo "**** changed or new file list ***** \n";
$updatefile = fopen("updatelist_". $tag .".lua", file_exists("./md5_" . $tag .".txt") ? "w+" : "a+");
fwrite($updatefile, "return {\n");
opreateupdatefile($xapath . "/res");
fwrite($updatefile, "}");
echo "*********************************** \n";

echo "****** create all files md5 ******* \n";
$md5file = fopen("./md5_" . $tag .".txt", "w+");
createmd5file($xapath . "/res");
echo "*********************************** \n";

fclose($updatefile);
fclose($md5file);

deletefile();
?>