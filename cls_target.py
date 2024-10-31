class Target:
    """A sample Employee class"""

    def __init__(self, name, ra, dec):
        self.name = name
        self.ra = ra
        self.dec = dec

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.ra, self.dec)

    @property
    def fullname(self):
        return '{} {}'.format(self.ra, self.dec)

    def __repr__(self):
        return "Target('{}', '{}', {})".format(self.name, self.ra, self.dec)