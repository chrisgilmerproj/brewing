# -*- coding: utf-8 -*-
from ..constants import GAL_PER_LITER
from ..constants import IMPERIAL_UNITS
from ..constants import POUND_PER_KG
from ..constants import SI_UNITS
from ..exceptions import ColorException
from ..validators import validate_units

__all__ = [
    u"srm_to_ebc",
    u"ebc_to_srm",
    u"calculate_mcu",
    u"calculate_srm_mosher",
    u"calculate_srm_daniels",
    u"calculate_srm_daniels_power",
    u"calculate_srm_noonan_power",
    u"calculate_srm_morey_hybrid",
    u"calculate_srm_morey",
    u"calculate_srm",
    u"lovibond_to_srm",
    u"srm_to_lovibond",
    u"srm_to_a430",
    u"ebc_to_a430",
]


def srm_to_ebc(srm):
    """
    Convert SRM to EBC Color

    :param float srm: SRM Color
    :return: EBC Color
    :rtype: float
    """
    return srm * 1.97


def ebc_to_srm(ebc):
    """
    Convert EBC to SRM Color

    :param float ebc: EBC Color
    :return: SRM Color
    :rtype: float
    """
    return ebc / 1.97


def calculate_mcu(grain_weight, beer_color, final_volume, units=IMPERIAL_UNITS):
    """
    Calculate MCU from Grain

    :param float grain_weight: Grain weight in lbs or kg
    :param float beer_color: Beer color in deg Lovibond
    :param float final_volume: Final Volume in gal or liters
    :param str units: The units

    Source:

    * http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/
    """  # noqa
    validate_units(units)
    if units == SI_UNITS:
        grain_weight = grain_weight * POUND_PER_KG
        final_volume = final_volume * GAL_PER_LITER

    mcu = grain_weight * beer_color / final_volume
    return mcu


def calculate_srm_mosher(mcu):
    """
    Mosher Equation for SRM

    :param float mcu: The Malt Color Units
    :return: SRM Color
    :rtype: float
    :raises ColorException: If the MCU is < 7.0
    """  # noqa
    if mcu < 7.0:
        raise ColorException(u"Mosher equation does not work for MCU < 7.0")
    srm = (mcu * 0.3) + 4.7
    return srm


def calculate_srm_daniels(mcu):
    """
    Daniels Equation for SRM

    :param float mcu: The Malt Color Units
    :return: SRM Color
    :rtype: float
    :raises ColorException: If the MCU is < 11.0
    """  # noqa
    if mcu < 11.0:
        raise ColorException(u"Daniels equation does not work for MCU < 11.0")
    srm = (mcu * 0.2) + 8.4
    return srm


def calculate_srm_daniels_power(mcu):
    """
    Daniels Power Equation for SRM based on work by Druey

    :param float mcu: The Malt Color Units
    :return: SRM Color
    :rtype: float
    :raises ColorException: If the SRM is > 50.0
    """  # noqa
    srm = 1.73 * (mcu ** 0.64) - 0.27
    if srm > 50.0:
        raise ColorException(
            u"Daniels Power equation does not work above SRM 50.0"
        )  # noqa
    return srm


def calculate_srm_noonan_power(mcu):
    """
    Noonan Power Equation for SRM based on work by Druey

    :param float mcu: The Malt Color Units
    :return: SRM Color
    :rtype: float
    :raises ColorException: If the SRM is > 50.0
    """  # noqa
    srm = 15.03 * (mcu ** 0.27) - 15.53
    if srm > 50.0:
        raise ColorException(
            u"Noonan Power equation does not work above SRM 50.0"
        )  # noqa
    return srm


def calculate_srm_morey_hybrid(mcu):
    """
    A hybrid approach used by Morey for SRM.

    :param float mcu: The Malt Color Units
    :return: SRM Color
    :rtype: float
    :raises ColorException: If the MCU is > 50.0

    Assumptions:

    1. SRM is approximately equal to MCU for values from 0 to 10.
    2. Homebrew is generally darker than commercial beer.
    3. Base on the previous qualitative postulate, I assumed that Ray Daniels'
       predicted relationship exists for beers with color greater than 10.
    4. Since Mosher's equation predicts darker color than Daniels' model for
       values of MCU greater than 37, I assumed that Mosher's approximation
       governed beer color for all values more than 37 MCUs.
    5. Difference in color for beers greater than 40 SRM are essentially
       impossible to detect visually; therefore, I limited the analysis to SRM
       of 50 and less.

    Source:

    * http://babblehomebrewers.com/attachments/article/61/beercolor.pdf
    """
    srm = 0
    if 0 < mcu < 10:
        srm = mcu
    elif 10 <= mcu < 37:
        srm = calculate_srm_daniels(mcu)
    elif 37 <= mcu < 50:
        srm = calculate_srm_mosher(mcu)
    else:
        raise ColorException(u"Morey Hybrid does not work above MCU 50.0")

    # SRM never gets above 50 so no exception is needed here
    return srm


def calculate_srm_morey(mcu):
    """
    Morey Equation for SRM

    :param float mcu: The Malt Color Units
    :return: SRM Color
    :rtype: float
    :raises ColorException: If the SRM is > 50.0

    Source:

    * http://www.morebeer.com/brewingtechniques/beerslaw/morey.html
    * http://beersmith.com/blog/2008/04/29/beer-color-understanding-srm-lovibond-and-ebc/
    """  # noqa
    srm = 1.4922 * (mcu ** 0.6859)
    if srm > 50.0:
        raise ColorException(u"Morey equation does not work above SRM 50.0")
    return srm


def calculate_srm(mcu):
    """
    General SRM calculation uses the Morey Power Equation

    :param float mcu: The Malt Color Units
    :return: SRM Color
    :rtype: float
    :raises ColorException: If the SRM is > 50.0
    """
    return calculate_srm_morey(mcu)


def lovibond_to_srm(lovibond):
    """
    Convert deg Lovibond to SRM

    :param float lovibond: The degrees Lovibond
    :return: SRM Color
    :rtype: float

    Source:

    * https://en.wikipedia.org/wiki/Standard_Reference_Method
    """
    return 1.3546 * lovibond - 0.76


def srm_to_lovibond(srm):
    """
    Convert SRM to deg Lovibond

    :param float srm: SRM Color
    :return: The degrees Lovibond
    :rtype: float

    Source:

    * https://en.wikipedia.org/wiki/Standard_Reference_Method
    """
    return (srm + 0.76) / 1.3546


def srm_to_a430(srm, dilution=1.0):
    """
    Get attenuation at A430 from SRM and dilution

    :param float srm: SRM Color
    :param float dilution: The dilution factor (D=1 for undiluted, D=2 for 1:1 dilution, etc)
    :return: The attenuiation at 430nm
    :rtype: float

    Source:

    * https://en.wikipedia.org/wiki/Standard_Reference_Method
    """  # noqa
    return srm / (12.7 * dilution)


def ebc_to_a430(ebc, dilution=1.0):
    """
    Get attenuation at A430 from EBC and dilution

    :param float ebc: EBC Color
    :param float dilution: The dilution factor (D=1 for undiluted, D=2 for 1:1 dilution, etc)
    :return: The attenuiation at 430nm
    :rtype: float

    Source:

    * https://en.wikipedia.org/wiki/Standard_Reference_Method
    """  # noqa
    return srm_to_a430(ebc_to_srm(ebc), dilution=dilution)
