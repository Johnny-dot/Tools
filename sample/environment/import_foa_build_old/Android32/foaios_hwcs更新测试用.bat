@echo off
echo ������Show changed files form SVN������
echo.

svn diff --summarize H:\redgold_oversea\tishen\XA
pause

php build_foa_20151013.php platform=ios bigversion=v1 isdebug=true tag=hwcs use_sdk=false use_localserverlist=true lang=en path=H:\redgold_oversea\tishen\XA sandbox=false toapple=false testapp=false istoiran=false sysversion=7.2.4