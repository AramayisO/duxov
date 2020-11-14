import io
import struct
import collections
from typing import List, Union

from app.opus.model import OpusPage, CAPTURE_PATTERN, CONTINUED_PACKET_FLAG

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
# | ...   

class OpusParser:

    __PageHeader = collections.namedtuple(
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
    __page_header_fmt = "<4sBBQIIIB"
    __page_header_size = struct.calcsize(__page_header_fmt)
    __segment_table_fmt = "<{page_segments}B"


    def __init__(self, buffer):
        self.__buffer = buffer
        self.__header_page: OpusPage = None
        self.__comment_page: OpusPage = None
        self.__audio_pages: List[OpusPage] = []
        self.__packet_iter = None
        self.__parse()


    def __parse_page(self, offset):
        start = offset

        header = self.__PageHeader._make(
            struct.unpack(
                self.__page_header_fmt,
                self.__buffer[offset : offset + self.__page_header_size]
            )
        )

        offset += self.__page_header_size

        if header.capture_pattern != CAPTURE_PATTERN:
            raise Error

        segment_table = struct.unpack(
            self.__segment_table_fmt.format(page_segments=header.page_segments),
            self.__buffer[offset : offset + header.page_segments]
        )

        offset += header.page_segments
        offset += sum(segment_table)

        return OpusPage(start, offset - start, header.header_type)


    def __parse(self):
        # The header page must always be the first page and the packet must
        # only span one page.
        self.__header_page = self.__parse_page(0)
        # The comment page must always start on the second page, but can span
        # multiple pages.
        self.__comment_page = self.__parse_page(self.__header_page.length)
    
        offset = self.__comment_page.offset + self.__comment_page.length
        page = self.__parse_page(offset)
    
        # We need to check if the comment packet spans multiple pages.
        while page.type & CONTINUED_PACKET_FLAG:
            self.__comment_page.length += page.length
            offset += page.length
            page = self.__parse_page(offset)

        self.__audio_pages.append(page)

        offset += page.length 

        while offset < len(self.__buffer):
            page = self.__parse_page(offset)
            self.__audio_pages.append(page)
            offset += page.length


    def __get_packet_iterator(self):
        index = 0
        num_pages = len(self.__audio_pages)
        packet_size = 10

        while index < num_pages:
            first_page = self.__audio_pages[index]
            last_page = self.__audio_pages[min(index + packet_size - 1, num_pages - 1)]
            index += packet_size
            packet = io.BytesIO()
            packet.write(self.__buffer[self.__header_page.offset : self.__header_page.offset + self.__header_page.length])
            packet.write(self.__buffer[self.__comment_page.offset : self.__comment_page.offset + self.__comment_page.length])
            packet.write(self.__buffer[first_page.offset : last_page.offset + last_page.length])
            packet.seek(0)
            yield packet


    def get_next_packet(self) -> Union[io.BytesIO, None]:
        try:
            packet = next(self.__packet_iter)
        except TypeError:
            self.__packet_iter = self.__get_packet_iterator()
            packet = next(self.__packet_iter)
        except StopIteration:
            packet = None

        return packet
