# GoPro Photo Organizer / Importer

This program is an alternative to the GoPro studio importer that allows you to import photos taken by a GoPro into a more customizable set of directories and file names.

More specifically, the program allows you to:
 - Sort media by type so that photos, videos, and timelapses are in separate directories.
 - Choose whether files are stored by date taken or in a single directory.
 - Rename files to the time they were taken (and choose the time format used)
 - Explicitly include or exclude LRV and THM files
 - 'Import' files from any directory structure, allowing you to move your exisitng imported GoPro files into a different format.

## Project Structure

The codebase is split into two modules and a test package:
 - `organizercore` contains the logic for identifying and moving files.
 - `organizerui` contains the user interface code that makes use of `organizercore`.
 - `tests` contains test classes.

## Key Concepts

The `file_matcher.py` class contains regular expressions for matching GoPro files as identified by their [published file formats](http://gopro.com/support/articles/hero3-and-hero3-file-naming-convention).

The `oranizer.py` class contains the core logic for walking the input directory and moving identified files. The class walks the directory structure until it reaches the end, so it does not require files to be in the typical input format (i.e. in DCIM sub-directories).

## Tests
Tests can be run using nose and the following command:
   `nosetests`

## Creating an Executable
The provided `MakeFile` shows the commands required to install dependencies, and to run the installer. 

The project uses _py2app_ to create an executable version of the project. On Mac, this can be run to create a .app file:
   `python setup.py py2app`

On Windows, you can use _py2exe_ to create a .EXE file:
   `python setup.py py2exe`

The windows command requires access to DLL files from the 'Microsoft Visual C++ 2008 SP1 Redistributable Package', which you can get from the [Microsoft Site](https://www.microsoft.com/en-us/download/details.aspx?id=2092).

You will find these DLL files referenced directly in the `setup.py` file.