@echo off
echo ¡ý¡ý¡ýShow changed files form SVN¡ý¡ý¡ý
echo.

svn diff --summarize H:\redgold_oversea\tishen\XA
pause

php build_foa_20151013yasuo.php platform=ios bigversion=v1 isdebug=true tag=ajmcs use_sdk=false use_localserverlist=true lang=en path=H:\redgold_oversea\tishen\XA sandbox=false toapple=false testapp=false istoiran=false sysversion=7.2.0 flag=old