import Metashape
from pathlib import Path
import sys

"""
Metashape create cunks Script (v 1.0)
Kent Mori, Feb 2023

Usage:
Workflow -> Batch Process -> Add -> Run script
This scrip creates new chunks with folders include images, and add images to the new chunks each.
You get new three chunks named "folder1", "folder2" and "folder3" when you imput "PATH" in argv in following example dir; 

    "PATH" ---- folder1 --- image1-1, image1-2,,,,,
            |
            --- folder2 --- image2-1, image2-2,,,,,
            |
            --- folder3 --- image3-1, image3-2,,,,,
"""

compatible_major_version = "1.8"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))

def createchunks(path):
    root = Path(path)
    print(root)
    abs_root = root.resolve()
    print(abs_root)
    parent = abs_root.parent
    print(parent)
    
    list_folders = list(Path(path).iterdir())
    print(list_folders)
    doc = Metashape.app.document
    
    for afolder in list_folders:
        if afolder.is_dir():
            chunk = doc.addChunk()
            chunk.label = afolder.name
            list_images = list(Path(afolder).iterdir())
            photo_list = list()
            i = 0
            for photo in list_images:
                if any((s in photo.suffix) for s in [".jpg", ".jpeg", ".tif", ".tiff", ".png", ".dng"]):
                    photo_list.append(fr'{photo.__str__()}')     # addPhoto method wants str list nither ospath
                    i = i+1
                else:
                    print('passed')
                    
            chunk.addPhotos(photo_list)
            print(f'added {i} photos in {afolder.name}')
            print('go next \n\n\n')
        else:
            continue

    print('Finished')
    Metashape.app.update()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('YOU MUST ENTER THE PATH IN ARGV')
        sys.exit

    else: # The path images is made from sys.argv 
        path = str(sys.argv[1])
        createchunks(path)