# !/usr/bin/env python3
#
# This code is based on the Common Lisp code published by Reingold and Dershowitz
# under the Apache 2.0 license.
#
# Python port and further modificiations were made by Roozbeh Pournader.
#
# Copyright 2024 Roozbeh Pournader
#
# The original header follows:
#
# CALENDRICA 4.0 -- Common Lisp
# E. M. Reingold and N. Dershowitz
#
# ================================================================
#
# The Functions (code, comments, and definitions) contained in this
# file (the "Program") were written by Edward M. Reingold and Nachum
# Dershowitz (the "Authors"), who retain all rights to them except as
# granted in the License and subject to the warranty and liability
# limitations listed therein.  These Functions are explained in the Authors'
# book, "Calendrical Calculations", 4th ed. (Cambridge University
# Press, 2016), and are subject to an international copyright.
#
# Licensed under the Apache License, Version 2.0 <LICENSE or
# https://www.apache.org/licenses/LICENSE-2.0>.
#
# Sample values for the functions (useful for debugging) are given in
# Appendix C of the book.

import math


def mod3(x, a, b):
    """The value of x shifted into the range [a..b). Returns x if a=b."""
    if a == b:
        return x
    else:
        return a + (x - a) % (b - a)


def poly(x, a):
    """Sum powers of x with coefficients (from order 0 up) in list a."""
    if not a:
        return 0
    else:
        return a[0] + x * poly(x, a[1:])


def rd(tee):
    """Identity function for fixed dates/moments.  If internal
    timekeeping is shifted, change epoch to be RD date of
    origin of internal count. epoch should be an integer."""
    epoch = 0
    return tee - epoch


def sign(y):
    """Sign of y."""
    if y < 0:
        return -1
    elif y > 0:
        return +1
    else:
        return 0


# Fixed date of start of the (proleptic) Gregorian calendar.
GREGORIAN_EPOCH = rd(1)


def gregorian_leap_year(g_year):
    """True if g_year is a leap year on the Gregorian calendar."""
    return g_year % 4 == 0 and (g_year % 400) not in [100, 200, 300]


def fixed_from_gregorian(g_date):
    year, month, day = g_date
    """Fixed date equivalent to the Gregorian date g_date."""
    return (
        GREGORIAN_EPOCH - 1  # Days before start of calendar
        + 365 * (year - 1)  # Ordinary days since epoch
        + (year - 1) // 4   # Julian leap days since epoch...
        - (year - 1) // 100  # ...minus century years since epoch...
        + (year - 1) // 400  # plus years since epoch divisible by 400.
        # Days in prior months this year assuming 30-day Feb
        + (367 * month - 362) // 12
        # Correct for 28- or 29-day Feb
        + (0 if month <= 2 else (-1 if gregorian_leap_year(year) else -2))
        + day)  # Days so far this month.


def gregorian_year_from_fixed(date):
    """Gregorian year corresponding to the fixed date."""
    d0 = date - GREGORIAN_EPOCH  # Prior days.
    n400 = d0 // 146097  # Completed 400-year cycles.
    d1 = d0 % 146097  # Prior days not in n400.
    n100 = d1 // 36524  # 100-year cycles not in n400.
    d2 = d1 % 36524  # Prior days not in n400 or n100.
    n4 = d2 // 1461  # 4-year cycles not in n400 or n100.
    d3 = d2 % 1461  # Prior days not in n400, n100, or n4.
    n1 = d3 // 365  # Years not in n400, n100, or n4.
    year = 400 * n400 + 100 * n100 + 4 * n4 + n1
    if n100 == 4 or n1 == 4:
        return year  # Date is day 366 in a leap year.
    else:
        return year + 1  # Date is ordinal day (d % 365 + 1) in (year + 1).


def gregorian_new_year(g_year):
    """Fixed date of January 1 in g_year."""
    return fixed_from_gregorian((g_year, 1, 1))


def gregorian_from_fixed(date):
    """Gregorian (year, month, day) corresponding to fixed date."""
    year = gregorian_year_from_fixed(date)
    prior_days = date - gregorian_new_year(year)  # This year
    # To simulate a 30-day Feb
    if date < fixed_from_gregorian((year, 3, 1)):
        correction = 0
    elif gregorian_leap_year(year):
        correction = 1
    else:
        correction = 2
    month = (12 * (prior_days - correction) +
             373) // 367  # Assuming a 30-day Feb
    # Calculate the day by subtraction.
    day = date - fixed_from_gregorian((year, month, 1)) + 1
    return (year, month, day)


