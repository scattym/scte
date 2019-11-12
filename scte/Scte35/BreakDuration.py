import bitstring
import logging
logger = logging.getLogger(__name__)

class BreakDuration:
    def __init__(self, bitarray_data, init_dict=None):
        if init_dict:
            self.break_duration = init_dict
            return

        self.break_duration = {}
        self.break_duration["auto_return"] = bitarray_data.read("bool")
        self.break_duration["reserved"] = bitarray_data.read("uint:6")
        self.break_duration["duration"] = bitarray_data.read("uint:33")

    def bitstring_format(self):
        bitstring_format = 'bool=auto_return,uint:6=reserved,uint:33=duration'
        return bitstring_format

    def serialize(self):
        return bitstring.pack(fmt=self.bitstring_format(), **self.break_duration)

    def __str__(self):
        return str(self.break_duration)

    def __iter__(self): #overridding this to return tuples of (key,value)
        arr = [('auto_return', self.break_duration['auto_return']), ('duration', self.break_duration['duration'])]
        return iter(arr)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, input_dict):
        # Need to do input checking here
        return cls(bitarray_data=None, init_dict=input_dict)
