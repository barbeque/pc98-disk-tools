import sys
from struct import *

def make_blank_fdi(output_fdi_path):
    dummy = 0
    fddtype = 144 # no idea what this means, just copied it from another fdi file that worked
    headersize = 4096
    fdd_size = 1261568 # 2HD
    sector_size = 1024
    sector_count = 8
    surfaces = 2
    cylinders = 77
    fdi_image = pack('<8L4064x1261568x', dummy, fddtype, headersize, fdd_size, sector_size, sector_count, surfaces, cylinders)
    with open(output_fdi_path, 'wb') as o:
        o.write(fdi_image)
    print(f'Wrote {output_fdi_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} [output fdi floppy image file]')
    else:
        for fdi_file in sys.argv[1:]:
            make_blank_fdi(fdi_file)
