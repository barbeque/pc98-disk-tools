import sys, os
import fdi

HDM_IMAGE_SIZE = 1261568 # TODO: support more kinds later

def remove_fdi_header(fdi_file_path):
    with open(fdi_file_path, 'rb') as i:
        fdi_blob = i.read()

    hdm_slice = fdi_blob[4096:]

    assert len(hdm_slice) == HDM_IMAGE_SIZE, "Expected %i bytes, but got %i. Is this really an FDI? (try is_fdi.py)" % ( HDM_IMAGE_SIZE, len(hdm_slice) )

    target_path = fdi.change_extension_of_path(fdi_file_path, '.hdm')

    with open(target_path, 'wb') as o:
        o.write(hdm_slice)

    print(f'Completed write of {target_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} [fdi floppy image file]')
    else:
        for fdi_file in sys.argv[1:]:
            remove_fdi_header(fdi_file)
