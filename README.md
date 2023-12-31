# box-envelope
Helper tool to draw the flat representation of an envelope that could fit around the specified box. Useful for laser cutting, for example, wrapping paper for a gift

# Usage
Call the script with the desired height, width, depth of the box for which you want to create an envelope.
The output of the SVG file will contain the envelope in green. It also contains the fold lines in red. These fold lines can for example be used to perform perforation using the laser cutter, as helper for folding the envelope.

## Example
A typical 999 Games gamebox, is appr. 122mmx96mmx20mm. Taking 2mm margin:
- python3 box-envelope.py 124 98 22 box-124_98_22.svg

# Dependencies
The script uses Python3 module svgwrite. Install it through your package manager, e.g.:
- sudo apt install python3-svgwrite
Tested is svgwrite 1.4.1

# Future work
Currently the 'flaps' are not configureable (well, you can adapt them by tinkering in the code). This can be made configureable. Also, the flaps have straight corners. It would be nicer to have rounded corners instead. Also the angle currently depends on the size of the box as it goes to just next to the middle of the box. It would be nice to stick to certain angles (e.g. near 45 degrees) and add a horizontal segment when needed.

# License
GPLv3, see LICENSE file