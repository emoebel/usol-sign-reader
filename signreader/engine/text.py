import moondream as md
import numpy as np

class TextReader:
    def __init__(self):
        # Run on cloud:
        self.model = md.vl(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI0MDQ2ZDljNi1iNjA4LTQ2NmItODFiNS03NTc5YTJjOTUxMTQiLCJvcmdfaWQiOiJaQkZoUHNyNjJtQVRvSnpKa3c3TktCZGhieGNvelg1cyIsImlhdCI6MTc1MDE2OTIyMSwidmVyIjoxfQ.-WxqicYJ2XEvAKyhiEjxkgwdW1wRR64FFX4x_AmZvD0")
        # Run locally:
        #self.model = md.vl(endpoint="http://localhost:2020/v1") # when model is called I get: rllib.error.URLError: <urlopen error [Errno 61] Connection refused>

    def __call__(self, img):
        '''
        :param img: (pil img)
        :return: (list of dict) each list line corresponds to a line in the sign
        '''
        answer = self.model.query(img, "Give me the name of the destinations and their durations")['answer']
        # test: Transcribe the destinations and corresponding durations in natural reading order.

        # # Here we make the assumption that the answer looks like: 'Brüschrainhöchi: 30 min\nChili Tändli: 1 h 30 min\nEinsiedeln: 4 h'
        # answer_splitter = '\n'
        # if answer.find(answer_splitter) == -1:
        #     answer_splitter = ',' # sometimes  answer looks like: 'Brüschrainhöchi: 30 min, Chili Tändli: 1 h 30 min, Einsiedeln: 4 h'
        #
        # text_lines = answer.split(answer_splitter)
        # scontent = []  # sign content
        # for line in text_lines:
        #     destination, duration = line.split(':')
        #     scontent.append(
        #         {'destination': destination, 'duration': duration}
        #     )

        scontent = self.format_md_answer(answer)
        scontent = self.get_text_lines(img, scontent)

        return scontent

    def format_md_answer(self, answer):
        '''
        Formats Moondream answer to be used in the pipeline. Moondream's output is not always stable, so this function
        handles the cases I encountered.
        :param answer: (string) as outputed by Moondream
        :return: (list of dict) sign content
        '''
        # Here we make the assumption that the answer looks like: 'Brüschrainhöchi: 30 min\nChili Tändli: 1 h 30 min\nEinsiedeln: 4 h'
        answer_splitter = '\n'
        if answer.find(answer_splitter) == -1:
            answer_splitter = ','  # sometimes  answer looks like: 'Brüschrainhöchi: 30 min, Chili Tändli: 1 h 30 min, Einsiedeln: 4 h'

        text_lines = answer.split(answer_splitter)

        scontent = []  # sign content
        for line in text_lines:
            line_splitter = ':'
            if line.find(line_splitter) != -1:
                destination, duration = line.split(line_splitter)
                scontent.append(
                    {'destination': destination, 'duration': duration}
                )
            else:
                if any(char.isdigit() for char in line):  # if string contains any number, then it is a duration
                    scontent.append(
                        {'destination': None, 'duration': line}
                    )
                else:
                    scontent.append(
                        {'destination': line, 'duration': None}
                    )

        return scontent

    def get_text_lines(self, img, scontent):
        '''
        This method computes the coordinates of detected text. Allows to infer text lines, each line defined by (pos_dest, pos_dura)
        :param img: (pil img)
        :param scontent: (list of dict) input sign content
        :return: (list of dict) output sign content, with added line coordinates
        '''
        img_np = np.asarray(img)
        for idx_line, content in enumerate(scontent):

            lcontent = scontent[idx_line]  # line content

            # Find destination position:
            if lcontent['destination'] is not None:
                objects = self.model.detect(img, lcontent['destination'])['objects']
                if len(objects) > 1:
                    print(f"[TextReader] Line {idx_line}: found {len(objects)} destination instance(s)")
                x = (objects[0]['x_min'] + objects[0]['x_max']) / 2 * img_np.shape[1]
                y = (objects[0]['y_min'] + objects[0]['y_max']) / 2 * img_np.shape[0]
                content['pos_dest'] = (x, y)
            else:
                content['pos_dest'] = (None, None)

            # Find duration position:
            if lcontent['duration'] is not None:
                objects = self.model.detect(img, lcontent['duration'])['objects']
                if len(objects) > 1:
                    print(f"[TextReader] Line {idx_line}: found {len(objects)} duration instance(s)")
                x = (objects[0]['x_min'] + objects[0]['x_max']) / 2 * img_np.shape[1]
                y = (objects[0]['y_min'] + objects[0]['y_max']) / 2 * img_np.shape[0]
                content['pos_dura'] = (x, y)
            else:
                content['pos_dura'] = (None, None)

            scontent[idx_line] = content  # add position info in sign content

        return scontent