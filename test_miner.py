import os
import tempfile
import unittest

from miner import parse_var_line, parse_file


class TestMiner(unittest.TestCase):

    def test_parse_var_line(self):
        line = "Output:Variable,*,Heating Coil Crankcase Heater Electric Power,hourly; !- HVAC Average [W]"
        d = parse_var_line(line)
        self.assertEqual(d, "Heating Coil Crankcase Heater Electric Power")

        line = "Zone,Average,Site Outdoor Air Drybulb Temperature [C]"
        d = parse_var_line(line)
        self.assertEqual(d, "Site Outdoor Air Drybulb Temperature")

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
        self.assertEqual(v[0], "Site Outdoor Air Drybulb Temperature")

        self.assertEqual(v[1], "Site Outdoor Air Dewpoint Temperature")

