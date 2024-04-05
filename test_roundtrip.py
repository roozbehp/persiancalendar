import persiancalendar


def test_roundtrip():
    start = persiancalendar.fixed_from_persian((1304, 1, 1))
    end = persiancalendar.fixed_from_persian((1500, 1, 1))

    for date in range(start, end):
        p_date = persiancalendar.persian_from_fixed(date)
        converted_back = persiancalendar.fixed_from_persian(p_date)
        assert (date == converted_back)


if __name__ == "__main__":
    test_roundtrip()
