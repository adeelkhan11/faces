from . import bodypart
#from bodypart import bodypart.BodyPart
#from colourpart import colourpart.ColourPart
from . import colourpart
from PIL import Image
import random

class Face:
    SKIN_COLOURS = [(255, 204, 153),
                    (191, 149, 94),
                    (128, 99, 62)]
    HAIR_COLOURS = [(0, 0, 0),
                    (100, 50, 0),
                    (200, 50, 0),
                    (220, 200, 0)]
    EYE_COLOURS = [(100, 50, 0),
                   (0, 100, 240),
                   (0, 180, 70),
                   (0, 0, 0)]
    GLASSES_COLOURS = [(0, 0, 0),
                   (150, 50, 200),
                   (200, 0, 0),
                   (0, 0, 200)]
    def __init__(self, group, dna):
        self.group = group
        self.dna = dna

    @staticmethod
    def makeDnaKey(dna):
        gender, head, eye, eye_colour, mouth, beard, hair, hair_colour, glasses, glasses_colour = self.dna.split('-')
        return '-'.join([gender, head, eye, mouth, beard, hair, hair_colour, glasses])

    @staticmethod
    def makeDna(gender, head, eye, eye_colour, mouth, beard, hair, hair_colour, glasses, glasses_colour):
        return '-'.join([gender, head, eye, eye_colour, mouth, beard, hair, hair_colour, glasses, glasses_colour])

    def draw(self, canvas, location=(0,0)):
        # dna
        # gender
        # head number
        # eye type and colour
        # eye colour
        # mouth type
        # facial hair type
        # hair type
        # hair colour
        # glasses
        # glasses colour
        gender, head, eye, eye_colour, mouth, beard, hair, hair_colour, glasses, glasses_colour = self.dna.split('-')

        bodypart.BodyPart(group=self.group, part='head', dna_code=head).draw(canvas, location)
        colourpart.ColourPart(group=self.group, part='eye', dna_code=eye, colour=self.EYE_COLOURS[int(eye_colour)]).draw(canvas, location)
        bodypart.BodyPart(group=self.group, part='mouth', dna_code=mouth).draw(canvas, location)
        colourpart.ColourPart(group=self.group, part='beard', dna_code=beard, colour=self.HAIR_COLOURS[int(hair_colour)]).draw(canvas, location)
        colourpart.ColourPart(group=self.group, part='hair', dna_code=hair, colour=self.HAIR_COLOURS[int(hair_colour)]).draw(canvas, location)
        colourpart.ColourPart(group=self.group, part='glasses', dna_code=glasses, colour=self.GLASSES_COLOURS[int(glasses_colour)]).draw(canvas, location)

    @classmethod
    def randomFace(cls, group):
        gender = random.choice('mf')
        head = random.choice(bodypart.BodyPart.allDnaCodes(group, 'head', gender=gender))
        eye = random.choice(bodypart.BodyPart.allDnaCodes(group, 'eye'))
        mouth = random.choice(bodypart.BodyPart.allDnaCodes(group, 'mouth', gender=gender))
        beard = random.choice(bodypart.BodyPart.allDnaCodes(group, 'beard', gender=gender))
        hair = random.choice(bodypart.BodyPart.allDnaCodes(group, 'hair', gender=gender))
        hair_colour = str(random.randint(0, 3))
        glasses = random.choice(bodypart.BodyPart.allDnaCodes(group, 'glasses', gender=gender))
        eye_colour = str(random.randint(0, 3))
        glasses_colour = str(random.randint(0, 3))
        dna = '-'.join([gender, head, eye, eye_colour, mouth, beard, hair, hair_colour, glasses, glasses_colour])
        return cls(group, dna)


    @classmethod
    def allFaces(cls, group, gender):
        heads = bodypart.BodyPart.allDnaCodes(group, 'head', gender=gender)
        eyes = bodypart.BodyPart.allDnaCodes(group, 'eye')
        mouths = bodypart.BodyPart.allDnaCodes(group, 'mouth', gender=gender)
        beards = bodypart.BodyPart.allDnaCodes(group, 'beard', gender=gender)
        hairs = bodypart.BodyPart.allDnaCodes(group, 'hair', gender=gender)
        glasseses = bodypart.BodyPart.allDnaCodes(group, 'glasses', gender=gender)
        hair_colours = [str(i) for i in range(len(cls.HAIR_COLOURS))]

        result = list()
        for head in heads:
            for eye in eyes:
                for mouth in mouths:
                    for beard in beards:
                        for hair in hairs:
                            for glasses in glasseses:
                                for hair_colour in hair_colours:
                                    eye_colour = str(random.randint(0, len(cls.EYE_COLOURS) - 1))
                                    glasses_colour = str(random.randint(0, len(cls.GLASSES_COLOURS) - 1))
                                    result.append(Face.makeDna(gender, head, eye, eye_colour, mouth, beard, hair, hair_colour, glasses, glasses_colour))

        print(result)
        return result

    @classmethod
    def fillRandomGrid(cls, group='32', grid_width=5, grid_height=5, horizontal_spacing=40, vertical_spacing=40):
        male_faces = Face.allFaces(group, 'm')
        female_faces = Face.allFaces(group, 'f')
        faces = male_faces + female_faces
        random.shuffle(faces)
        print("{} male faces and {} female faces.".format(len(male_faces), len(female_faces)))
        width, height = horizontal_spacing * grid_width, vertical_spacing * grid_height
        canvas = Image.new("RGBA", (width, height))
        for i in range(grid_width):
            for j in range(grid_height):
                # face = Face.randomFace('16')
                face = cls(group, faces[j * grid_width + i])
                face.draw(canvas, ((i * horizontal_spacing) + 4, (j * vertical_spacing) + 4))
        new_width, new_height = width * 4, height * 4
        resized_canvas = canvas.resize((new_width, new_height))

        canvas.save('faces/images/output/output_{}_{}x{}.png'.format(group, grid_width, grid_height))
        resized_canvas.save('faces/images/output/output_{}_{}x{}-large.png'.format(group, grid_width, grid_height))


