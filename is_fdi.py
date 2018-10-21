from struct import *
import sys, os

def is_fdi(image_file_path):
    """
    typedef struct {
        BYTE   dummy[4];
        BYTE   fddtype[4];
        BYTE   headersize[4];
        BYTE   fddsize[4];
        BYTE   sectorsize[4];
        BYTE   sectors[4];
        BYTE   surfaces[4];
        BYTE   cylinders[4];
    } FDIHDR;
    intel dwords - little endian
    """
    size = os.path.getsize(image_file_path)
    with open(image_file_path, 'rb') as f:
        raw_header = f.read(32)
        dummy, fddtype, headersize, fddsize, sectorsize, sectors, surfaces, cylinders = unpack('<8L', raw_header)
        print('dummy = %d' % dummy)
        print('fddtype = %d' % fddtype)
        print('header size = %d' % headersize)
        print('fdd size = %d' % fddsize)
        print('sector size = %d' % sectorsize)
        print('sectors = %d' % sectors)
        print('surfaces = %d' % surfaces)
        print('cylinders = %d' % cylinders)

        if dummy != 0:
            # this seems like a pretty good indicator, empirically
            return (False, 'Dummy out of bounds: %d' % dummy)
        if cylinders > 100:
            return (False, 'Ridiculous cylinder count: %d' % cylinders)
        if size > 1265664:
            return (False, 'Too big to be an FDI: %d' % size)

        # look for suspicious pad bytes

        return (True, '')

if __name__ == '__main__':
    # work as a command-line utility to analyze multiple maybe-FDI images
    if len(sys.argv) < 2:
        print('Usage: %s [disk images]' % sys.argv[0])
    for arg in sys.argv[1:]:
        (result, why) = is_fdi(arg)
        if not result:
            print('%s: no (%s)' % (arg, why))
        else:
            print('%s: yes' % arg)
