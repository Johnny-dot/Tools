@echo off
echo ������Show changed files form SVN������
echo.

svn diff --summarize E:\redgold_oversea_182\Game\tagA\XA
pause

php build_foa_20151013yasuo.php platform=android bigversion=v1 isdebug=false tag=ajmzs use_sdk=true use_localserverlist=false lang=en path=E:\redgold_oversea_182\Game\tagA\XA sandbox=false toapple=false testapp=false istoiran=false sysversion=8.1.3 flag=old