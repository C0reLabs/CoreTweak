import os, sys
import psutil
from download import download

# cd to current directory
current_path = os.popen(r'echo %cd%').read().replace('\n', '')
os.chdir(current_path)

schemes = []
regtweaks = []
vcpp = 'https://cdn.discordapp.com/attachments/1070727971515662447/1135279225973243924/vcpp.zip'
hpet_link = 'https://cdn.discordapp.com/attachments/1070727971515662447/1135286240611151872/checkhpet.exe'

IsWin11 = lambda : True if sys.getwindowsversion().build >= 22000 else False
IsWin10 = lambda : False if sys.getwindowsversion().build >= 22000 else True
IsHDD = lambda: any(
    partition.fstype.lower() == 'ntfs'
    for partition in psutil.disk_partitions(all=True)
    if partition.mountpoint == '/'
)

class RegFile:
    def __init__(self, name: str, 
                 desc: str, 
                 file: str, 
                 silent: bool = True, 
                 powerrun: bool = False, 
                 only11: bool = False, 
                 only10: bool = False,
                 recommended: bool = False,
                 dangerous: bool = False):
        self.name = name
        self.desc = desc
        self.file = file
        self.silent = silent
        self.powerrun = powerrun
        self.only11 = only11
        self.only10 = only10
        self.recommended = recommended
        self.dangerous = dangerous

        if self.recommended:
            self.desc += '\nRecommended tweak.'

        if self.only10:
            self.desc += '\nOnly for Windows 10!'

        if self.only11:
            self.desc += '\nOnly for Windows 11!'

        if self.dangerous:
            self.desc += '\nWe do not recommend using this tweak.'

        regtweaks.append(self)

    def run(self):
        if self.only11 and IsWin10():
            print('This tweak is only for Windows 11!')
            return
    
        if self.only10 and IsWin11():
            print('This tweak is only for Windows 10!')
            return

        print(f'Applying: {self.name} tweak!')
        if self.powerrun:
            os.system(f'tweaks\\PowerRun.exe regedit.exe {" /s" if self.silent else ""} "tweaks/{self.file}.reg"')
        else:
            os.system(f'regedit.exe {" /s" if self.silent else ""} "tweaks\\{self.file}.reg"')

        print('Done!')

    def __str__(self):
        return self.name
    
    def checkCompatibility(self):
        if self.only11 and IsWin10():
            return False
        
        if self.only10 and IsWin11():
            return False
        
        if 'Only For SSD' in self.name and not IsHDD():
            return False
        
        return True

class PowerPlanFile:
    def __init__(self, name: str, desc: str, file: str, dangerous: bool = False):
        self.name = name
        self.desc = desc
        self.file = file
        self.dangerous = dangerous

        if self.dangerous:
            self.desc += '\nWe do not recommend using this power plan.'

        schemes.append(self)

    def run(self):
        print(f'Applying: {self.name} scheme!')
        scheme_import = os.popen(f'powercfg /import "{current_path}\\tweaks\\{self.file}.pow"').read()
        scheme_guid = scheme_import[scheme_import.find('GUID: ') + len('GUID: '):]

        # Set PowerPlan
        os.system(f'powercfg /S {scheme_guid}')

        print('Done!')

    def __str__(self):
        return self.name

