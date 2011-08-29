import urllib2
from PIL import ImageFile,Image,ImageEnhance

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

def makeWaterMark(im,water,watermark_pos):
    
    response = urllib2.urlopen(water)
    water = response.read()
    parser = ImageFile.Parser()
    parser.feed(water)
    mark = parser.close()
    
    pos = (0,0)
    if watermark_pos == 'tc': 
        pos = ((im.size[0]/2) - (mark.size[0]/2),0)
    elif watermark_pos == 'tr':
        pos = (im.size[0]-mark.size[0],0)
    elif watermark_pos == 'cl':
        pos = (0, (im.size[1]/2) - (mark.size[1]/2) )
    elif watermark_pos == 'cc':
        pos = ( (im.size[0]/2) - (mark.size[0]/2), (im.size[1]/2) - (mark.size[1]/2) )
    elif watermark_pos == 'cr':
        pos = (im.size[0]-mark.size[0],(im.size[1]/2) - (mark.size[1]/2))
    elif watermark_pos == 'bl':
        pos = (0,im.size[1]-mark.size[1])    
    elif watermark_pos == 'bc':
        pos = ((im.size[0]/2) - (mark.size[0]/2),im.size[1]-mark.size[1])    
    elif watermark_pos == 'br':
        pos = (im.size[0]-mark.size[0],im.size[1]-mark.size[1])    
    
    im = watermark(im,mark,pos,1)
    return im
 