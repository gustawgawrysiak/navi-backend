from flask_ipfilter import Whitelist as Wl


class Whitelist(Wl):

    def __init__(self):
        super().__init__()

    def import_from_file(self, filename: str) -> None:
        with open(filename, 'r') as file:
            for line in file.readlines():
                self.permitted_hosts.append(line)
