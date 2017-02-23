"""
mercury particle engine main types
"""

from __future__ import print_function

from xnb_parse.xna_types.mercury.emitters import EmitterCollection


class ParticleEffect(EmitterCollection):
    def __init__(self, emitters, name, author, description):
        EmitterCollection.__init__(self, emitters)
        self.name = name
        self.author = author
        self.description = description

    def __repr__(self):
        return 'ParticleEffect(name={!r}, emitters={}, author={!r}, description={!r})'.format(
            self.name, self.emitters, self.author, self.description)
