@echo off
echo ¡ý¡ý¡ýShow changed files form SVN¡ý¡ý¡ý
echo.

svn diff --summarize E:\redgold_oversea_182\Game\tagA\XA
pause

php build_foa_20151013.php platform=ios bigversion=v1 isdebug=false tag=hwfb use_sdk=true use_localserverlist=false lang=en path=E:\redgold_oversea_182\Game\tagA\XA sandbox=false toapple=true testapp=false istoiran=false sysversion=8.2.2