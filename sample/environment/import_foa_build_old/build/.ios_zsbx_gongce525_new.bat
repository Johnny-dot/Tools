@echo off


copy F:\gongce5-25\logo_kbzy.png F:\gongce5-25\XA\res_pvr1\icon\logo_kbzy.png


pause

del %cd%\fancy-dev.cfg
echo build.lua -d>%cd%\fancy-dev.cfg

php build_foa_20151013��С.php platform=ios isdebug=false bigversion=v1 tag=zsbx lang=zh use_sdk=true use_localserverlist=false toapple=false path=F:\gongce5-25\XA flag=new innetpath=E:\nginx-1.10.2\html outnetpath=E:\app_foa