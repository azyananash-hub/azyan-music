import io
import unittest

from _helpers import FMEA, load_module

fmea = load_module("fmea_rpn", FMEA)

HEADER = "item,failure_mode,effect,cause,severity,occurrence,detection,control\n"


def _load(text: str):
    return fmea.load_rows(io.StringIO(text))


class FmeaTests(unittest.TestCase):
    def test_rpn_product(self):
        rows = _load(HEADER + "pump,seal leak,,,8,5,4,\n")
        self.assertEqual(rows[0].rpn, 160)

    def test_ordering_descending(self):
        rows = _load(HEADER + "a,f1,,,2,2,2,\nb,f2,,,8,5,4,\nc,f3,,,5,5,5,\n")
        ordered = fmea.prioritise(rows)
        self.assertEqual([r["item"] for r in ordered], ["b", "c", "a"])
        self.assertEqual([r["rpn"] for r in ordered], [160, 125, 8])

    def test_flags(self):
        rows = _load(HEADER + "a,f1,,,9,1,1,\nb,f2,,,8,5,4,\n")
        ordered = {r["item"]: r["flags"] for r in fmea.prioritise(rows)}
        # S=9 selalu perlu tinjauan walau RPN 9 kecil
        self.assertIn("HIGH_SEVERITY_REVIEW", ordered["a"])
        self.assertNotIn("RPN_ABOVE_THRESHOLD", ordered["a"])
        self.assertIn("RPN_ABOVE_THRESHOLD", ordered["b"])

    def test_out_of_range_rejected(self):
        for bad in ("0", "11", "x", "3.5"):
            with self.assertRaises(ValueError, msg=bad):
                _load(HEADER + f"a,f,,,{bad},5,5,\n")

    def test_missing_column_rejected(self):
        with self.assertRaises(ValueError):
            _load("item,failure_mode,severity,occurrence\na,f,5,5\n")

    def test_empty_file_rejected(self):
        with self.assertRaises(ValueError):
            fmea.load_rows(io.StringIO(""))


if __name__ == "__main__":
    unittest.main()
