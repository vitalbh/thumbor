#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import re, os

from thumbor.engines import watermark

class test_WaterMark():

    img  = 'fixture/img/img_to_watermark.jpg'
    mark = 'fixture/img/watermark.png'
    position = (100, 100)
    resPath = 'fixture/img/watermark_result.jpg'
    def test_watermark_filter( self ):
        
        res  = watermark.watermark( img, mark, position )
        res.save( resPath )
        
    def test_watermark_opacity( self ):
    
        res  = watermark.watermark( self.img, self.mark, self.position, 0.7 )
        res.save( resPath )
    
    
    def test_make_watermark( self ):
        
        markPositions = ['lt', 'ct', 'rt', 'lc', 'cc', 'rc', 'lb', 'cb', 'rb']
        os.mkdir('fixture/img/watermark_result')
        
        for i in markPosition:
            im = makeWaterMark( self.img, self.mark, i )
            im.save( self.resPath + '_' + i + '.jpg')
        
    def test_clean ( self ):
        os.remove( resPath )
        os.rmdir('fixture/img/watermark_result')
        
        