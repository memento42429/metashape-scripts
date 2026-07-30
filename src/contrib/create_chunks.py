import Metashape
from pathlib import Path
import sys

"""
Metashape create chunks Script
- SubfolderごとにChunkを作成し、画像をaddPhotosする
- 画像が1枚も無いフォルダはChunkを作らずスキップする

Usage:
Workflow -> Batch Process -> Add -> Run script

argv[1]: root folder (subfolders inside it)
argv[2]: (optional) extension like "jpg" or ".jpg"
"""

import Metashape
from pathlib import Path
import sys

COMPATIBLE_MAJOR_VERSION = "2.2"
found_major_version = ".".join(Metashape.app.version.split(".")[:2])
if found_major_version != COMPATIBLE_MAJOR_VERSION:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, COMPATIBLE_MAJOR_VERSION))

DEFAULT_EXTS = [".jpg", ".jpeg", ".tif", ".tiff", ".png", ".dng"]

def createchunks(path, image_types=None, recursive=False):
    if image_types is None:
        image_types = DEFAULT_EXTS

    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(str(root))

    doc = Metashape.app.document

    folders = [p for p in root.iterdir() if p.is_dir()]
    folders.sort(key=lambda p: p.name.lower())

    for folder in folders:
        files = list(folder.rglob("*")) if recursive else list(folder.iterdir())

        photo_list = []
        for f in files:
            if f.is_file() and f.suffix.lower() in image_types:
                photo_list.append(str(f.resolve()))

        photo_list.sort()

        if len(photo_list) == 0:
            print('skip "{}" (no images)'.format(folder.name))
            continue

        chunk = doc.addChunk()
        chunk.label = folder.name
        chunk.addPhotos(photo_list)

        print('added {} photos in "{}"'.format(len(photo_list), folder.name))

    Metashape.app.update()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("YOU MUST ENTER THE PATH IN ARGV")
        sys.exit(1)

    path = sys.argv[1]

    if len(sys.argv) >= 3:
        ext = sys.argv[2].lower().strip()
        if not ext.startswith("."):
            ext = "." + ext
        if ext not in DEFAULT_EXTS:
            print('YOU SHOULD ENTER THE SUFFIX AMONG ".jpg", ".jpeg", ".tif", ".tiff", ".png", ".dng"')
            sys.exit(2)
        image_types = [ext]
    else:
        image_types = DEFAULT_EXTS

    createchunks(path, image_types=image_types, recursive=False)