from struct import *

def make_fdi_header(dummy=0,
                    fddtype=144,
                    headersize=4096,
                    fdd_size=1261568, # 2HD
                    sector_size=1024,
                    sector_count=8,
                    surfaces=2,
                    cylinders=77):
    return pack("<8L4064x", dummy, fddtype, headersize, fdd_size, sector_size, sector_count, surfaces, cylinders)

# TODO: unpack_fdi_header