class CMDTweak(RegFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        print(f'Applying: {self.name} tweak!')
        with open(f'tweaks/{self.file}.bat', 'r') as tweak:
            data = tweak.read()

            for line in data.split('\n'):
                os.system(line)

def RegTweakByName(query: str):
    for tweak in regtweaks:
        if tweak.name == query:
            tweak.run()

def PowerPlanByName(query: str):
    for scheme in schemes:
        if scheme.name == query:
            scheme.run()

def InstallVCPP():
    if not os.path.isdir('vcpp'):
        os.mkdir('vcpp')
        download(vcpp, 'vcpp/', 'zip', replace=True)
    vcpps = os.listdir('vcpp')
    vcpps.sort()

    for vc in vcpps:
        print(f'Installing {vc}..')
        if '2005' in vc:
            os.system(f'vcpp\\{vc} /q')
        elif '2008' in vc:
            os.system(f'vcpp\\{vc} /qb')
        else:
            os.system(f'vcpp\\{vc} /passive /norestart')

def InstallDirectX():
    print('Installing DirectX..')
    os.system('tweaks\\directx.exe')
    print('Done!')

def CheckHPET():
    print('We opened the app, check the "Current resolution". If it is 1.000 or ~15.000, it\'s okay.')
    os.system('tweaks\\checkhpet.exe')

def MsiModeTools():
    print('We opened the Msi Mode Tool application. Find all your video cards, enable MSI, and select High instead of undefined. Then, on the top right, click on apply.')
    os.system('tweaks\\PowerRun.exe tweaks\\MSIModeTool.exe')

UWPApps = {
    '3D Builder': '*3dbuilder*',
    'Alarms & Clock': '*windowsalarms*', 
    'Calculator': '*windowscalculator*', 
    'Camera': '*windowscamera', 
    'Get Office': '*officehub*', 
    'Groove Music': '*zunemusic*', 
    'Mail/Calendar': '*windowscommunicationapps*', 
    'Maps': '*windowsmaps*', 
    'Microsoft Solitaire Collection': '*solitairecollection*', 
    'Movies & TV': '*zunevideo*',
    'Microsoft Store': '*windowsstore*',
    'News': '*bingnews*', 
    'OneNote': '*onenote*', 
    'Microsoft Phone Companion': '*windowsphone*', 
    'Photos': '*photos*', 
    'Skype': '*skypeapp*', 
    'Tips': '*getstarted*', 
    'Voice Recorder': '*sound recorder*', 
    'Weather': '*bingweather*', 
    'Xbox': '*xboxapp*'}

def removeUWP(uwp: str, revert = False):
    app = {v: k for k, v in UWPApps.items()}[uwp]
    if not revert:
        print('Removing: ' + app + ', please wait..')
        os.system(f'powershell -command "Get-AppxPackage {uwp} | Remove-AppxPackage"')
        print('Done!')

    elif revert:
        print('Restoring: ' + app + ', please wait..')
        os.system(f'''powershell -command "Get-AppxPackage -allusers {uwp} ''' + ''' | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register """$($_.InstallLocation)\AppXManifest.xml"""}"''')
        print('Done!')

def removeAllUWP():
    for uwp in UWPApps.values():
        print('Removing: ' + uwp)
        os.system(f'powershell -command "Get-AppxPackage {uwp} | Remove-AppxPackage"')

RegFile('Disable Hibernation', 'Removes hibernation, sort of like sleep mode', 'DisableHibernation')
RegFile('Disable Telemetry', 'Disable Telemetry, spying', 'DisableTelemetry')
RegFile('Disable Defender', 'Removes Windows Defender, gives a pretty good FPS boost, but removes protection from your PC', 'DisableDefender', powerrun=True, dangerous=True)
RegFile('Disable Firewall', 'Removes the firewall because it is not needed and may break some LAN emulation applications', 'DisableFirewall', recommended=True)
RegFile('Disable, Meltdown, Tsx, Spectre', 'Removes Meltdown and Spectre protection, gives a small boost in FPS, recommended for AMD processors', 'DisableMeltdownTsxSpectre')
RegFile('Disable Security Notifications', 'The title speaks for itself', 'DisableSecurityNotifications')
RegFile('Disable SysMain (Only for SSD)', 'Removes the SysMain process (fast application startup), useful for SSD, but better not to try this on HDDs', 'DisableSysmain')
RegFile('Enable OldPhotoViewer', 'Includes old photo viewer, useful for HDD', 'OldPhotoViewer', recommended=True)
RegFile('Disable BackgroundProcesses', 'Turns off background processes', 'StopBgProcess', only11=True)
RegFile('Disable Adapter Energysaving', 'Improves the speed of the Internet, sometimes it can increase the Internet speed by 50-70 Mbps', 'DisableAdapterEnergysaving')
RegFile('Disable Scheduler Triggers', 'Removes scheduled tasks so that they do not load the processor in the background', 'DisableSchedulerTriggers')
RegFile('Disable UAC and SmartScreen', 'Removes UAC and SmartScreen, helps restore your nerves', 'DisableUACandSmartScreen')
RegFile('Enable Gamemode', "Enables gamemode", 'EnableGameMode')
RegFile('Disable FullScreenOptimization', 'Disabling full-screen optimization', 'DisableFSO', recommended=True)
RegFile('Enable classic context menu', 'Enables the old context menu in Windows 11', 'ClassicContextMenu', only11=True)
RegFile('Disable Sync', 'Removes synchronization, not recommended to turn off if you do not have a local account', 'DisableSync', dangerous=True)

CMDTweak('Delete OneDrive', 'Completely removes OneDrive from the system', 'DeleteOneDrive', powerrun=True) # beta
CMDTweak('Decrease latency', 'Reduces system latency', 'DecreaseLatency', True, False, recommended=True)
CMDTweak('Optimizing script after login', 'Runs a script that lowers the priority of unnecessary processes', 'StartupBat', recommended=True)
CMDTweak('Disable Task Scheduler Telemetry', 'Exactly the same as the Disable Scheduler Triggers tweak, but removes telemetry', 'DisableTaskSchedulerTelemetry')
CMDTweak('Disable HPET', 'Removes HPET - High Precision Event Timer, improves FPS but may slightly degrade system performance', 'DisableHPET', only10=True)
CMDTweak('Stop Search Indexer', 'Disables file indexing, useful for HDD', 'StopSearchIndexer')

PowerPlanFile('Bitsum Highest Performance', 'Provides Bitsum optimized CPU performance', 'BitsumHighestPerformance')
PowerPlanFile("Muren's Low Latency", 'Disables power-saving features for better performance and lower latency', 'Muren_Idle_Enabled')
PowerPlanFile("Little Unixcorn's PowerPlan without idle", 'A custom power plan for having the best latency', 'Unixcorn', True)

version = '1.1 ALPHA'