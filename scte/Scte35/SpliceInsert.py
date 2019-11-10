import logging

import bitstring

from scte.Scte35.BreakDuration import BreakDuration
from scte.Scte35.TimeSignal import TimeSignal


class SpliceInsert:
    def __init__(self, bitarray_data, init_dict=None, logger=None):
        if logger is not None:
            self._log = logger
        else:
            self._log = logging.getLogger()
        None
        if init_dict:
            self.splice_insert_info = init_dict
            return

        self.splice_insert_info = {}
        self.splice_insert_info["splice_event_id"] = bitarray_data.read("uint:32")
        self.splice_insert_info["splice_event_cancel_indicator"] = bitarray_data.read("bool")
        self.splice_insert_info["reserved"] = bitarray_data.read("uint:7")
        if self.splice_insert_info["splice_event_cancel_indicator"] is False:
            self.splice_insert_info["out_of_network_indicator"] = bitarray_data.read("bool")
            self.splice_insert_info["program_splice_flag"] = bitarray_data.read("bool")
            self.splice_insert_info["duration_flag"] = bitarray_data.read("bool")
            self.splice_insert_info["splice_immediate_flag"] = bitarray_data.read("bool")
            self.splice_insert_info["reserved2"] = bitarray_data.read("uint:4")
            if self.splice_insert_info["program_splice_flag"] is True \
                    and self.splice_insert_info["splice_immediate_flag"] is False:
                self.splice_insert_info["splice_time"] = TimeSignal(bitarray_data)
            if self.splice_insert_info["program_splice_flag"] is False:
                raise NotImplementedError('Can not interpret splice_insert events with program_splice_flag False')
            if self.splice_insert_info["duration_flag"] is True:
                self.splice_insert_info["break_duration"] = BreakDuration(bitarray_data)
            self.splice_insert_info["unique_program_id"] = bitarray_data.read("uint:16")
            self.splice_insert_info["avail_num"] = bitarray_data.read("uint:8")
            self.splice_insert_info["avails_expected"] = bitarray_data.read("uint:8")

    @property
    def bitstring_format(self):
        bitstring_format = 'uint:32=splice_event_id,' \
                           'bool=splice_event_cancel_indicator,' \
                           'uint:7=reserved'
        return bitstring_format

    @property
    def splice_insert_detail_bitstring_format(self):
        bitstring_format = 'bool=out_of_network_indicator,' \
                           'bool=program_splice_flag,' \
                           'bool=duration_flag,' \
                           'bool=splice_immediate_flag,' \
                           'uint:4=reserved2'
        return bitstring_format

    @property
    def trailing_fields_bitstring_format(self):
        bitstring_format = 'uint:16=unique_program_id,' \
                           'uint:8=avail_num,' \
                           'uint:8=avails_expected'
        return bitstring_format

    def serialize(self):
        splice_insert_section_bs = bitstring.pack(fmt=self.bitstring_format, **self.splice_insert_info)

        splice_insert_detail_bs = None
        splice_time_bs = None
        break_duration_bs = None
        trailing_fields_bs = None
        if self.splice_insert_info["splice_event_cancel_indicator"] is False:
            splice_insert_detail_bs = bitstring.pack(
                fmt=self.splice_insert_detail_bitstring_format,
                **self.splice_insert_info
            )

            if self.splice_insert_info["program_splice_flag"] is True \
                    and self.splice_insert_info["splice_immediate_flag"] is False:
                splice_time_bs = self.splice_insert_info["splice_time"].serialize()

            if self.splice_insert_info["duration_flag"] is True:
                break_duration_bs = self.splice_insert_info["break_duration"].serialize()

            trailing_fields_bs = bitstring.pack(fmt=self.trailing_fields_bitstring_format, **self.splice_insert_info)

        return splice_insert_section_bs + splice_insert_detail_bs + splice_time_bs + break_duration_bs + trailing_fields_bs
