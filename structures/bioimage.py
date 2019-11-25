
class BioImage:

    def __init__(self):
        self.filepath = None
        self.layer = None
        self.channels = None
        self.c = None

        # STANDARD SETTINGS HERE
        self.debug = None
        self.series = 0
        self.setz = 0

        # META
        self.shape = (0, 0, 0)

        # DATA
        self.file = None
