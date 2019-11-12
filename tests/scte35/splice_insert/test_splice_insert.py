import base64
import logging
import unittest

from scte.Scte35 import SpliceEvent

TEST_VECTORS = {
    # From: https://support.google.com/admanager/answer/9087202?hl=en
    "google_ad_example": "/DAlAAAAAAAAAP/wFAUAAAAEf+/+kybGyP4BSvaQAAEBAQAArky/3g==",
    # From:
    # https://www.unified-streaming.com/blog/how-do-scte-35-based-dynamic-ad-insertion-live-streaming-unified-origin
    "unified_streaming_example": "/DAhAAAAAAAAAP/wEAUAAAA3f+9/fgBSZcAAAAAAAAAmObEZ",
}


class SpliceInsertTests(unittest.TestCase):
    def setUp(self):
        logger = logging.getLogger('')
        logger.setLevel(logging.WARN)
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARN)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(lineno)s - %(funcName)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    def test_vectors(self):
        for key in TEST_VECTORS:
            payload = TEST_VECTORS[key]
            print("B64 payload: {}".format(payload))
            original_hex_payload = base64.b64decode(payload).hex().upper()
            print("Hex payload: {}".format(original_hex_payload))
            my_event = SpliceEvent(TEST_VECTORS[key])
            print("Parsed hex : {}".format(my_event.hex_string))
            self.assertEqual(original_hex_payload, my_event.hex_string)


if __name__ == '__main__':
    unittest.main()
