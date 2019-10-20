import inspect
import logging
import os
import sys
import traceback

from django.dispatch import Signal
from django.utils.autoreload import StatReloader, autoreload_started, file_changed

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('spreloader')


SP_PROJECT_FILE_TEMPLATE = """
#!/usr/bin/env python3

from solid import *
from solid.utils import *  # Not required, but the utils module is useful

# sample code, remove and start here
d = difference()(
    cube(10, center=True),
    sphere(6)
)

final_object = d

def render():
    scad_render_to_file(final_object, '%s')

"""

SP_RELOADER_TEMPLATE = """
#!/usr/bin/env python3

import importlib
import os
import threading
import traceback
import subprocess
import sys

from spreloader.spreloader import SPReloader, autoreload_started

# prevent syntax errors from breaking the reload loop
try:
    import %s
except Exception:
    traceback.print_exc()

scad_file = "%s"

def run_openscad():
    subprocess.run(["openscad",scad_file])

def render_on_autoreload(sender, **kwargs):
    importlib.reload(%s)
    %s.render()

if __name__ == "__main__":
    openscad = threading.Thread(target=run_openscad, args=(), daemon=True)
    openscad.start()
    reloader = SPReloader()
    reloader.reload_signal.connect(render_on_autoreload)
    reloader.reload_signal.send(sender=reloader.__class__)
    current_dir = os.getcwd()
    # add or modify a line here if you want to trigger a reload 
    # for other files or file types
    reloader.watch_dir(current_dir, "*py")
    reloader.watch_dir(current_dir, "*svg")

    reloader.run()
"""



class SPReloader(StatReloader):
    reload_signal = Signal()

    def run(self):
        """
        works like the original, but doesn't depend on django main thread
        """
        autoreload_started.send(sender=self)
        logging.info("Solidpython reloader started.")        
        self.run_loop()

    def notify_file_changed(self, path):
        """works like the original, but doesn't exit on file change.
        """
        results = file_changed.send(sender=self, file_path=path)
        logger.debug('%s notified as changed. Signal results: %s.', path, results)
        if not any(res[1] for res in results):
            logger.info('%s changed, reloading.', path)
        # prevent syntax errors from breaking the reload loop
        try:
            self.reload_signal.send(sender=self)
        except Exception:
            traceback.print_exc()

def startproject(project_name):
    """
    creates a directory and prepares a few files for convenience
    """
    current_path = os.getcwd()
    project_path = os.path.join(current_path, project_name)
    # create directory
    os.mkdir(os.path.join(current_path, project_name), 0o755)

    # create main solid python file
    file_name = "%s.py" % project_name
    scad_file_name = "%s.scad" % project_name
    with open(os.path.join(project_path, file_name),"w") as f:
        f.write(SP_PROJECT_FILE_TEMPLATE % scad_file_name)
    # and an empty openscad file
    file_name = scad_file_name
    with open(os.path.join(project_path, file_name),"w") as f:
        f.write('')
    # create the reloader for this project
    file_name = "run.py"
    with open(os.path.join(project_path, file_name),"w") as f:
        f.write(SP_RELOADER_TEMPLATE % (project_name, scad_file_name, project_name, project_name))
    logger.info('Project %s created.', project_name)

def main():
    script_name = os.path.basename(sys.argv[0])
    try:
        command = sys.argv[1]
    except IndexError:
        print("No command provided, e.g. %s startproject project_name" % script_name)
        sys.exit(1)
    try:
        project_name = sys.argv[2]
    except IndexError:
        print("No project name provided, e.g. %s startproject project_name" % script_name)
        sys.exit(1)
    startproject(project_name)



if __name__ == "__main__":
    main()