def gregorian_date_difference(g_date1, g_date2):
    """Number of days from Gregorian date g_date1 until g_date2."""
    return fixed_from_gregorian(g_date2) - fixed_from_gregorian(g_date1)


# Fixed date of start of the Julian calendar.
JULIAN_EPOCH = fixed_from_gregorian((0, 12, 30))


def julian_leap_year(j_year):
    """True if j_year is a leap year on the Julian calendar."""
    return (j_year % 4) == (0 if j_year > 0 else 3)


def fixed_from_julian(year, month, day):
    """Fixed date equivalent to the Julian date."""
    y = year + 1 if year < 0 else year  # No year zero
    return (
        JULIAN_EPOCH - 1  # Days before start of calendar
        + 365 * (y - 1)  # Ordinary days since epoch.
        + (y - 1) // 4   # Leap days since epoch...
        # Days in prior months this year...
        + ((367 * month - 362) // 12)  # ...assuming 30-day Feb
        # Correct for 28- or 29-day Feb
        + (0 if month <= 2 else (-1 if julian_leap_year(year) else -2))
        + day)           # Days so far this month.


def hr(x):
    """x hours."""
    return x / 24


def angle(d, m, s):
    """d degrees, m arcminutes, s arcseconds."""
    return d + (m + s / 60) / 60


def radians_from_degrees(theta):
    """Convert angle theta from degrees to radians."""
    return (theta % 360) * math.pi / 180


def sin_degrees(theta):
    """Sine of theta (given in degrees)."""
    return math.sin(radians_from_degrees(theta))


def cos_degrees(theta):
    """Cosine of theta (given in degrees)."""
    return math.cos(radians_from_degrees(theta))


def tan_degrees(theta):
    """Tangent of $theta$ (given in degrees)."""
    return math.tan(radians_from_degrees(theta))


def longitude(location):
    return location[1]


def zone_from_longitude(phi):
    """Difference between UT and local mean time at longitude
    phi as a fraction of a day."""
    return phi / 360


def universal_from_local(tee_ell, location):
    """Universal time from local tee_ell at location."""
    return tee_ell - zone_from_longitude(longitude(location))


def local_from_apparent(tee, location):
    """Local time from sundial time tee at location."""
    return tee - equation_of_time(universal_from_local(tee, location))


def universal_from_apparent(tee, location):
    """Universal time from sundial time tee at location."""
    return universal_from_local(local_from_apparent(tee, location), location)


def midday(date, location):
    """Universal time on fixed date of midday at location."""
    return universal_from_apparent(date + hr(12), location)


def julian_centuries(tee):
    """Julian centuries since 2000 at moment tee."""
    return (dynamical_from_universal(tee) - J2000) / 36525


def obliquity(tee):
    """Obliquity of ecliptic at moment tee."""
    c = julian_centuries(tee)
    return angle(23, 26, 21.448) + poly(c, (0,
                                            angle(0, 0, -46.8150),
                                            angle(0, 0, -0.00059),
                                            angle(0, 0, 0.001813)))


def dynamical_from_universal(tee_rom_u):
    """Dynamical time at Universal moment tee_rom_u."""
    return tee_rom_u + ephemeris_correction(tee_rom_u)


# Noon at start of Gregorian year 2000.
J2000 = hr(12) + gregorian_new_year(2000)

MEAN_TROPICAL_YEAR = 365.242189


def ephemeris_correction(tee):
    """Dynamical Time minus Universal Time (in days) for moment tee.

    Adapted from "Astronomical Algorithms"
    by Jean Meeus, Willmann-Bell (1991) for years
    1600-1986 and from polynomials on the NASA
    Eclipse web site for other years."""

    year = gregorian_year_from_fixed(math.floor(tee))
    c = gregorian_date_difference((1900, 1, 1), (year, 7, 1)) / 36525
    c2051 = (-20 + 32 * ((year - 1820) / 100) ** 2
                 + 0.5628 * (2150 - year)) / 86400
    y2000 = year - 2000
    c2006 = poly(y2000, (62.92, 0.32217, 0.005589)) / 86400
    c1987 = poly(y2000, (63.86, 0.3345, -0.060374,
                         0.0017275,
                         0.000651814, 0.00002373599)) / 86400
    c1900 = poly(c, (-0.00002, 0.000297, 0.025184,
                     -0.181133, 0.553040, -0.861938,
                     0.677066, -0.212591))
    c1800 = poly(c, (-0.000009, 0.003844, 0.083563,
                     0.865736,
                     4.867575, 15.845535, 31.332267,
                     38.291999, 28.316289, 11.636204,
                     2.043794))
    y1700 = year - 1700
    c1700 = poly(y1700, (8.118780842, -0.005092142,
                         0.003336121, -0.0000266484)) / 86400
    y1600 = year - 1600
    c1600 = poly(y1600, (120, -0.9808, -0.01532,
                         0.000140272128)) / 86400
    y1000 = (year - 1000) / 100
    c500 = poly(y1000, (1574.2, -556.01, 71.23472, 0.319781,
                        -0.8503463, -0.005050998,
                        0.0083572073)) / 86400
    y0 = year / 100
    c0 = poly(y0, (10583.6, -1014.41, 33.78311,
                   -5.952053, -0.1798452, 0.022174192,
                   0.0090316521)) / 86400
    y1820 = (year - 1820) / 100
    other = poly(y1820, (-20, 0, 32)) / 86400
    if 2051 <= year <= 2150:
        return c2051
    elif 2006 <= year <= 2050:
        return c2006
    elif 1987 <= year <= 2005:
        return c1987
    elif 1900 <= year <= 1986:
        return c1900
    elif 1800 <= year <= 1899:
        return c1800
    elif 1700 <= year <= 1799:
        return c1700
    elif 1600 <= year <= 1699:
        return c1600
    elif 500 <= year <= 1599:
        return c500
    elif -500 < year < 500:
        return c0
    else:
        return other


def equation_of_time(tee):
    """Equation of time (as fraction of day) for moment tee.

    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann-Bell, 2nd edn., 1998, p. 185."""

    c = julian_centuries(tee)
    lamda = poly(c, (280.46645, 36000.76983, 0.0003032))
    anomaly = poly(c, (357.52910, 35999.05030, -0.0001559, -0.00000048))
    eccentricity = poly(c, (0.016708617, -0.000042037, -0.0000001236))
    varepsilon = obliquity(tee)
    y = tan_degrees(varepsilon / 2) ** 2
    equation = ((1 / 2 / math.pi) *
                (y * sin_degrees(2 * lamda)
                 - 2 * eccentricity * sin_degrees(anomaly)
                 + 4 * eccentricity * y * sin_degrees(anomaly)
                     * cos_degrees(2 * lamda)
                 - 0.5 * y * y * sin_degrees(4 * lamda)
                 - 1.25 * eccentricity * eccentricity
                     * sin_degrees(2 * anomaly)))
    return sign(equation) * min(abs(equation), hr(12))


def solar_longitude(tee):
    """Longitude of sun at moment tee.

    Adapted from "Planetary Programs and Tables from -4000
    to +2800" by Pierre Bretagnon and Jean-Louis Simon,
    Willmann-Bell, 1986."""

    c = julian_centuries(tee)  # moment in Julian centuries
    coefficients = (403406, 195207, 119433, 112392, 3891, 2819, 1721,
                    660, 350, 334, 314, 268, 242, 234, 158, 132, 129, 114,
                    99, 93, 86, 78, 72, 68, 64, 46, 38, 37, 32, 29, 28, 27, 27,
                    25, 24, 21, 21, 20, 18, 17, 14, 13, 13, 13, 12, 10, 10, 10,
                    10)
    multipliers = (0.9287892, 35999.1376958, 35999.4089666,
                   35998.7287385, 71998.20261, 71998.4403,
                   36000.35726, 71997.4812, 32964.4678,
                   -19.4410, 445267.1117, 45036.8840, 3.1008,
                   22518.4434, -19.9739, 65928.9345,
                   9038.0293, 3034.7684, 33718.148, 3034.448,
                   -2280.773, 29929.992, 31556.493, 149.588,
                   9037.750, 107997.405, -4444.176, 151.771,
                   67555.316, 31556.080, -4561.540,
                   107996.706, 1221.655, 62894.167,
                   31437.369, 14578.298, -31931.757,
                   34777.243, 1221.999, 62894.511,
                   -4442.039, 107997.909, 119.066, 16859.071,
                   -4.578, 26895.292, -39.127, 12297.536,
                   90073.778)
    addends = (270.54861, 340.19128, 63.91854, 331.26220,
               317.843, 86.631, 240.052, 310.26, 247.23,
               260.87, 297.82, 343.14, 166.79, 81.53,
               3.50, 132.75, 182.95, 162.03, 29.8,
               266.4, 249.2, 157.6, 257.8, 185.1, 69.9,
               8.0, 197.1, 250.4, 65.3, 162.7, 341.5,
               291.6, 98.5, 146.7, 110.0, 5.2, 342.6,
               230.9, 256.1, 45.3, 242.9, 115.2, 151.8,
               285.3, 53.3, 126.6, 205.7, 85.9,
               146.1)
    x = coefficients
    y = addends
    z = multipliers
    lamda = (
        282.7771834
        + 36000.76953744 * c
        + 0.000005729577951308232 *
        sum([x[i] * sin_degrees(y[i] + z[i] * c) for i in range(len(x))])
    )
    return (lamda + aberration(tee) + nutation(tee)) % 360


def nutation(tee):
    """Longitudinal nutation at moment tee."""
    c = julian_centuries(tee)  # moment in Julian centuries
    cap_a = poly(c, (124.90, -1934.134, 0.002063))
    cap_b = poly(c, (201.11, 72001.5377, 0.00057))
    return - 0.004778 * sin_degrees(cap_a) - 0.0003667 * sin_degrees(cap_b)


def aberration(tee):
    """Aberration at moment tee."""
    c = julian_centuries(tee)  # moment in Julian centuries
    return 0.0000974 * cos_degrees(177.63 + 35999.01848 * c) - 0.005575


# Longitude of sun at vernal equinox.
SPRING = 0


def estimate_prior_solar_longitude(lamda, tee):
    """Approximate moment at or before tee
    when solar longitude just exceeded lamda degrees."""
    rate = MEAN_TROPICAL_YEAR / 360  # Mean change of one degree.
    # First approximation.
    tau = tee - rate * ((solar_longitude(tee) - lamda) % 360)
    cap_delta = mod3(solar_longitude(tau) - lamda, -180, 180)
    return min(tee, tau - rate * cap_delta)


# Fixed date of start of the Persian calendar.
PERSIAN_EPOCH = fixed_from_julian(622, 3, 19)

# Location of Tehran, Iran.
TEHRAN = (35.68, 51.42, 1100, +3.5)
# Middle of Iran.
IRAN = (35.5, 52.5, 0, +3.5)

persian_locale = IRAN


def set_persian_locale(locale):
    """Change the locale used for computing the Persian calenar."""
    global persian_locale
    persian_locale = locale


def midday_in_persian_locale(date):
    """Universal time of true noon on fixed date in the locale used for computing the Persian calenddar."""
    return midday(date, persian_locale)


def persian_new_year_on_or_before(date):
    """Fixed date of Astronomical Persian New Year on or before fixed date."""
    # Approximate time of equinox.
    approx = estimate_prior_solar_longitude(
        SPRING, midday_in_persian_locale(date))
    day = math.floor(approx) - 1
    while solar_longitude(midday_in_persian_locale(day)) > SPRING + 2:
        day += 1
    return day


def fixed_from_persian(p_date):
    """Fixed date of Astronomical Persian date p_date."""
    year, month, day = p_date
    new_year = persian_new_year_on_or_before(
        PERSIAN_EPOCH + 180  # Fall after epoch.
        + math.floor(MEAN_TROPICAL_YEAR *
                     (year - 1 if 0 < year else year)))  # No year zero.
    return (new_year - 1  # Days in prior years.
            # Days in prior months this year.
            + (31 * (month - 1) if month <= 7 else 30 * (month - 1) + 6)
            + day)  # Days so far this month.


def persian_from_fixed(date):
    """Astronomical Persian date corresponding to fixed date."""
    new_year = persian_new_year_on_or_before(date)
    y = round((new_year - PERSIAN_EPOCH) / MEAN_TROPICAL_YEAR) + 1
    year = y if 0 < y else y - 1  # No year zero
    day_of_year = date - fixed_from_persian((year, 1, 1)) + 1
    month = math.ceil(
        day_of_year /
        31) if day_of_year <= 186 else math.ceil(
        (day_of_year -
         6) /
        30)
    # Calculate the day by subtraction
    day = date - fixed_from_persian((year, month, 1)) + 1
    return (year, month, day)


def nowruz(g_year):
    """Fixed date of Persian New Year (Nowruz) in Gregorian year g_year."""
    persian_year = g_year - gregorian_year_from_fixed(PERSIAN_EPOCH) + 1
    y = persian_year - 1 if persian_year <= 0 else persian_year  # No Persian year 0
    return fixed_from_persian((y, 1, 1))
