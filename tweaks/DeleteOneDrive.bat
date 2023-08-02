taskkill /f /im OneDrive.exe & %systemroot%\SysWOW64\OneDriveSetup.exe /uninstall
reg delete HKCR\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6} /f
reg delete HKCR\Wow6432Node\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6} /f
rd /s /q %userprofile%\OneDrive
rd /s /q %userprofile%\AppData\Local\Microsoft\OneDrive
rd /s /q "%allusersprofile%\Microsoft OneDrive"