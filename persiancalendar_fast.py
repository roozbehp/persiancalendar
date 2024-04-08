# This code is partially based on the Common Lisp code published by
# Reingold and Dershowitz under the Apache 2.0 license.
#
# Python port and modifications for using the 33-year cycle were
# made by Roozbeh Pournader.
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

PERSIAN_EPOCH = 226896  # Precalculated result from Calendarical Calculations

SUPPORTED_FIRST_YEAR = 1178
SUPPORTED_LAST_YEAR = 3000

# All these years are not leap, while they are considered leap by the 33-year
# rule. The year following each of them is leap, but it's considered non-leap
# by the 33-year rule. This table has been tested to match the modified
# astronomical algorithm based on the 52.5 degrees east meridian from 1178 AP
# (an arbitrary date before the Persian calendar was adopted in 1304 AP) to
# 3000 AP (an arbitrary date far into the future).
NON_LEAP_CORRECTION = frozenset(
    {
        1502,
        1601, 1634, 1667,
        1700, 1733, 1766, 1799,
        1832, 1865, 1898,
        1931, 1964, 1997,
        2030, 2059, 2063, 2096,
        2129, 2158, 2162, 2191, 2195,
        2224, 2228, 2257, 2261, 2290, 2294,
        2323, 2327, 2356, 2360, 2389, 2393,
        2422, 2426, 2455, 2459, 2488, 2492,
        2521, 2525, 2554, 2558, 2587, 2591,
        2620, 2624, 2653, 2657, 2686, 2690,
        2719, 2723, 2748, 2752, 2756, 2781, 2785, 2789,
        2818, 2822, 2847, 2851, 2855, 2880, 2884, 2888,
        2913, 2917, 2921, 2946, 2950, 2954, 2979, 2983, 2987
    })


def fixed_from_persian_fast(p_date):
    year, month, day = p_date
    new_year = PERSIAN_EPOCH - 1 + 365 * (year - 1) + (8 * year + 21) // 33
    if year - 1 in NON_LEAP_CORRECTION:
        new_year -= 1
    return (new_year - 1  # Days in prior years.
            # Days in prior months this year.
            + (31 * (month - 1) if month <= 7 else 30 * (month - 1) + 6)
            + day)  # Days so far this month.


def div_ceil(a, b):
    return -((-a) // b)


def persian_fast_from_fixed(date):
    days_since_epoch = date - fixed_from_persian_fast((1, 1, 1))
    year = 1 + (33 * days_since_epoch + 3) // 12053
    day_of_year = date - fixed_from_persian_fast((year, 1, 1)) + 1
    if day_of_year == 366 and year in NON_LEAP_CORRECTION:
        year += 1
        day_of_year = 1
    if day_of_year <= 186:
        month = div_ceil(day_of_year, 31)
    else:
        month = div_ceil(day_of_year - 6, 30)
    # Calculate the day by subtraction
    day = date - fixed_from_persian_fast((year, month, 1)) + 1
    return (year, month, day)


def persian_fast_leap_year(p_year):
    if p_year in NON_LEAP_CORRECTION:
        return False
    elif p_year - 1 in NON_LEAP_CORRECTION:
        return True
    else:
        return (25 * p_year + 11) % 33 < 8
