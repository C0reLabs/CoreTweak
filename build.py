import os, sys
import shutil
from glob import glob
from zipfile import ZipFile


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
    
    def build(self, removeBuild: bool = True, makeZip: bool = False):
        print(logo)
        os.system(f'''pyinstaller {'--onefile' if self.onefile else ''} {'--clean' if self.clean else ''} --upx-dir "{sys.path[0]}\\upx" --name "{self.name + ' Dev Build' if self.dev else self.name} {self.version}" --icon "{self.icon}" main.py''')

        [shutil.move(file, './') for file in glob('dist/*')]

        if removeBuild:
            self.ClearAll()    

        if makeZip:
            self.makeBuildZip()

    def ClearAll(self):
        if os.path.exists('build/'):
            shutil.rmtree('build/')

        if os.path.exists('dist/'):
            shutil.rmtree('dist/')

        # Remove spec file
        for spec in glob('*.spec'):
            os.remove(spec)

    def makeBuildZip(self):
        with ZipFile(f'./CoreTweaks_{self.version.replace(" ", "_")}.zip', 'w') as zip_object:
            zip_object.write(glob('CoreTweaks*.exe')[0])

            tweaks_dir = './tweaks'
            if os.path.exists(tweaks_dir):
                for root, dirs, files in os.walk(tweaks_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_path = os.path.relpath(file_path, tweaks_dir)
                        zip_object.write(file_path, os.path.join('tweaks', zip_path))

        print('\n\nMaded zip file with builded executable and tweaks.')


Builder(version='1.2 ALPHA', dev=False).build(makeZip=True)


