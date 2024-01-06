@echo off

reg delete HKCR\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6} /f > NUL 2>&1
reg delete HKCR\Wow6432Node\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6} /f > NUL 2>&1


rd /s /q %userprofile%\OneDrive > NUL 2>&1
rd /s /q %userprofile%\AppData\Local\Microsoft\OneDrive > NUL 2>&1
rd /s /q "%allusersprofile%\Microsoft OneDrive" > NUL 2>&1

reg query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT

if %OS%==64BIT set "OneDriveSetupPath=%systemroot%\SysWOW64\OneDriveSetup.exe"
if %OS%==32BIT set "OneDriveSetupPath=%systemroot%\System32\OneDriveSetup.exe"


taskkill /f /im OneDrive.exe > NUL 2>&1

echo Uninstalling OneDrive
%OneDriveSetupPath% /uninstall > NUL 2>&1

timeout /t 5 /nobreak > NUL 2>&1

echo Done!