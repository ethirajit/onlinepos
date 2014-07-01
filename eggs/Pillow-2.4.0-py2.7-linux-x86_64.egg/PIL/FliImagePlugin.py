#
# The Python Imaging Library.
# $Id$
#
# FLI/FLC file handling.
#
# History:
#       95-09-01 fl     Created
#       97-01-03 fl     Fixed parser, setup decoder tile
#       98-07-15 fl     Renamed offset attribute to avoid name clash
#
# Copyright (c) Secret Labs AB 1997-98.
# Copyright (c) Fredrik Lundh 1995-97.
#
# See the README file for information on usage and redistribution.
#


__version__ = "0.2"

from PIL import Image, ImageFile, ImagePalette, _binary

i8 = _binary.i8
i16 = _binary.i16le
i32 = _binary.i32le
o8 = _binary.o8

#
# decoder

def _accept(prefix):
    return i16(prefix[4:6]) in [0xAF11, 0xAF12]

##
# Image plugin for the FLI/FLC animation format.  Use the <b>seek</b>
# method to load individual frames.

class FliImageFile(ImageFile.ImageFile):

    format = "FLI"
    format_description = "Autodesk FLI/FLC Animation"

    def _open(self):

        # HEAD
        s = self.fp.read(128)
        magic = i16(s[4:6])
        if not (magic in [0xAF11, 0xAF12] and
                i16(s[14:16]) in [0, 3] and  # flags
                s[20:22] == b"\x00\x00"): # reserved
            raise SyntaxError("not an FLI/FLC file")

        # image characteristics
        self.mode = "P"
        self.size = i16(s[8:10]), i16(s[10:12])

        # animation speed
        duration = i32(s[16:20])
        if magic == 0xAF11:
            duration = (duration * 1000) / 70
        self.info["duration"] = duration

        # look for palette
        palette = [(a,a,a) for a in range(256)]

        s = self.fp.read(16)

        self.__offset = 128

        if i16(s[4:6]) == 0xF100:
            # prefix chunk; ignore it
            self.__offset = self.__offset + i32(s)
            s = self.fp.read(16)

        if i16(s[4:6]) == 0xF1FA:
            # look for palette chunk
            s = self.fp.read(6)
            if i16(s[4:6]) == 11:
                self._palette(palette, 2)
            elif i16(s[4:6]) == 4:
                self._palette(palette, 0)

        palette = [o8(r)+o8(g)+o8(b) for (r,g,b) in palette]
        self.palette = ImagePalette.raw("RGB", b"".join(palette))

        # set things up to decode first frame
        self.frame = -1
        self.__fp = self.fp

        self.seek(0)

    def _palette(self, palette, shift):
        # load palette

        i = 0
        for e in range(i16(self.fp.read(2))):
            s = self.fp.read(2)
            i = i + i8(s[0])
            n = i8(s[1])
            if n == 0:
                n = 256
            s = self.fp.read(n * 3)
            for n in range(0, len(s), 3):
                r = i8(s[n]) << shift
                g = i8(s[n+1]) << shift
                b = i8(s[n+2]) << shift
                palette[i] = (r, g, b)
                i = i + 1

    def seek(self, frame):

        if frame != self.frame + 1:
            raise ValueError("cannot seek to frame %d" % frame)
        self.frame = frame

        # move to next frame
        self.fp = self.__fp
        self.fp.seek(self.__offset)

        s = self.fp.read(4)
        if not s:
            raise EOFError

        framesize = i32(s)

        self.decodermaxblock = framesize
        self.tile = [("fli", (0,0)+self.size, self.__offset, None)]

        self.__offset = self.__offset + framesize

    def tell(self):

        return self.frame

#
# registry

Image.register_open("FLI", FliImageFile, _accept)

Image.register_extension("FLI", ".fli")
Image.register_extension("FLI", ".flc")
