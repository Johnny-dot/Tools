@echo off
echo ������Show changed files form SVN������
echo.

svn diff --summarize E:\redgold_oversea_182\Game\tagA\XA
pause

php build_foa_20151013yasuo.php platform=ios bigversion=v1 isdebug=false tag=ajmzs use_sdk=true use_localserverlist=false lang=en path=E:\redgold_oversea_182\Game\tagA\XA sandbox=false toapple=false testapp=false istoiran=false sysversion=8.2.3 flag=old