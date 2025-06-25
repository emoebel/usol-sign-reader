import moondream as md
import numpy as np


class TextReader:
    def __init__(self, print_flag=False):
        self.print = print_flag
        # Run on cloud:
        self.model = md.vl(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI0MDQ2ZDljNi1iNjA4LTQ2NmItODFiNS03NTc5YTJjOTUxMTQiLCJvcmdfaWQiOiJaQkZoUHNyNjJtQVRvSnpKa3c3TktCZGhieGNvelg1cyIsImlhdCI6MTc1MDE2OTIyMSwidmVyIjoxfQ.-WxqicYJ2XEvAKyhiEjxkgwdW1wRR64FFX4x_AmZvD0")
        # Run locally:
        #self.model = md.vl(endpoint="http://localhost:2020/v1") # when model is called I get: rllib.error.URLError: <urlopen error [Errno 61] Connection refused>

    def __call__(self, img_pil):
        '''
        :param img_pil: (PIL img)
        :return: (list of dict) each list line corresponds to a line in the sign
        '''
        query_destinations = 'Give me the destinations, line by line'
        answer_destinations = self.model.query(img_pil, query_destinations)['answer']

        query_durations = 'Give me the durations'
        answer_durations = self.model.query(img_pil, query_durations)['answer']
        if self.print:
            print('[TextReader] Destination answer:')
            print(answer_destinations)
            print('[TextReader] Durations answer:')
            print(answer_durations)

        scontent = self.format_md_answers(answer_destinations, answer_durations)
        scontent = self.get_text_line_positions(img_pil, scontent)
        scontent = self.format_duration_strings(scontent)

        return scontent

    def format_md_answers(self, answer_destinations, answer_durations):
        dest_str_list = self.split_md_answer_components(answer_destinations)
        dura_str_list = self.split_md_answer_components(answer_durations)
        dura_str_list = self.post_process_dura_str_list(dura_str_list)
        scontent = self.find_dest_dura_correspondence(dest_str_list, dura_str_list)
        scontent = self.remove_useless_prefix_from_destination_names(scontent)
        return scontent

    def split_md_answer_components(self, answer):
        answer_splitted = [answer] # initalisation: nothing to be splitted (happens when only 1 component)
        if answer.find('\n') > -1:
            answer_splitted = answer.split('\n')
        elif answer.find(',') > -1:
            answer_splitted = answer.split(',')
        elif answer.find('and') > -1:
            answer_splitted = answer.split('and')
        else:
            '[TextReader]: no string splitter found'
        return answer_splitted

    def find_dest_dura_correspondence(self, dest_str_list, dura_str_list):
        '''
        Later in the development, this function should have a smarter way of making dest-dura correspondence
        (by considering the positions in image), because sometimes len(dest_str_list)!=len(dura_str_list)
        '''
        scontent = []
        for idx, dest_str in enumerate(dest_str_list):
            if idx < len(dura_str_list):
                dura_str = dura_str_list[idx]
            else:
                dura_str = None
            scontent.append(
                {'destination': dest_str, 'duration': dura_str}
            )
        return scontent

    def remove_useless_prefix_from_destination_names(self, scontent):
        # Post-process the text:
        for idx, lcontent in enumerate(scontent):
            if lcontent['destination'] is not None:
                if lcontent['destination'].startswith('-'):
                    lcontent['destination'] = lcontent['destination'].removeprefix('-')
                if lcontent['destination'].startswith(' '):  # remove blanks
                    lcontent['destination'] = lcontent['destination'].removeprefix(' ')
            scontent[idx] = lcontent

        return scontent

    def format_duration_strings(self, scontent):
        for idx, lcontent in enumerate(scontent):
            if lcontent['duration'] is not None:
                dura_str = lcontent['duration']
                dura_dict = self.get_dura_dict_from_dura_string(dura_str)
            else:
                dura_dict = {'hours': None, 'minutes': None}
            scontent[idx]['duration'] = dura_dict
        return scontent

    def post_process_dura_str_list(self, dura_str_list):
        for idx, dura_str in enumerate(dura_str_list):
            if dura_str.find('and') > -1:  # sometime we have [' 15 minutes', ' 35 minutes', ' and 50 minutes']
                dura_str = dura_str.replace('and', '')
                dura_str_list[idx] = dura_str

        return dura_str_list

    def get_dura_dict_from_dura_string(self, dura_str):
        dura_dict = {'hours': None, 'minutes': None}

        if dura_str.find(':') > -1:  # '1:35 min'
            idx = dura_str.find(':')
            hours_str = dura_str[:idx]
            dura_dict['hours'] = int(hours_str)
            dura_str = dura_str.replace(hours_str + ':', '')

        if dura_str.find('hours') > -1:
            idx = dura_str.find('hours')
            hours_str = dura_str[:idx]
            dura_dict['hours'] = int(hours_str)
            dura_str = dura_str.replace(hours_str + 'hours', '')

        if dura_str.find('hour') > -1:
            idx = dura_str.find('hour')
            hours_str = dura_str[:idx]
            dura_dict['hours'] = int(hours_str)
            dura_str = dura_str.replace(hours_str + 'hour', '')

        if dura_str.find('minutes') > -1:
            idx = dura_str.find('minutes')
            minutes_str = dura_str[:idx]
            dura_dict['minutes'] = int(minutes_str)
            minutes_str = minutes_str.replace(minutes_str + 'minutes', '')

        if dura_str.find('h') > -1:
            idx = dura_str.find('h')
            hours_str = dura_str[:idx]
            dura_dict['hours'] = int(hours_str)
            dura_str = dura_str.replace(hours_str + 'h', '')

        if dura_str.find('min') > -1:
            idx = dura_str.find('min')
            minutes_str = dura_str[:idx]
            dura_dict['minutes'] = int(minutes_str)

        return dura_dict

    def get_text_line_positions(self, img, scontent):
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
                if self.print: print('[TextReader] lcontent[destination]: ' + lcontent['destination'])
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
                if self.print: print('[TextReader] lcontent[duration]: ' + lcontent['duration'])
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


class TextReaderOLD:
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
        print('[TextReader] answer:')
        print(answer)

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
        # Then, there is following case: 'The destinations are Ober Bettenalp, Stöckalp, and Stockalp. The durations are 45 minutes, 2 hours, and 15 minutes respectively.'
        if answer.find('The destinations are') != -1 and answer.find('The durations are') != -1:
            idx = answer.find('The durations are')
            destinations_str = answer[:idx]
            durations_str = answer[idx:]
            destinations_str = destinations_str.replace('The destinations are', '')
            durations_str = durations_str.replace('The durations are', '')
            if answer.find('respectively') != -1:
                durations_str = durations_str.replace('respectively', '')
            destinations_str_split = destinations_str.split(',')
            durations_str_split = durations_str.split(',')
            scontent = []
            for idx, dest in enumerate(destinations_str_split):
                scontent.append(
                    {'destination': dest, 'duration': durations_str_split[idx]}
                )

        else:
            # First, there is the case where answer looks like: 'The destinations and their durations are as follows:\n\n- Schnuer: 25 minutes\n- Tannalp: 40 minutes'
            # So we want to remove this prefix which does not contain useful information
            answer_prefix = 'The destinations and their durations are as follows:'
            if answer.startswith(answer_prefix):
                answer = answer.removeprefix(answer_prefix)
            while answer.startswith('\n'):
                answer = answer.removeprefix('\n')
            # Sometimes look like: 'The destinations and their durations are:\n\n- Schnuer: 25 minutes\n- Tannalp: 40 minutes'
            answer_prefix = 'The destinations and their durations are:'
            if answer.startswith(answer_prefix):
                answer = answer.removeprefix(answer_prefix)
            while answer.startswith('\n'):
                answer = answer.removeprefix('\n')

            # Now, let's find out how text is structured, and format it in consequence:
            # Sometimes the information is seprated by '\n', sometimes by ','
            answer_splitter = '\n'  # sometimes  answer looks like: 'Brüschrainhöchi: 30 min\n Chili Tändli: 1 h 30 min\n Einsiedeln: 4 h'
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

        # Post-process the text:
        for idx, lcontent in enumerate(scontent):
            if lcontent['destination'] is not None:
                if lcontent['destination'].startswith('-'):
                    lcontent['destination'] = lcontent['destination'].removeprefix('-')
                if lcontent['destination'].startswith(' '):  # remove blanks
                    lcontent['destination'] = lcontent['destination'].removeprefix(' ')
            if lcontent['duration'] is not None:
                if lcontent['duration'].startswith(' '):  # remove blanks
                    lcontent['duration'] = lcontent['duration'].removeprefix(' ')

            scontent[idx] = lcontent

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
                print('[TextReader] lcontent[destination]: ' + lcontent['destination'])
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
                print('[TextReader] lcontent[duration]: ' + lcontent['duration'])
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