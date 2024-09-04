@echo off
echo ¡ý¡ý¡ýShow changed files form SVN¡ý¡ý¡ý
echo.

svn diff --summarize E:\redgold_oversea_182\Game\tagA\XA
pause

php build_foa_20151013.php platform=android bigversion=v1 isdebug=false tag=hwzs64 use_sdk=true use_localserverlist=false lang=en path=E:\redgold_oversea_182\Game\tagA\XA sandbox=false toapple=false testapp=false istoiran=false sysversion=8.2.3 is64=true