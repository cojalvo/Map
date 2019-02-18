import os, os.path, datetime, string, errno
from maperipy import *
import GenIsraelHikingTilesLite

# http://stackoverflow.com/questions/749711/how-to-get-the-python-exe-location-programmatically
MaperitiveDir = os.path.dirname(os.path.dirname(os.path.normpath(os.__file__)))
# App.log('MaperitiveDir: ' + MaperitiveDir)
ProgramFiles = os.path.normpath(os.path.dirname(MaperitiveDir))
# App.log('ProgramFiles: ' + ProgramFiles)
IsraelHikingDir = os.path.dirname(os.path.dirname(os.path.normpath(App.script_dir)))
# App.log('App.script_dir: ' + App.script_dir)
# App.log('IsraelHikingDir: ' + IsraelHikingDir)
App.run_command('change-dir dir="' + IsraelHikingDir +'"')
os.chdir(IsraelHikingDir)

# # Keep the name of the Tile Upload command
# upload_tiles = os.path.join(IsraelHikingDir, "Scripts", "Batch", "UploadTiles.bat")

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def add_to_PATH(app_dir):
    full_app_dir=os.path.join(ProgramFiles, app_dir)
    for path_dir in (string.split(os.environ["PATH"], os.pathsep)):
        if os.path.basename(path_dir) == app_dir:
            # Application already found in PATH
            return
    if not os.path.isdir(full_app_dir):
        # Application not a sibling of Maperitive
        App.log("Warning: " + app_dir + " location not found. Could not add it to PATH.")
        return
    os.environ["PATH"] = string.join([os.environ["PATH"],full_app_dir], os.pathsep)



# Keep batch windows open up to 24 hours
os.environ["NOPAUSE"] = "TIMEOUT /T 86400"

# os.rmdir(os.path.join(IsraelHikingDir, 'Site', 'Tiles_Lite' ))

gen_cmd =  GenIsraelHikingTilesLite.IsraelHikingTileGenCommand()

App.run_command("run-script file=" + os.path.join("Scripts", "Maperitive", "IsraelHikingLite.mscript"))
# Map Created
#Original# App.run_command("generate-tiles minzoom=7 maxzoom=15 subpixel=3 tilesdir=" + IsraelHikingDir + "\Site\Tiles use-fprint=true")
gen_cmd.GenToDirectory(16, 16, os.path.join(IsraelHikingDir, 'Site', 'Tiles_Lite'))
App.collect_garbage()


