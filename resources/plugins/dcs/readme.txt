
Place Export.lua and the directory GCA-ExportScript in ~/Saved Games/DCS/Scripts. You may have to create the Scripts directory yourself.
If a previous Export.lua already resides there, instead of overwriting it, just add the following line last in the existing file:

dofile(lfs.writedir()..[[Scripts\GCA-ExportScript\ExportScript.lua]])