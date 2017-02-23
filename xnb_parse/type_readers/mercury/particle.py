"""
mercury particle engine main type readers
"""

from __future__ import print_function

from xnb_parse.type_reader import TypeReaderPlugin
from xnb_parse.type_readers.mercury.emitters import EmitterCollectionReader
from xnb_parse.type_readers.xna_primitive import StringReader
from xnb_parse.xna_types.mercury.particle import ParticleEffect


class ParticleEffectReader(EmitterCollectionReader, TypeReaderPlugin):
    target_type = 'ProjectMercury.ParticleEffect'
    reader_name = 'Microsoft.Xna.Framework.Content.ReflectiveReader`1[ProjectMercury.ParticleEffect]'

    def read(self):
        emitters = EmitterCollectionReader.read(self).emitters
        name = self.stream.read_object(StringReader)
        author = self.stream.read_object(StringReader)
        description = self.stream.read_object(StringReader)
        return ParticleEffect(emitters, name, author, description)
