from struct import *
import sys, os

def hdm_to_fdi(hdm_file_path):
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
    print 'Converting %s' % hdm_file_path

    # first get file size
    size = os.path.getsize(hdm_file_path)
    if size != 1261568:
        print 'Be careful, I was only tested with HDM (2HD) files of size 1261568'

    # load the entire file into a blob
    with open(hdm_file_path, 'rb') as i:
        hdm_blob = i.read()

    # prepare an fdi header that works
    dummy = 0
    fddtype = 144 # no idea what this means, just copied it from another fdi file that worked
    headersize = 4096
    fdd_size = size
    sector_size = 1024
    sector_count = 8
    surfaces = 2
    cylinders = 77
    fdi_header = pack('<8L4064x', dummy, fddtype, headersize, fdd_size, sector_size, sector_count, surfaces, cylinders)

    assert len(fdi_header) == headersize

    # now kiss
    full_fdi_image = fdi_header + hdm_blob

    # now write that puppy out
    destinationdir = os.path.dirname(hdm_file_path)
    filename = os.path.basename(hdm_file_path)
    (filename, extension) = os.path.splitext(filename)
    fdi_filename = filename + '.fdi'

    target_path = os.path.join(destinationdir, fdi_filename)

    with open(target_path, 'wb') as o:
        o.write(full_fdi_image)

    print 'Completed write of %s' % target_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: %s [hdm floppy image file]' % sys.argv[0]
    else:
        for hdm_file in sys.argv[1:]:
            hdm_to_fdi(hdm_file)
