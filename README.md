# PC98 disk image tools
Here are some various tools for dealing with PC98 disk images.

## History
Many historical image sets of PC98 software store them in "BKDSK" HDM format, but at the time [the FlashFloppy firmware](https://github.com/keirf/FlashFloppy) only supported FDI images. A converter was needed to convert them.

Most people used the closed-source (AFAIK) [Virtual Floppy Image Converter](https://www.vector.co.jp/soft/win95/util/se151106.html) tool, which is excellent. Out of fear of the software one day becoming incompatible, I wanted to figure out for myself what the format differences were. Also, it didn't run right in WINE.

## The tools
 * `is_fdi.py`: Has a bunch of best-guess heuristics about whether or not a random image actually _is_ in the FDI format. I ran across a few that were just raw images renamed to *.FDI, and so had nonsense headers or the wrong size.
 * `hdm_to_fdi.py`: Converts HDM images to FDI by generating a fake FDI header for a "2HD"-size disk, and then appends the header and the pad bytes to the front of the HDM raw image. This worked with FlashFloppy. I don't think it will work if you have any other BKDSK size format (e.g. `*.HD5` or `*.DD9`). Patches very welcome. It also worked for me on a D88 image that was converted using [d88split](https://github.com/tomari/d88split)'s `d882mhlt` utility, which makes me think that any raw (i.e. uncompressed) Mahalito image will work. 
