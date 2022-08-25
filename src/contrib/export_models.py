from mimetypes import suffix_map
import Metashape
import sys

"""
Metashape disable model Script (v 1.0)
Kent Mori, Feb 2022

Usage:
Workflow -> Batch Process -> Add -> Run script
This scrip export whole models of chunks. When use system arguments[1], you can add suffix at the export file names.
"""

compatible_major_version = "1.8"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))

doc = Metashape.app.document
chunks = doc.chunks

print(len(sys.argv))
if len(sys.argv) == 1: # default is no suffix.
    suffix = ""
else: # suffix is made from sys.argv 
    suffix = "_" + str(sys.argv[1])



for chunk in chunks:
    if chunk.enabled is True:
        if chunk.model is None:
            continue
        else:
            chunk.exportModel(path = "/".join(doc.path.split("/")[:-1]) + "/" + chunk.label + "_models/fromMS/" + chunk.label + suffix + ".obj",
            texture_format=Metashape.ImageFormat.ImageFormatPNG)
            #ImageFormatJPEG
# export each quarity models of each chunks
# chunk.label + quarity["high" or "low"] + ".obj"
