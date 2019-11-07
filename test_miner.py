import os
import tempfile
import unittest

from miner import parse_var_line, parse_file


class TestMiner(unittest.TestCase):

    def test_parse_var_line(self):
        line = "Output:Variable,*,Heating Coil Crankcase Heater Electric Power,hourly; !- HVAC Average [W]"
        d = parse_var_line(line)
        self.assertEqual(d["name"], "Heating Coil Crankcase Heater Electric Power")
        self.assertEqual(d["comment"], "HVAC Average")
        self.assertEqual(d["unit"], "W")

        line = "Output:Variable,*,Heating Coil Crankcase Heater Electric Energy,hourly; !- HVAC Sum [J]"
        d = parse_var_line(line)
        self.assertEqual(d["name"], "Heating Coil Crankcase Heater Electric Energy")
        self.assertEqual(d["comment"], "HVAC Sum")
        self.assertEqual(d["unit"], "J")

        line = "Output:Variable,*,Cooling Coil Runtime Fraction,hourly; !- HVAC Average []"
        d = parse_var_line(line)
        self.assertEqual(d["name"], "Cooling Coil Runtime Fraction")
        self.assertEqual(d["comment"], "HVAC Average")
        self.assertEqual(d["unit"], "")

    def test_parse_file(self):
        file_str = "! Program Version,EnergyPlus, Version 9.3.0-7bb5e69fa0, YMD=2019.11.07 09:44,\n" \
                   "! Output:Variable Objects (applicable to this run)\n" \
                   "Output:Variable,*,Site Outdoor Air Drybulb Temperature,hourly; !- Zone Average [C]\n" \
                   "Output:Variable,*,Site Outdoor Air Dewpoint Temperature,hourly; !- Zone Average [C]\n"

        f_dir = os.path.join(tempfile.mkdtemp(), 'temp.rdd')
        with open(f_dir, 'w+') as f:
            for line in file_str:
                f.write(line)

        v = parse_file(f_dir)

        self.assertEqual(len(v), 2)
        self.assertEqual(v[0]["name"], "Site Outdoor Air Drybulb Temperature")
        self.assertEqual(v[0]["comment"], "Zone Average")
        self.assertEqual(v[0]["unit"], "C")

        self.assertEqual(v[1]["name"], "Site Outdoor Air Dewpoint Temperature")
        self.assertEqual(v[1]["comment"], "Zone Average")
        self.assertEqual(v[1]["unit"], "C")
