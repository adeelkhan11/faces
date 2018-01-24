from . import bodypart
#from bodypart import bodypart.BodyPart
from PIL import Image


class ColourPart(bodypart.BodyPart):
    R_OLD, G_OLD, B_OLD = 0, 255, 0

    def __init__(self, group='16', part='mouth', dna_code='1', colour=(0, 0, 0), picfile=None):
        super().__init__(group=group, part=part, dna_code=dna_code, picfile=picfile)
        self.R_NEW, self.G_NEW, self.B_NEW = colour

    def draw(self, canvas, location=(0, 0)):
        image = Image.open(self.picfile)
        self.recolour(image)
        canvas.paste(image, location, mask=image)

    def recolour(self, image):
        width, height = image.size
        pixels = image.load()
        for x in range(width):
            for y in range(height):
                r, g, b, a = pixels[x, y]
                if (r, g, b) == (self.R_OLD, self.G_OLD, self.B_OLD):
                    pixels[x, y] = (self.R_NEW, self.G_NEW, self.B_NEW, a)