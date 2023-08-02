import os, sys
import shutil
from glob import glob

logo = '''
   ____ ___  ____  _____ _______        _______    _    _  ______  
  / ___/ _ \|  _ \| ____|_   _\ \      / / ____|  / \  | |/ / ___| 
 | |  | | | | |_) |  _|   | |  \ \ /\ / /|  _|   / _ \ | ' /\___ \ 
 | |__| |_| |  _ <| |___  | |   \ V  V / | |___ / ___ \| . \ ___) |
  \____\___/|_| \_\_____| |_|    \_/\_/  |_____/_/   \_\_|\_\____/ 
                                                                   builder
'''

class Builder:
    def __init__(self, onefile: bool = True, clean: bool = True, name: str = 'CoreTweaks', icon: str = 'tweaks\\coretweaks.ico', dev: bool = False, version: str = '1.0'):
        self.onefile = onefile
        self.clean = clean
        self.name = name
        self.icon = icon
        self.dev = dev
        self.version = version
    
    def build(self, removeBuild: bool = True):
        print(logo)
        os.system(f'''pyinstaller {'--onefile' if self.onefile else ''} {'--clean' if self.clean else ''} --upx-dir "{sys.path[0]}\\upx" --name "{self.name + ' Dev Build' if self.dev else self.name} {self.version}" --icon "{self.icon}" gui.py''')

        [shutil.move(file, './') for file in glob('dist/*')]

        if removeBuild:
            self.ClearAll()        

    def ClearAll(self):
        shutil.rmtree('build/')
        shutil.rmtree('dist/')

        # Remove spec file
        for spec in glob('*.spec'):
            os.remove(spec)

Builder(version='1.0 ALPHA', dev=False).build()