# this reads grid 3 files. Finds image in one grid page and same one in another and replaces it with a new one

# Compile me python -m PyInstaller --onefile --windowed imagereplace-qt.py


import zipfile
from google_images_download import google_images_download
import re
import os, shutil
from glob import glob
from sys import exit, argv, exc_info, stderr
import traceback

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QApplication, \
  QMessageBox, QLabel, QMainWindow, QFileDialog, QPushButton, QLineEdit

from threading import Timer, Thread

app = None
default_bundle = 'Original.gridset'
default_keywords = 'AceCentre UK'

def find_replace(bundle, images, updatemsgf=None):
    """Read a bundle. Find. Replace. Save bundle."""
    if updatemsgf != None:
        updatemsgf("Extract bundle")
    # 1. Sanity check. Check extension
    # 2. Unzip

    zip_ref = zipfile.ZipFile(bundle, 'r')
    zip_ref.extractall('bundle')
    zip_ref.close()
    
    # 3. Lets now get a file list. THIS IS A TERRIBLE BIT OF code    
    all_files = [y for x in os.walk('bundle/') for y in glob(os.path.join(x[0], '*.jpg'))]
    
    # Get a list of all starting items, and all similar 'win' items. Put them in a dict
    # WARNING: All pages need to be named something 999 and something 999 win for this to work
    r = re.compile("bundle[/\\\\]Grids[/\\\\]([a-zA-Z]+) ([0-9]+)[/\\\\]([0-9]+)-([0-9]+).jpg")
    startPages = list(filter(r.match, all_files))
    print(startPages)
    no_of_images = len(startPages)
    # 4. Now find the relevant 'win pages'

    if updatemsgf != None:
        updatemsgf("Search & Download")
    pageDict = dict()
    for p in startPages:
        # For each one - find the corresponding 'win' page
        m = re.search("bundle[/\\\\]Grids[/\\\\]([a-zA-Z]+) ([0-9]+)[/\\\\]([0-9]+)-([0-9]+).jpg", p)
        if m:
            pageDict['bundle/Grids/'+ m.group(1)+' '+m.group(2)+'/'+m.group(3)+'-'+m.group(4)+'.jpg'] = 'bundle/Grids/'+m.group(1) + ' '+ m.group(2) + ' win/0-0.jpg'
    
    # 5. Lets get some images from google. 
    
    response = google_images_download.googleimagesdownload()
    absolute_image_paths = response.download({"keywords":images,"limit":no_of_images,"s":">800*600","a":"wide","image_directory":"newImages",'format':'jpg',"print_paths":True})

    # 6. Now lets navigate the folder structure structure looking for each element and replacing it with the right image. 
        
    i = 0

    if updatemsgf != None:
        updatemsgf("Replace & Create new bundle")
    for mainImage, thumbImage in pageDict.items():
        if len(absolute_image_paths[images][i]) > 0:
            print("copy: ", absolute_image_paths[images][i], mainImage)
            shutil.copy(absolute_image_paths[images][i], mainImage)
            shutil.move(absolute_image_paths[images][i], thumbImage)
        i = i + 1   
        
    # 7. Zip it all up.
    new_name = "".join([c for c in images if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    shutil.make_archive('Final.gridset', 'zip', 'bundle/')
    shutil.move('Final.gridset.zip', new_name+'.gridset')
    
def cleanup ():
    shutil.rmtree('bundle/', ignore_errors=True)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

class FindReplaceThread (Thread):
    def __init__ (self, bundle, search, msgSignal):
        self._bundle = bundle
        self._search = search
        self._msgSignal = msgSignal
        super().__init__()
    
    def run (self):
        try:
            find_replace(self._bundle, self._search, self.updateMsg)
            cleanup()
            self.updateMsg("Ready")
        except:
            etype, exc, exctb = exc_info()
            self.updateMsg("Error: " + repr(exc))
            print(traceback.format_exc(), file=stderr)
    
    def updateMsg (self, msg):
        if self._msgSignal != None:
            self._msgSignal.emit(msg)

class Window (QMainWindow):
    statusMessageSignal = pyqtSignal(str)

    def __init__ (self):
        super(Window, self).__init__()
        self.statusMessageSignal.connect(self.updateStatusMessageSignal)
        self._worker = None
        mainLayout = QVBoxLayout()
        
        tmp = QHBoxLayout()
        label = QLabel("Bundle: ")
        self.teditBundle = QLineEdit(default_bundle)
        self.btnBrowseBtn = QPushButton("Browse")
        self.btnBrowseBtn.clicked.connect(self.bundleBrowseClicked)
        tmp.addWidget(label)
        tmp.addWidget(self.teditBundle)
        tmp.addWidget(self.btnBrowseBtn)
        mainLayout.addLayout(tmp)

        tmp = QHBoxLayout()
        label = QLabel("Search: ")
        self.teditSearch = QLineEdit(default_keywords)
        tmp.addWidget(label)
        tmp.addWidget(self.teditSearch)
        mainLayout.addLayout(tmp)

        self.btnStart = QPushButton("Start")
        self.btnStart.clicked.connect(self.startClicked)
        mainLayout.addWidget(self.btnStart)
        
        self._window = QWidget()
        self._window.setLayout(mainLayout)
        self.setCentralWidget(self._window)
        
        self.title = "Image Replace (Google Search)"
        self.left = 100
        self.top = 100
        self.width = 480
        self.height = 150
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        screen_resolution = app.desktop().screenGeometry()
        screenWidth = screen_resolution.width()
        screenHeight = screen_resolution.height()
        width = self.width
        height = self.height
        self.setGeometry((screenWidth/2)-(width/2),
                         (screenHeight/2)-(height/2), width, height)
        
        self.statusBar().showMessage('Ready')

    def bundleBrowseClicked (self, sender):
        filepath, a2 = QFileDialog.getOpenFileName(self, "Open Bundle File")
        if filepath != None and filepath != "":
            self.teditBundle.setText(filepath)

    def startClicked (self):
        if self._worker != None and self._worker.isAlive():
            self.btnStart.setEnabled(False)
            return
        bundle = self.teditBundle.text()
        search = self.teditSearch.text()
        self._worker = FindReplaceThread(bundle, search, self.statusMessageSignal)
        self._worker.start()
        self.btnStart.setEnabled(False)

    def onUpdateStatus2 (self):
        # Also update worker status
        if self._worker == None or not self._worker.isAlive():
            self.btnStart.setEnabled(True)
            self._worker = None
        

    def updateStatusMessageSignal (self, msg):
        self._update_timer = Timer(0.1, self.onUpdateStatus2)
        self._update_timer.start()
        self.statusBar().showMessage(msg)


def main ():
    global app
    app = QApplication(argv)
    try:
        QApplication.setQuitOnLastWindowClosed(True)
        window = Window()
        window.show()
        return app.exec_()
    except:
        raise
        #QMessageBox.critical(None, "MorseWriter Fatal Error", "{}".format(traceback.format_exc()))
        #return 1

if __name__ == '__main__':
  ret = main()
  exit(ret)
