CAPTURE_PATTERN = b"OggS"
CONTINUED_PACKET_FLAG = 0x01
BEGINNING_OF_STREAM_FLAG = 0x02
END_OF_STREAM_FLAG = 0x04


class OpusPage:

    def __init__(self, offset: int, length: int, packet_type: int):
        self.offset: int = offset
        self.length: int = length
        self.type: int = packet_type


    def __str__(self):
        return (
            "<OpusPage: "
            f"offset={self.offset}, "
            f"length={self.length}, "
            f"type={self.type}"
            ">"
        )
