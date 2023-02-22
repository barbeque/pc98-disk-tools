import os, sys
from struct import *
from fdi import *

def make_blank_fdi(output_fdi_path):
    header = make_fdi_header()
    blank_space = pack('1261568x')
    fdi_image = header + blank_space
    with open(output_fdi_path, 'wb') as o:
        o.write(fdi_image)
    print(f'Wrote {output_fdi_path}')

def make_blank_hdm(output_hdm_path):
    blank_image = pack('1261568x')
    with open(output_hdm_path, 'wb') as o:
        o.write(blank_image)
    print(f'Wrote {output_hdm_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} [output fdi, hdm floppy image file]', file=sys.stderr)
        sys.exit(1)
    else:
        for output_path in sys.argv[1:]:
            (path, ext) = os.path.splitext(output_path)
            match ext.replace('.', ''):
                case 'fdi':
                    make_blank_fdi(output_path)
                case 'hdm':
                    make_blank_hdm(output_path)
                case _:
                    print(f"Don't know how to generate an image of type '{ext}'.", file=sys.stderr)
                    sys.exit(1)
