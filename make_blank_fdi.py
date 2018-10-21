import sys
from struct import *
from fdi import *

def make_blank_fdi(output_fdi_path):
    header = make_fdi_header()
    blank_space = pack('1261568x')
    fdi_image = header + blank_space
    with open(output_fdi_path, 'wb') as o:
        o.write(fdi_image)
    print(f'Wrote {output_fdi_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} [output fdi floppy image file]')
    else:
        for fdi_file in sys.argv[1:]:
            make_blank_fdi(fdi_file)
