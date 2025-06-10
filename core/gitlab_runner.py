class GitlabRunner:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.status = "stopped"

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "status": self.status
        }
    
    def is_starting(self):
        self.status = "starting"

    def is_on(self):
        self.status = "on"

    def is_off(self):
        self.status = "off"