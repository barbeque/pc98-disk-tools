from struct import *
import sys, os, inspect
# extract exe header
def extract_exe_header(exe_path):
    print(f'decoding {exe_path}')
    with open(exe_path, 'rb') as i:
        whole_exe = i.read() # inefficient, we only really need the first page...
        print(f'file length = {len(whole_exe)}')
        signature, \
                last_page_bytes, \
                relocation_table_count, \
                header_size, \
                minimum_memory, \
                maximum_memory, \
                stack_offset, \
                initial_sp, \
                checksum, \
                initial_ip, \
                cs_offset, \
                reloc_offset, \
                overlay_number = unpack('<13H', whole_exe[:26])
        if signature != 23117: # 'MZ'
            print(f'Signature does not make sense. (Got {signature.to_bytes(2, "little")}).')
        print(f"last page bytes = '{last_page_bytes}'")
        print(f"reloc. table count = '{relocation_table_count}'")
        print(f"header size = '{header_size}'")
        print(f"min. memory = '{minimum_memory}'")
        print(f"max. memory = '{maximum_memory}'")
        print(f"stack offset = '0x{ '%02x' % stack_offset}'")
        print(f"initial SP = '0x{'%02x' % initial_sp}'")
        print(f"checksum = '{checksum}'")
        print(f"CS offset = '0x{'%02x' % cs_offset}'")
        print(f"reloc. offset = '0x{'%02x' % reloc_offset}'")
        print(f"overlay number = '0x{'%02x' % overlay_number}'")

        if checksum == 184:
            print(f"Checksum is probably BS")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            extract_exe_header(file)
    else:
        print(f'Usage: {sys.argv[0]} files...')
