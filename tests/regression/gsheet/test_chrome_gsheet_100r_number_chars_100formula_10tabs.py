from lib.perfBaseTest import PerfBaseTest


class TestSikuli(PerfBaseTest):

    def setUp(self):
        super(TestSikuli, self).setUp()

    def test_chrome_gsheet_100r_number_chars_100formula_10tabs(self):
        self.test_url = self.env.GSHEET_TEST_URL_SPEC % self.env.TEST_TARGET_ID_100R_NUMBER_ENCHAR_100FORMULA_10TABS
        self.sikuli_status = self.sikuli.run_test(self.env.test_name, self.env.output_name, test_target=self.test_url, script_dp=self.env.test_script_py_dp)
