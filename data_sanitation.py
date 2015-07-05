import regex
import unittest


_number_regex = regex.compile('\d+(\.\d+)?')


def _is_number(value: str):
    try:
        # Let's assume that the value has potentially been cleaned for mongo, i.e. .s have become _s
        float(value.replace('_', '.'))
    except ValueError:
        return False
    return True


# TODO plumb this in and change the tests.
def _is_unfccc_acceptable(value: str) -> bool:
    return True


def _is_acceptable(system: str, value: str) -> bool:
    if system == "UNFCCC":
        return _is_unfccc_acceptable(value)
    return _is_number(value)
    # v, _, o = value.partition('/')
    # return is_number(v) and (o == '' or is_number(o))


def clean_value(system: str, value: str)-> list:
    """
    Try to extract some sense from the categories in the input file.
    Extract strings that (in theory) are values in the classification system and  create a list of cleaned values.
    @param value:
    @return: list
    """
    # TODO allow for this to be used without passing through the system id
    value = value.replace(' ', '')
    # a value can contain "not 34.6 or (not 34.5), strip these out.
    value = value.partition('not')[0] if 'not' in value else value
    value.strip('(')
    outputs = list()
    if _is_acceptable(system, value):
        outputs.append(value.replace('.', '_'))

    elif 'CPA_' in value:
        outputs += clean_value(system, value.lstrip('CPA_'))

    elif 'OTHER' in value:
        outputs += clean_value(system, value.rstrip('OTHER'))

    elif '&' in value:
        v = value.split('&')
        for val in v:
            if v:
                outputs += clean_value(system, val)

    elif '+' in value:
        outputs += clean_value(system, value.replace('+', '&'))

    elif ',' in value:
        v = value.split(',')
        for val in v:
            if v:
                outputs += (clean_value(system, val))

    # for the case 12.4 - 7, we want to extract the 12., then loop from 4 - 7 prepending 12. to each.
    # we also want to catch the case 12.05 - 10, that's why this looks particularly complicated.
    elif '-' in value:
        left, _, right = value.partition('-')
        left = clean_value(system, left)[0]
        right = clean_value(system, right)[0]

        base_number = left[:-len(right)]
        if not _is_number(left) or not _is_number(right):
            raise ValueError("Both sies of the '-' must be numbers, value {0} not accepted".format(value))
        if len(right) <= len(left):
            # right = right[-1:]
            left = left[-len(right):]
        for i in range(int(left), int(right) + 1):
            format_string = "{0}{1:0" + str(len(right)) + "d}"
            outputs += clean_value(system, format_string.format(base_number, i))

    elif '/' in value:
        outputs += clean_value(system, value[:value.index('/')])

    # At this point we assume that the number is in the form "1", "14.3", "234.56" etc.
    else:
        match = _number_regex.search(value)
        if match:
            outputs += clean_value(system, match.group(0))
        else:
            # this will possibly go wrong but we're assuming that if there's no number at all then it's a top
            # level category of some description and we don't want it
            pass
            # outputs.append(value)
    return outputs


class TestCleanValue(unittest.TestCase):
    # TODO make tests to check for UNFCCC badness
    def test_range(self):
        test_case = clean_value("SIC4", "14.49-53")
        self.assertListEqual(test_case, ["14_49", "14_50", "14_51", "14_52", "14_53"])

    def test_smaller_range(self):
        test_case = clean_value("SIC4", "10.08-11")
        self.assertListEqual(test_case, ["10_08", "10_09", "10_10", "10_11"])

    def test_remove_other(self):
        test_case = clean_value("SIC4", "23OTHER")
        self.assertListEqual(test_case, ["23"])

    def test_not_(self):
        test_case = clean_value("SIC4", "23.4 not 23.47")
        self.assertListEqual(test_case,
                             ["23_4"]
                             )

    def test_and_(self):
        test_cast = clean_value("SIC4", "1 & 2")
        self.assertListEqual(test_cast, ["1", "2"])

    def test_strip_slash(self):
        test_case = clean_value("SIC4", "23.12/4")
        self.assertListEqual(test_case, ["23_12"])

    def test_leading_chars(self):
        test_case = clean_value("SITC4", "A05-A10")
        self.assertListEqual(test_case, ["05", "06", "07", "08", "09", "10"])

    def test_bad_range(self):
        #test_case = clean_value("SIC4", "12.5-1")
        self.assertRaises(ValueError, clean_value, "SIC4", "12.5-1")