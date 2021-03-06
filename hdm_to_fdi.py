from struct import *
import sys, os
import fdi

# MS-DOS disk formats:
# HDM -> 2HD/360rpm -> 1024 bytes * 8 sectors * 2 surfaces * 77 cyls = 1,261,568
# HD5 -> 2HD/360rpm -> 512 bytes * 15 sectors * 2 surfaces * 80 cyls = 1,228,800
# HD4 -> 2HD/300rpm -> 512 bytes * 18 sectors * 2 surfaces * 80 cyls = 1,474,560
# DD6 -> 2DD/300rpm -> 512 bytes * 8 sectors * 2 surfaces * 80 cyls = 655,360
# DD9 -> 2DD/360rpm -> 512 bytes * 9 sectors * 2 surfaces * 80 cyls = 737,280
# N88-BASIC disk formats:
# HDB -> 2HD/360rpm -> (128/256) bytes * 26 sectors * 2(?) surfaces * 77 cyls. First track single-density (128-bytes), latter tracks 256 byte double density
# DDB -> 2DD/300rpm -> 256 bytes * 16 sectors * 2 surfaces * 80 cyls

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
    print(f'Converting {hdm_file_path}')

    # sanity check to see if it is a different format of hdm
    (filename, extension) = os.path.splitext(hdm_file_path)
    extension = extension.lower()
    if extension == 'fdi':
        print(f'Image is already an FDI, aborting')
    # todo: load alternative ideal sizes, surfaces, cylinders for hdb, etc

    # first get file size
    size = os.path.getsize(hdm_file_path)
    if size != 1261568:
        print('Be careful, I was only tested with HDM (2HD) files of size 1261568')

    # load the entire file into a blob
    with open(hdm_file_path, 'rb') as i:
        hdm_blob = i.read()

    # prepare an fdi header that works
    dummy = 0
    fddtype = 144 # 144 = 0x90 = 1.2MB 2HD
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
    target_path = fdi.change_extension_of_path(hdm_file_path, '.fdi')

    with open(target_path, 'wb') as o:
        o.write(full_fdi_image)

    print(f'Completed write of {target_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} [hdm floppy image file]')
    else:
        for hdm_file in sys.argv[1:]:
            hdm_to_fdi(hdm_file)
