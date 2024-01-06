@echo off
echo Disabling dynamic tick..
bcdedit /set disabledynamictick yes
echo Disabling synthetic timers..
bcdedit /set useplatformtick yes
echo Done!