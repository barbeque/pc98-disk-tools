import sys, os
import fdi

def remove_hdi_header(hdi_file_path):
    with open(hdi_file_path, 'rb') as i:
        hdi_blob = i.read()

    assert len(hdi_blob) > 4096, "Expected at least 4096 bytes, but got %i. Is this really an HDI?" % ( len(hdi_blob) )

    flat_slice = hdi_blob[4096:]
    assert len(flat_slice) + 4096 == len(hdi_blob)

    # Maybe this should be a warning instead of a hard assert
    assert len(flat_slice) % 512 == 0, "Expected the resulting disk image to be a multiple of 512 bytes long, but got a length of %i instead." % len(flat_slice)

    if flat_slice[0] != 0xeb:
        fdi.warn("Disk may not be bootable ($eb missing from first byte)")

    # not sure if IMG is an accurate target format,
    # i am not clear on how HDI is formatted inside. Maybe HDN:
    #   https://github.com/AZO234/NP2kai/blob/2ca8e7ebc4e56c006aee38312782069fccbd910e/fdd/newdisk.c#L401
    target_path = fdi.change_extension_of_path(hdi_file_path, '.img')

    with open(target_path, 'wb') as o:
        o.write(flat_slice)

    print(f'Completed write of {target_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} [hdi hard disk image file]')
    else:
        for hdi_file in sys.argv[1:]:
            remove_hdi_header(hdi_file)
