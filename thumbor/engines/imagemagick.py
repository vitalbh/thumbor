#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from cStringIO import StringIO

from tornado.options import options

from thumbor.engines import BaseEngine
from thumbor.vendor.pythonmagickwand.image import Image
from thumbor.vendor.pythonmagickwand import wand

FORMATS = {
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.gif': 'GIF',
    '.png': 'PNG'
}

class Engine(BaseEngine):

    def reset_image(self):
        self.load(self.read(), self.extension)

    def create_image(self, buffer):
        return Image(StringIO(buffer))

    def resize(self, width, height):
        self.image.resize((int(width), int(height)), wand.CATROM_FILTER, 1)

    def crop(self, left, top, right, bottom):
        offset_left = left
        offset_top = top
        width = right - left
        height = bottom - top

        self.image.crop(
            (width, height),
            (offset_left, offset_top)
        )

        self.reset_image()

    def flip_vertically(self):
        self.image.flip()

    def flip_horizontally(self):
        self.image.flop()
        
    def watermark(self,mark,watermark_pos):
        return None
    
    def read(self, extension=None, quality=options.QUALITY):
        #returns image buffer in byte format.
        img_buffer = StringIO()

        ext = extension or self.extension
        self.image.format = FORMATS[ext]
        self.image.compression_quality = quality

        self.image.save(img_buffer)

        results = img_buffer.getvalue()
        img_buffer.close()

        return results
