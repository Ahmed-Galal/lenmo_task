import unittest
from lenmo import fundLoanFromInvestor, leonSchedule, processLeon


class MyTestCase(unittest.TestCase):

    # test loan status in fund the loan function
    def test_fundLoanFromInvestor(self):
        leon_status = "submited"
        leon_amount = 5 * 1000
        leon_period = 6
        annual_rate_percentage = 15
        annual_rate = 750
        leon_amount_after_adding_annual_rate = 575
        lenom_fees = 3
        avialble_amount = 9 * 1000

        with self.assertRaises(ValueError) as context:
            fundLoanFromInvestor(leon_status,
                                 leon_amount,
                                 leon_period,
                                 annual_rate_percentage,
                                 annual_rate,
                                 leon_amount_after_adding_annual_rate,
                                 lenom_fees, avialble_amount)

        self.assertTrue('Borrower Must Accept the Offer first' in str(context.exception))

    # test loan status in leonSchedule function
    def test_leonSchedule(self):
        leon_status = "submited"
        leon_amount = 5 * 1000
        leon_period = 6
        annual_rate_percentage = 15
        annual_rate = 750
        leon_amount_after_adding_annual_rate = 575
        lenom_fees = 3
        investor_total_fund = 5753

        with self.assertRaises(ValueError) as context:
            leonSchedule(leon_status, leon_amount, leon_period, annual_rate_percentage, annual_rate,
             leon_amount_after_adding_annual_rate, investor_total_fund, lenom_fees)

        self.assertTrue('Investor must fund the leon first' in str(context.exception))

    # test submit negative leon ammount
    def test_negative_leon_amount(self):
        leon_amount = -5 * 1000
        leon_period = 6
        lenom_fees = 3
        avialble_amount = 900 * 1000
        with self.assertRaises(ValueError) as context:
            processLeon(leon_amount, leon_period, lenom_fees, avialble_amount)

        self.assertTrue('Leon ammount must be greater than zero' in str(context.exception))

    # test submit negative leon period
    def test_negative_leon_period(self):
        leon_amount = 5 * 1000
        leon_period = -6
        lenom_fees = 3
        avialble_amount = 900 * 1000
        with self.assertRaises(ValueError) as context:
            processLeon(leon_amount, leon_period, lenom_fees, avialble_amount)

        self.assertTrue('Leon period must be greater than zero' in str(context.exception))

    # test investore balance is less than leon amount
    def test_investor_balance_amount(self):
        leon_amount = 5 * 1000
        leon_period = 6
        lenom_fees = 3
        avialble_amount = 1000
        with self.assertRaises(ValueError) as context:
            processLeon(leon_amount, leon_period, lenom_fees, avialble_amount)

        self.assertTrue('Leon amount Exceeded Investor Balance' in str(context.exception))

    # test submit leon
    def test_processLeon(self):
        leon_amount = 5 * 1000
        leon_period = 6
        lenom_fees = 3
        avialble_amount = 900 * 1000
        res = processLeon(leon_amount, leon_period, lenom_fees, avialble_amount)
        expect_json = {
            'leon_status': 'Completed',
            'leon_amount': 5000,
            'leon_period': 6,
            'annual_rate_percentage': 750,
            'annual_rate': 15,
            'leon_amount_after_adding_annual_rate': 5750,
            'investor_total_fund': 5753,
            'lenom_fees': 3
        }
        self.assertTrue(expect_json, res)


if __name__ == '__main__':
    unittest.main()
