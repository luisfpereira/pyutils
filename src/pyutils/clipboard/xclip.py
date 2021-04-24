import os


class XclipCommand:
    '''
    Copies image to clipboard through `xclip`.
    '''

    def __init__(self):
        self.cmd = 'xclip -selection clipboard -t image/{} -i {}'

    def get_cmd(self, image_name):
        _, file_extension = os.path.splitext(image_name)

        return self.cmd.format(file_extension.lower()[1:], image_name)
