@echo off
echo ¡ý¡ý¡ýShow changed files form SVN¡ý¡ý¡ý
echo.

svn diff --summarize E:\FW\redgold_oversea\branches\tishen\XA
pause

php build_foa_20151013.php platform=ios bigversion=v1 isdebug=true tag=hwfb use_sdk=true use_localserverlist=true lang=en path=E:\FW\redgold_oversea\branches\tishen\XA sandbox=true toapple=true testapp=false istoiran=false sysversion=8.1.1