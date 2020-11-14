import struct
import collections

#  0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1| Byte
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | capture_pattern: Magic number for page start "OggS"           | 0-3
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | version       | header_type   | granule_position              | 4-7
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                                                               | 8-11
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                               | bitstream_serial_number       | 12-15
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                               | page_sequence_number          | 16-19
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                               | CRC_checksum                  | 20-23
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                               |page_segments  | segment_table | 24-27
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# | ...                                                           | 28-


PAGE_HEADER_SIZE = 27
page_header_format = lambda: "<4sBBQIIIB"
segment_table_format = lambda num_segments: f"<{num_segments}B"

PageHeader = collections.namedtuple(
    "PageHeader",
    (
        "capture_pattern "
        "version "
        "header_type "
        "granule_position "
        "bitstream_serial_number "
        "page_sequence_number "
        "checksum "
        "page_segments "
    )
)

def parse_page(buffer, offset):
    start = offset

    page_header = PageHeader._make(
        struct.unpack(
            page_header_format(), 
            buffer[offset : offset + PAGE_HEADER_SIZE]
        )
    )

    offset += PAGE_HEADER_SIZE

    segment_table = struct.unpack(
        segment_table_format(page_header.page_segments),
        buffer[offset : offset + page_header.page_segments]
    )

    offset += page_header.page_segments

    offset += sum(segment_table)

    return page_header.header_type, start, offset


def parse_file(buffer):
    offset = 0

    while offset < len(buffer):
        page = parse_page(buffer, offset)
        offset = page[2]
        print(page)



