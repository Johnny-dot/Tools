del %cd%\fancy-dev.cfg
echo build.lua -d>%cd%\fancy-dev.cfg

php build_foa_20151013.php platform=android isdebug=true bigversion=v1 tag=yunying lang=zh use_sdk=true use_localserverlist=true toapple=false path=D:\XA-Trunk flag=old