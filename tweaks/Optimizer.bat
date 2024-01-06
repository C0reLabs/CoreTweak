@echo off
call :USER_DEFINED

:processaffinity
if defined affinity (
	if not %affinity% GTR 0 goto INVALID_AFFINITY
	PowerShell -NoLogo -NoProfile -NonInteractive -Command "get-process dwm,audiosvchost,audiodg,lsass,svchost,WmiPrvSE | ForEach-Object {$_.ProcessorAffinity=%affinity%}"
)

:INVALID_AFFINITY
wmic process where name="winlogon.exe" call setpriority 32

:: clear Temp folder
rd /s /q "%temp%" & mkdir "%userprofile%\AppData\Local\Temp"

exit /b

:USER_DEFINED
wmic process where name="dwm.exe" call setpriority 32
wmic process where name="lsass.exe" call setpriority 64
wmic process where name="svchost.exe" call setpriority 64
wmic process where name="WmiPrvSE.exe" call setpriority 64

