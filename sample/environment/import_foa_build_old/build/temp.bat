cd sample/environment/build
del %cd%\fancy-dev.cfg
echo build.lua -d>%cd%\fancy-dev.cfg
php build_foa_20151013.php platform=android isdebug=false bigversion=v1 tag=and_hwfb lang=zh use_sdk=true use_localserverlist=false toapple=false path=D:\gongce5-25\XA flag=old innetpath=D:\nginx-1.10.2\html outnetpath=D:\Tools\sample\environment\build\output\android_and_hwfb
pause