@echo off
echo Disabling telemetry..

sc stop DiagTrack > NUL 2>&1
sc config DiagTrack start= disabled > NUL 2>&1
sc delete DiagTrack > NUL 2>&1

sc stop dmwappushservice > NUL 2>&1
sc config dmwappushservice start= disabled > NUL 2>&1
sc delete dmwappushservice > NUL 2>&1

set F=%TEMP%\al.reg
set F2=%TEMP%\al2.reg

regedit /e "%F%" "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\WMI\Autologger\AutoLogger-Diagtrack-Listener" > NUL 2>&1

powershell -Command "Select-String -Pattern "\"Enabled\"", "\[HKEY", "Windows\sRegistry" -Path \"%F%\" | ForEach-Object {$_.Line} | Foreach-Object {$_ -replace '\"Enabled\"=dword:00000001', '\"Enabled\"=dword:00000000'} | Out-File \"%F2%\"" > NUL 2>&1

regedit /s "%F2%" > NUL 2>&1
del "%F%" "%F2%" > NUL 2>&1
del "%ProgramData%\Microsoft\Diagnosis\ETLLogs\AutoLogger\*.etl" "%ProgramData%\Microsoft\Diagnosis\ETLLogs\ShutdownLogger\*.etl" > NUL 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\AutoLogger-Diagtrack-Listener" /v "Start" /t REG_DWORD /d 0 /f > NUL 2>&1

sc config diagnosticshub.standardcollector.service start= disabled > NUL 2>&1

:: Disabling services
schtasks /change /TN "Microsoft\Windows\Autochk\Proxy" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\Application Experience\ProgramDataUpdater" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\Application Experience\StartupAppTask" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\Customer Experience Improvement Program\Consolidator" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\Customer Experience Improvement Program\KernelCeipTask" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\Customer Experience Improvement Program\UsbCeip" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticResolver" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\Maintenance\WinSAT" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\NetTrace\GatherNetworkInfo" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Windows\PI\Sqm-Tasks" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Office\Office ClickToRun Service Monitor" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Office\OfficeTelemetry\AgentFallBack2016" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Office\OfficeTelemetry\AgentFallBack2016" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Office\OfficeTelemetry\OfficeTelemetryAgentLogOn2016" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Office\OfficeTelemetryAgentFallBack2016" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Office\OfficeTelemetryAgentLogOn2016" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Office\OfficeTelemetryAgentFallBack" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Office\OfficeTelemetryAgentLogOn" /DISABLE > NUL 2>&1
schtasks /change /TN "Microsoft\Office\Office 15 Subscription Heartbeat" /DISABLE > NUL 2>&1


set isNvidia=0
nvidia-smi > nul 2>&1

if %errorlevel% equ 0 (
    set isNvidia=1
)

if %isNvidia% equ 1 (
    echo Nvidia GPU detected, removing telemetry

    reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NvTelemetryContainer" /v "Start" /t REG_DWORD /d 4 /f > NUL 2>&1

    schtasks /change /TN NvTmRepOnLogon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} /DISABLE > NUL 2>&1
    schtasks /change /TN NvTmRep_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} /DISABLE > NUL 2>&1
    schtasks /change /TN NvTmMon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} /DISABLE > NUL 2>&1
    net stop NvTelemetryContainer > NUL 2>&1
    sc config NvTelemetryContainer start= disabled > NUL 2>&1
    sc stop NvTelemetryContainer > NUL 2>&1
)

echo Done!