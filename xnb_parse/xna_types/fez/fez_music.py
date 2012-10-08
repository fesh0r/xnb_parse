"""
FEZ music types
"""

from xnb_parse.xna_types.xna_primitive import Enum


class ShardNotes(Enum):
    enum_values = dict(enumerate(['C2', 'Csharp2', 'D2', 'Dsharp2', 'E2', 'F2', 'Fsharp2', 'G2', 'Gsharp2', 'A2',
                                  'Asharp2', 'B2', 'C3', 'Csharp3', 'D3', 'Dsharp3', 'E3', 'F3', 'Fsharp3', 'G3',
                                  'Gsharp3', 'A3', 'Asharp3', 'B3', 'C4']))


class AssembleChords(Enum):
    enum_values = dict(enumerate(['C_maj', 'Csharp_maj', 'D_maj', 'Dsharp_maj', 'E_maj', 'F_maj', 'Fsharp_maj', 'G_maj',
                                  'Gsharp_maj', 'A_maj', 'Asharp_maj', 'B_maj']))
