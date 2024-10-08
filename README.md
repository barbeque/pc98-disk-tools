# PC98 disk image tools
Here are some various tools for dealing with PC98 disk images.

## History
Many historical image sets of PC98 software store them in "BKDSK" HDM format, but at the time [the FlashFloppy firmware](https://github.com/keirf/FlashFloppy) only supported FDI images. A converter was needed to convert them.

Most people used the closed-source (AFAIK) [Virtual Floppy Image Converter](https://www.vector.co.jp/soft/win95/util/se151106.html) tool, which is excellent. Out of fear of the software one day becoming incompatible, I wanted to figure out for myself what the format differences were. Also, VFIC didn't run right in WINE, which meant having to use a real Windows machine every time I wanted to update or add images.

Nowadays, the FlashFloppy firmware supports HDM images, so this code is primarily useful as a reference.

## Getting Started
Download this repository using the "Download ZIP" option under the Code menu at the top of the page, then unzip the zip. Make sure you have Python 3 installed.

## The tools
### `is_fdi.py`
Has a bunch of best-guess heuristics about whether or not a random image actually _is_ in the FDI format. I ran across a few that were just raw images renamed to .FDI, and so had nonsense headers or the wrong size.

Useful so you don't waste too much time looking at an image that can't possibly be right.

#### Usage:
```bash
$ python3 is_fdi.py Windows\ 95\ \?\?\?\?\?\?.fdi
dummy = 0
fddtype = 144
header size = 4096
fdd size = 1261568
sector size = 1024
sectors = 8
surfaces = 2
cylinders = 77
Windows 95 ??????.fdi: yes
```

### `hdm_to_fdi.py`
Converts raw HDM images to FDI by generating a fake FDI header for a "2HD"-size disk, and then appends the header and the pad bytes to the front of the HDM raw image.

This worked with FlashFloppy. I don't think it will work if you have any other BKDSK size format (e.g. `*.HD5` or `*.DD9`).

It also worked for me on a D88 image that was converted using [d88split](https://github.com/tomari/d88split)'s `d882mhlt` utility, which makes me think that any raw (i.e. uncompressed) Mahalito image will work.

Patches very welcome.

#### Usage:
```bash
$ python3 hdm_to_fdi.py Lemmings.hdm
Converting Lemmings.hdm
Completed write of Lemmings.fdi
```

### `fdi_to_hdm.py`
Converts FDI images to HDM (raw) by clawing the first 4096 bytes off of them and then sanity-checking that they seem like the right length afterward.

This worked to convert a few FDI images to a raw image that I could mount with `mount_disk_image.sh`.

#### Usage:
```bash
$ python3 fdi_to_hdm.py Lemmings.fdi
Completed write of Lemmings.hdm
```

### `hdi_to_flat.py`
Converts an *.HDI hard disk image into a flat image, suitable for writing to a CompactFlash card or other destination hard drive using `dd` or similar tool.

#### Usage:
```bash
$ python3 hdi_to_flat.py A Ressha de Ikou III HD - Hard Disk Only.hdi
Completed write of A Ressha de Ikou III HD - Hard Disk Only.img
```

### `make_blank_image.py`
Produces a blank FDI or HDM image. Determines which one based on the extension given.

### Usage:
```bash
% python3 make_blank_image.py blank.fdi
Wrote blank.fdi
```

### `mount_disk_image.sh`
Convenience script to mount a raw MSDOS disk image as a loopback on macOS.

Mounts read-write, so be careful if you are afraid of corrupting a disk image.

#### Usage:
```bash
$ sh mount_disk_image.sh Lemmings.hdm
/dev/disk3	/Volumes/Untitled
```

On Linux, you would probably use something like `mount -o loop Lemmings.hdm /mnt/Lemmings`, but I haven't tried this yet.
