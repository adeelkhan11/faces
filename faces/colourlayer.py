from . import layer
#from bodypart import bodypart.BodyPart
from PIL import Image


class ColourLayer(layer.Layer):
    SCREEN_COLOUR = (0, 255, 0)

    def __init__(self, group='16', part='mouth', genders=[''], colours=[(0, 0, 0)]):
        super().__init__(group=group, part=part, genders=genders)

        colour_images = dict()
        for dna_code, image in self.images.items():
            for colour_code, colour in enumerate(colours):
                colour_image = image.copy()
                if ColourLayer.recolour(colour_image, colour):
                    colour_images['{}.{}'.format(dna_code, colour_code)] = colour_image
                else:
                    colour_images['{}'.format(dna_code)] = colour_image

        self.dna_codes = colour_images.keys()
        self.images = colour_images

    @classmethod
    def recolour(cls, image, colour):
        recoloured = False
        width, height = image.size
        pixels = image.load()
        for x in range(width):
            for y in range(height):
                r, g, b, a = pixels[x, y]
                if (r, g, b) == cls.SCREEN_COLOUR:
                    pixels[x, y] = colour + (a, )
                    recoloured = True
        return recoloured