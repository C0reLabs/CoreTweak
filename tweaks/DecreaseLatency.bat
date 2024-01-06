@echo off

echo Applying SystemResponsiveness10.reg
regedit.exe /s "tweaks\SystemResponsiveness10.reg"

echo Applying SpeedUpPowerOff.reg
regedit.exe /s "tweaks\SpeedUpPowerOff.reg"

echo Applying MouseDataQueue.reg
regedit.exe /s "tweaks\MouseDataQueue.reg"

echo Applying IncreaseBgQuality.reg
regedit.exe /s "tweaks\IncreaseBgQuality.reg"

echo Applying DisableStoreAutoUpdate.reg
regedit.exe /s "tweaks\DisableStoreAutoUpdate.reg"

echo Applying DesktopTweaks.reg
regedit.exe /s "tweaks\DesktopTweaks.reg"

echo Applying KeyboardDataQueue.reg
regedit.exe /s "tweaks\KeyboardDataQueue.reg"

echo Applying DisableAutoPlay.reg
regedit.exe /s "tweaks\DisableAutoPlay.reg"

echo Applying DisableCortana.reg
regedit.exe /s "tweaks\DisableCortana.reg"

echo Applying DisableLastAccessUpdate.reg
regedit.exe /s "tweaks\DisableLastAccessUpdate.reg"

echo Applying UnloadDLL.reg
regedit.exe /s "tweaks\UnloadDLL.reg"