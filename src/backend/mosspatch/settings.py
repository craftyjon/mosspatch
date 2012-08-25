import ConfigParser


class MosspatchConfig:

    def __init__(self):
        self.cp = ConfigParser.ConfigParser()
        self.config = self.cp.read("data/mosspatch.ini")

        for section in self.cp.sections():
            print section
            for option in self.cp.options(section):
                print " ", option, "=", self.cp.get(section, option)

    def get(self, section, option):
        return self.cp.get(section, option)
