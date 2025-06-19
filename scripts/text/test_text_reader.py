import moondream as md
from PIL import Image


class TextReader:
    def __init__(self):
        self.model = md.vl(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI0MDQ2ZDljNi1iNjA4LTQ2NmItODFiNS03NTc5YTJjOTUxMTQiLCJvcmdfaWQiOiJaQkZoUHNyNjJtQVRvSnpKa3c3TktCZGhieGNvelg1cyIsImlhdCI6MTc1MDE2OTIyMSwidmVyIjoxfQ.-WxqicYJ2XEvAKyhiEjxkgwdW1wRR64FFX4x_AmZvD0")

    def __call__(self, img):
        '''

        :param img: (pil img)
        :return: (list of dict) each list line corresponds to a line in the sign
        '''
        answer = self.model.query(img, "Give me the name of the destinations and their durations")['answer']

        # Here we make the assumption that the answer looks like: ' Brüschrainhöchi: 30 min\nChili Tändli: 1 h 30 min\nEinsiedeln: 4 h'
        text_lines = answer.split('\n')
        scontent = []  # sign content
        for line in text_lines:
            destination, duration = line.split(':')
            scontent.append(
                {'destination': destination, 'duration': duration}
            )

        return scontent

# Load your image
img = Image.open('/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_3.png')
#img = io.open_img_as_np_array('/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_3.png')
#img = Image.open('/Users/manu/boulot/unit_solutions/diapos/arbeitsplan/images/isolate_2.png')

treader = TextReader()
scontent = treader(img)