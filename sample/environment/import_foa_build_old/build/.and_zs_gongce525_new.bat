del %cd%\fancy-dev.cfg
echo build.lua -d>%cd%\fancy-dev.cfg

php build_foa_20151013.php platform=android isdebug=false bigversion=v1 tag=zs lang=zh use_sdk=true use_localserverlist=false toapple=false path=F:\gongce5-25\XA flag=new innetpath=E:\nginx-1.10.2\html outnetpath=E:\app_foa