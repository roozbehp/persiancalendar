import persiancalendar


def test_leap():
    with open("kabise.txt") as kabise_txt:
        for line in kabise_txt:
            if line.startswith('#'):
                continue
            p_year, g_date = line.strip().split()
            if p_year.endswith('**'):
                leap = 5
            elif p_year.endswith('*'):
                leap = 4
            else:
                leap = 0
            p_year = int(p_year[:4])
            if leap == 5:
                assert (persiancalendar.persian_leap_year(p_year))
                assert (persiancalendar.persian_leap_year(p_year - 5))
            elif leap == 4:
                assert (persiancalendar.persian_leap_year(p_year))
                assert (persiancalendar.persian_leap_year(p_year - 4))
            else:
                assert (not persiancalendar.persian_leap_year(p_year))

            g_year, g_month, g_day = g_date.split('-')
            g_year = int(g_year)
            g_month = int(g_month)
            g_day = int(g_day)
            g_date = persiancalendar.fixed_from_gregorian(
                (g_year, g_month, g_day))
            nowruz = persiancalendar.fixed_from_persian((p_year, 1, 1))
            assert (nowruz == g_date)


if __name__ == "__main__":
    test_leap()
