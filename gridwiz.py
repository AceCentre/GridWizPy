# this reads grid 3 files. Finds image in one grid page and same one in another and replaces it with a new one

import zipfile
import click
from google_images_download import google_images_download
import re
import os, shutil
from glob import glob

@click.command()
@click.option('--bundle', default='Original.gridset', help='We need a bundle to work on')
@click.option('--images', default='AceCentre UK', help='What images do you want?')
            

def find_replace(bundle,images):
    """Read a bundle. Find. Replace. Save bundle."""
    
    # 1. Sanity check. Check extension
    # 2. Unzip
    zip_ref = zipfile.ZipFile(bundle, 'r')
    zip_ref.extractall('bundle')
    zip_ref.close()
    
    # 3. Lets now get a file list. THIS IS A TERRIBLE BIT OF code    
    all_files = [y for x in os.walk('bundle/') for y in glob(os.path.join(x[0], '*.jpg'))]
    
    # Get a list of all starting items, and all similar 'win' items. Put them in a dict
    # I know this is mad. Its historic.I should rewrite this bit but it works and I'm lazy
    # WARNING: All pages need to be named something 999 and something 999 win for this to work
    r = re.compile("bundle/Grids/([a-zA-Z]+) ([0-9]+)/([0-9]+)-([0-9]+).jpg")
    startPages = list(filter(r.match, all_files)) 
    # 4. Now find the relevant 'win pages'

    pageDict = dict()
    for p in startPages:
        # For each one - find the corresponding 'win' page
        m = re.search("bundle/Grids/([a-zA-Z]+) ([0-9]+)/([0-9]+)-([0-9]+).jpg", p)
        if m:
            pageDict['bundle/Grids/'+ m.group(1)+' '+m.group(2)+'/'+m.group(3)+'-'+m.group(4)+'.jpg'] = 'bundle/Grids/'+m.group(1) + ' '+ m.group(2) + ' win/0-0.jpg'
    
    # 5. Lets get some images from google. 

    no_of_images = len(pageDict)+1
    
    response = google_images_download.googleimagesdownload()
    absolute_image_paths = response.download({"keywords":images,"limit":no_of_images,"s":">800*600","a":"wide","image_directory":"newImages",'format':'jpg',"print_paths":True})

    # 6. Now lets navigate the folder structure structure looking for each element and replacing it with the right image. 
        
    i = 0

    for mainImage, thumbImage in pageDict.items():
        shutil.copy(absolute_image_paths[images][i], mainImage)
        shutil.move(absolute_image_paths[images][i], thumbImage)
        i = i + 1   
        
    # 7. Zip it all up. 
    new_name = "".join([c for c in images if c.isalpha() or c.isdigit() or c==' ']).rstrip()

    shutil.make_archive('Final.gridset', 'zip', 'bundle/')
    shutil.move('Final.gridset.zip', new_name+'.gridset')
    
    
    

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

        
if __name__ == '__main__':
    find_replace()
    filelist = [ f for f in os.listdir('bundle/') if f.endswith(".jpg") ]
    for f in filelist:
        os.remove(os.path.join('bundle/', f))



