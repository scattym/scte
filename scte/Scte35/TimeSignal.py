import bitstring
import logging
logger = logging.getLogger(__name__)

class TimeSignal:
    def __init__(self, bitarray_data, init_dict=None):
        if init_dict:
            self.splice_time = init_dict
            return

        self.splice_time = {}
        self.splice_time["time_specified_flag"] = bitarray_data.read("bool")
        if self.splice_time["time_specified_flag"] is True:
            self.splice_time["reserved"] = bitarray_data.read("uint:6")
            self.splice_time["pts_time"] = bitarray_data.read("uint:33")
        else:
            self.splice_time["reserved"] = bitarray_data.read("uint:7")

    def bitstring_format(self):
        bitstring_format = 'bool=time_specified_flag'

        if self.splice_time["time_specified_flag"] is True:
            bitstring_format += ',' + 'uint:6=reserved,' \
                                      'uint:33=pts_time'
        else:
            bitstring_format += ',' + 'uint:7=reserved'

        return bitstring_format

    def serialize(self):
        return bitstring.pack(fmt=self.bitstring_format(), **self.splice_time)

    def __str__(self):
        return str(self.splice_time)

    def __iter__(self):  # overridding this to return tuples of (key,value)
        arr = [('time_specified_flag', self.splice_time['time_specified_flag'])]
        if self.splice_time["time_specified_flag"] is True:
            arr += [('pts_time', self.splice_time['pts_time'])]
        return iter(arr)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, input_dict):
        # Need to do input checking here
        return cls(bitarray_data=None, init_dict=input_dict)
