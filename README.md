This is a partial port of Calendrical Calculations code to Python, focused on the astronomical Persian calendar.

The code is updated to reflect the best information available on
the ground about the Persian calendar, especially changing its locale
to 52.5 degrees east, which is what the Iranian calendar authority uses.

The output of this code matches the partial leap year table published by the
Iranian calendar authority (The Center for Calendar, Geophysics Institute,
University of Tehran), available at
https://calendar.ut.ac.ir/Fa/News/Data/Doc/KabiseShamsi1206-1498-new.pdf.
(That leap year table covers 1206 to 1498 AP.)

The original method, published in the book Calendrical Calculations and
implemented in the original Lisp code, uses Tehran as the locale for its
astronomical calculations. That fails to match all of the leap years
published by the Iranian calendar authority (see above). Specifically,
1469 AP should be leap and 1470 AP should not be leap. Changing the locale
to the meridian used for the Iranian standard time fixes this problem.
