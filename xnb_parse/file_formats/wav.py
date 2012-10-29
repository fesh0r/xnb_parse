"""
WAV file writer
"""

from uuid import UUID

from xnb_parse.type_reader import ReaderError
from xnb_parse.binstream import BinaryWriter, BinaryReader


WAVE_FORMAT_WMAUDIO2 = 0x161
WAVE_FORMAT_WMAUDIO3 = 0x162
WAVE_FORMAT_XMA2 = 0x166
WAVE_FORMAT_EXTENSIBLE = 0xFFFE
WAVE_FORMAT = {
    0x0000: 'WAVE_FORMAT_UNKNOWN',
    0x0001: 'WAVE_FORMAT_PCM',
    0x0161: 'WAVE_FORMAT_WMAUDIO2',
    0x0162: 'WAVE_FORMAT_WMAUDIO3',
    0x0165: 'WAVE_FORMAT_XMA',
    0x0166: 'WAVE_FORMAT_XMA2',
    0xFFFE: 'WAVE_FORMAT_EXTENSIBLE',
    0xFFFF: 'WAVE_FORMAT_DEVELOPMENT',
}


class PyWavWriter(object):
    _waveformatex = 'H H I I H H'
    _waveformat_xma2 = 'H I I I I I I I B B H'
    _waveformat_extensible = 'H I 16s'

    def __init__(self, header, data, dpds=None, seek=None, needs_swap=False):
        self.header_raw = header
        self.data_raw = data
        self.dpds_raw = dpds
        self.seek_raw = seek
        self.needs_swap = needs_swap

        h_s = BinaryReader(self.header_raw, needs_swap)
        waveformatex_size = h_s.calc_size(self._waveformatex)
        (self.h_format_tag, self.h_channels, self.h_samples_per_sec, self.h_avg_bytes_per_sec, self.h_block_align,
         self.h_bits_per_sample) = h_s.unpack(self._waveformatex)
        header_size = waveformatex_size

        # do we have an WAVEFORMATEX
        self.h_size = None
        if len(self.header_raw) >= waveformatex_size + 2:
            self.h_size = h_s.read_uint16()
            header_size += 2

            if self.h_format_tag == WAVE_FORMAT_XMA2:
                waveformat_xma2_size = h_s.calc_size(self._waveformat_xma2)
                if self.h_size != waveformat_xma2_size:
                    raise ReaderError("Unknown cbSize for XMA2WAVEFORMATEX: %d" % self.h_size)
                (self.hx_num_streams, self.hx_channel_mask, self.hx_samples_encoded, self.hx_bytes_per_block,
                 self.hx_play_begin, self.hx_play_length, self.hx_loop_begin, self.hx_loop_length, self.hx_loop_count,
                 self.hx_encoder_version, self.hx_block_count) = h_s.unpack(self._waveformat_xma2)
                header_size += waveformat_xma2_size
            elif self.h_format_tag == WAVE_FORMAT_EXTENSIBLE:
                waveformat_extensible_size = h_s.calc_size(self._waveformat_extensible)
                if self.h_size < waveformat_extensible_size:
                    raise ReaderError("Invalid cbSize for WAVEFORMATEXTENSIBLE: %d", self.h_size)
                (self.he_valid_bits_per_sample, self.he_channel_mask,
                 he_subformat_bytes) = h_s.unpack(self._waveformat_extensible)
                self.he_subformat = UUID(bytes_le=he_subformat_bytes)
                header_size += waveformat_extensible_size
                self.he_remainder = None
                if self.h_size > waveformat_extensible_size:
                    self.he_remainder = h_s.read_bytes(self.h_size - waveformat_extensible_size)
                    header_size += self.h_size - waveformat_extensible_size
                    raise ReaderError("Extra bytes in WAVEFORMATEXTENSIBLE: %d", h_s.remaining)
            self.h_remainder = None
            if h_s.remaining():
                self.h_remainder = h_s.remainder()
                header_size += len(self.h_remainder)
                raise ReaderError("Trailing bytes in header: %d", len(self.h_remainder))
        if header_size != len(self.header_raw):
            raise ReaderError("Header size mismatch: %d != %d" % (header_size, len(self.header_raw)))

    def dump(self):
        if self.needs_swap:
            out_str = 'RIFX '
        else:
            out_str = 'RIFF '
        out_str += 'h:%d d:%d %s\n' % (len(self.header_raw), len(self.data_raw),
                                       WAVE_FORMAT.get(self.h_format_tag, 'UNKNOWN'))
        out_str += 'wFormatTag:0x%04x nChannels:%d nSamplesPerSec:%d nAvgBytesPerSec:%d\n' % (
            self.h_format_tag, self.h_channels, self.h_avg_bytes_per_sec, self.h_samples_per_sec)
        out_str += 'nBlockAlign:%d wBitsPerSample:%d cbSize:%d\n' % (
            self.h_block_align, self.h_bits_per_sample, self.h_size)
        if self.h_format_tag == WAVE_FORMAT_XMA2:
            out_str += 'NumStreams:%d ChannelMask:%08x SamplesEncoded:%d BytesPerBlock:%d\n' % (
                self.hx_num_streams, self.hx_channel_mask, self.hx_samples_encoded, self.hx_play_begin)
            out_str += 'PlayBegin:%d PlayLength:%d LoopBegin:%d LoopLength:%d\n' % (
                self.hx_play_begin, self.hx_play_length, self.hx_loop_begin, self.hx_loop_length)
            out_str += 'LoopCount:%d EncoderVersion:%d BlockCount:%d\n' % (
                self.hx_loop_count, self.hx_encoder_version, self.hx_block_count)
        elif self.h_format_tag == WAVE_FORMAT_EXTENSIBLE:
            out_str += 'wValidBitsPerSample:%d dwChannelMask:%08x\n' % (
                self.he_valid_bits_per_sample, self.he_channel_mask)
        print out_str

    def write(self, filename):
        h_s = BinaryWriter()
        h_s.pack(self._waveformatex, self.h_format_tag, self.h_channels, self.h_samples_per_sec,
                 self.h_avg_bytes_per_sec, self.h_block_align, self.h_bits_per_sample)
        if self.h_size is not None:
            h_s.write_uint16(self.h_size)
            if self.h_format_tag == WAVE_FORMAT_XMA2:
                # hack so mono sounds end up center rather than left
                if self.h_channels == 1 and self.hx_channel_mask == 1:
                    hx_channel_mask = 0
                else:
                    hx_channel_mask = self.hx_channel_mask
                h_s.pack(self._waveformat_xma2, self.hx_num_streams, hx_channel_mask, self.hx_samples_encoded,
                         self.hx_bytes_per_block, self.hx_play_begin, self.hx_play_length, self.hx_loop_begin,
                         self.hx_loop_length, self.hx_loop_count, self.hx_encoder_version, self.hx_block_count)
            elif self.h_format_tag == WAVE_FORMAT_EXTENSIBLE:
                h_s.pack(self._waveformat_extensible, self.he_valid_bits_per_sample, self.he_channel_mask,
                         self.he_subformat.bytes_le)
                if self.he_remainder:
                    h_s.write_bytes(self.he_remainder)
            if self.h_remainder:
                h_s.write_bytes(self.h_remainder)
        header_raw = h_s.serial()
        if self.dpds_raw:
            dpds_size = len(self.dpds_raw)
        else:
            dpds_size = None
        if self.seek_raw:
            seek_size = len(self.seek_raw)
        else:
            seek_size = None
        o_s = BinaryWriter()
        if self.h_format_tag == WAVE_FORMAT_WMAUDIO2 or self.h_format_tag == WAVE_FORMAT_WMAUDIO3:
            riff_type = 'XWMA'
        else:
            riff_type = 'WAVE'
        self.write_header(o_s, riff_type, len(header_raw), len(self.data_raw), dpds_size, seek_size)
        self.write_chunk(o_s, 'fmt ', header_raw)
        if self.dpds_raw:
            self.write_chunk(o_s, 'dpds', self.dpds_raw)
        if self.seek_raw:
            self.write_chunk(o_s, 'seek', self.seek_raw)
        self.write_chunk(o_s, 'data', self.data_raw)
        wav_data = o_s.serial()
        if self.h_format_tag == WAVE_FORMAT_XMA2:
            full_filename = filename + '.xma'
        elif self.h_format_tag == WAVE_FORMAT_WMAUDIO2 or self.h_format_tag == WAVE_FORMAT_WMAUDIO2:
            full_filename = filename + '.xwma'
        else:
            full_filename = filename + '.wav'
        with open(full_filename, 'wb') as out_file:
            out_file.write(wav_data)

    @staticmethod
    def write_header(o_s, riff_type, header_size, data_size, dpds_size=None, seek_size=None):
        full_size = 4 + 8 + header_size + 8 + data_size
        if dpds_size:
            full_size += 8 + dpds_size
        if seek_size:
            full_size += 8 + seek_size
        o_s.write_bytes('RIFF')
        o_s.write_uint32(full_size)
        o_s.write_bytes(riff_type)

    @staticmethod
    def write_chunk(o_s, name, data):
        o_s.write_bytes(name)
        o_s.write_uint32(len(data))
        o_s.write_bytes(data)


def write_wav(filename, header, data, needs_swap):
    PyWavWriter(header, data, needs_swap=needs_swap).write(filename)