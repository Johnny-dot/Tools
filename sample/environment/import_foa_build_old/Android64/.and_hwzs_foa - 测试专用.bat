@echo off
echo ������Show changed files form SVN������
echo.

svn diff --summarize E:\redgold_oversea_182\Game\tagA\XA
pause

php build_foa_20151013.php platform=android bigversion=v1 isdebug=true tag=hwzs64_test use_sdk=false use_localserverlist=true lang=en path=E:\redgold_oversea_182\Game\tagA\XA sandbox=false toapple=false testapp=false istoiran=false sysversion=8.2.3 is64=true