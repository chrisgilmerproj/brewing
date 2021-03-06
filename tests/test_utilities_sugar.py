# -*- coding: utf-8 -*-
import unittest

from brew.constants import SI_UNITS
from brew.exceptions import SugarException
from brew.exceptions import ValidatorException
from brew.utilities.sugar import apparent_extract_to_real_extract
from brew.utilities.sugar import brix_to_plato
from brew.utilities.sugar import brix_to_sg
from brew.utilities.sugar import gu_to_sg
from brew.utilities.sugar import hydrometer_adjustment
from brew.utilities.sugar import plato_to_brix
from brew.utilities.sugar import plato_to_sg
from brew.utilities.sugar import refractometer_adjustment
from brew.utilities.sugar import sg_to_brix
from brew.utilities.sugar import sg_to_gu
from brew.utilities.sugar import sg_to_plato


class TestSugarUtilities(unittest.TestCase):
    def test_brix_to_plato(self):
        plato = brix_to_plato(22.0)
        self.assertEquals(round(plato, 3), 22.001)

    def test_brix_to_sg(self):
        sg = brix_to_sg(22.0)
        self.assertEquals(round(sg, 3), 1.092)

    def test_gu_to_sg(self):
        sg = gu_to_sg(57.0)
        self.assertEquals(round(sg, 3), 1.057)

    def test_plato_to_brix(self):
        brix = plato_to_brix(14.0)
        self.assertEquals(round(brix, 3), 14.002)

    def test_plato_to_sg(self):
        sg = plato_to_sg(14.0)
        self.assertEquals(round(sg, 3), 1.057)

    def test_sg_to_brix(self):
        brix = sg_to_brix(1.092)
        self.assertEquals(round(brix, 1), 22.0)

    def test_sg_to_brix_raises(self):
        with self.assertRaises(SugarException) as ctx:
            sg_to_brix(1.18)
        self.assertEquals(
            str(ctx.exception), u"Above 40 degBx this function no longer works"
        )

    def test_sg_to_plato(self):
        plato = sg_to_plato(1.057)
        self.assertEquals(round(plato, 2), 14.04)

    def test_sg_to_gu(self):
        gu = sg_to_gu(1.057)
        self.assertEquals(round(gu, 2), 57.0)

    def test_apparent_extract_to_real_extract(self):
        oe = sg_to_plato(1.060)
        ae = sg_to_plato(1.010)
        out = apparent_extract_to_real_extract(oe, ae)
        self.assertEquals(round(out, 2), 4.88)

    def test_hydrometer_adjustment(self):
        sg = hydrometer_adjustment(1.050, 70.0)
        self.assertEquals(round(sg, 3), 1.051)

    def test_hydrometer_adjustment_no_adjustment(self):
        sg = hydrometer_adjustment(1.050, 59.0)
        self.assertEquals(round(sg, 3), 1.050)

    def test_hydromter_adjustment_si_units(self):
        sg = hydrometer_adjustment(1.050, 16.0, units=SI_UNITS)
        self.assertEquals(round(sg, 3), 1.050)

    def test_hydrometer_adjustment_raises_bad_units(self):
        with self.assertRaises(ValidatorException) as ctx:
            hydrometer_adjustment(1.050, 16.0, units=u"bad")
        self.assertEquals(
            str(ctx.exception), u"Unkown units 'bad', must use imperial or metric"
        )

    def test_hydrometer_adjustment_raises_bad_temp(self):
        with self.assertRaises(SugarException) as ctx:
            hydrometer_adjustment(1.050, -1.0)
        self.assertEquals(
            str(ctx.exception), u"Correction does not work outside temps 0 - 212F"
        )

        with self.assertRaises(SugarException) as ctx:
            hydrometer_adjustment(1.050, 213.0)
        self.assertEquals(
            str(ctx.exception), u"Correction does not work outside temps 0 - 212F"
        )

        with self.assertRaises(SugarException) as ctx:
            hydrometer_adjustment(1.050, -1.0, units=SI_UNITS)
        self.assertEquals(
            str(ctx.exception), u"Correction does not work outside temps 0 - 100C"
        )

        with self.assertRaises(SugarException) as ctx:
            hydrometer_adjustment(1.050, 101.0, units=SI_UNITS)
        self.assertEquals(
            str(ctx.exception), u"Correction does not work outside temps 0 - 100C"
        )

    def test_refractometer_adjustment(self):
        fg = refractometer_adjustment(1.053, 1.032)
        self.assertEquals(round(fg, 3), 1.017)
