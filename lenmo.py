def borrowerRequestLoan(amount, period):
    """
    borrower submit a request to have his leon
    :param amount: amount of the request leon
    :param period: period that borrower take to pay the leon back
    :return: object
    """

    # ammount value and period value should be positive :  abs(value) or raise ValueError
    if (amount <= 0):
        raise ValueError('Leon ammount must be greater than zero')
    if (period <= 0):
        raise ValueError('Leon period must be greater than zero')

    # send notification to Investor with new leon request from Borrower
    return {
        'leon_amount': amount,
        'leon_period': period,
        'leon_status': 'submited'
    }


def investorOffer(leon_amount, leon_period):
    """
    investore sumbit his offer base on leon ammount and period
    :param leon_amount: amount of the request leon
    :param leon_period: period that borrower take to pay the leon back
    :return: object
    """

    annual_rate_percentage = 15
    annual_rate = (15 * leon_amount) / 100
    leon_amount_after_adding_annual_rate = leon_amount + annual_rate

    # send notification to Borrower with new offer from Investor
    return {
        'annual_rate_percentage': annual_rate_percentage,
        'annual_rate': annual_rate,
        'leon_amount_after_adding_annual_rate': leon_amount_after_adding_annual_rate,
        'leon_period': leon_period,
    }


def borrowerResponseOffer(annual_rate_percentage,
                          annual_rate,
                          leon_amount_after_adding_annual_rate,
                          leon_period,
                          leon_amount):
    """
    borrower will accept/reject the investor offer
    :param annual_rate_percentage: investore offer annual rate percentage for the borrower leon
    :param annual_rate: amount of the annual rate calulated based on leon amount
    :param leon_amount_after_adding_annual_rate: leon amount with annual rate added to it
    :param leon_period: period that borrower take to pay the leon back
    :param leon_amount: amount of the request leon
    :return: object
    """

    # send notification to borrower and investore with leon status is accepted
    return {
        'leon_status': 'accepted',
        'leon_amount': leon_amount,
        'leon_period': leon_period,
        'annual_rate_percentage': annual_rate_percentage,
        'annual_rate': annual_rate,
        'leon_amount_after_adding_annual_rate': leon_amount_after_adding_annual_rate,
    }


def fundLoanFromInvestor(leon_status,
                         leon_amount,
                         leon_period,
                         annual_rate_percentage,
                         annual_rate,
                         leon_amount_after_adding_annual_rate,
                         lenom_fees, avialble_amount):
    """
    Getting fund from Investor for the borrower leon
    :param leon_status: current status for borrower lean
    :param leon_amount: amount of the request leon
    :param leon_period: period that borrower take to pay the leon back
    :param annual_rate_percentage: investore offer annual rate percentage for the borrower leon
    :param annual_rate: amount of the annual rate calulated based on leon amount
    :param leon_amount_after_adding_annual_rate: leon amount with annual rate added to it
    :param lenom_fees: lenom fees amount that investor will pay
    :return: object
    """
    if (leon_status != "accepted"):
        raise ValueError('Borrower Must Accept the Offer first')
    if (not checkInverstorBalance(leon_amount_after_adding_annual_rate, lenom_fees, avialble_amount)):
        raise ValueError('Leon amount Exceeded Investor Balance')

    # send notification to borrower and investore with leon status is Funded
    return {
        'leon_status': 'Funded',
        'leon_amount': leon_amount,
        'leon_period': leon_period,
        'annual_rate_percentage': annual_rate_percentage,
        'annual_rate': annual_rate,
        'leon_amount_after_adding_annual_rate': leon_amount_after_adding_annual_rate,
        'investor_total_fund': leon_amount_after_adding_annual_rate + lenom_fees
    }


def checkInverstorBalance(leon_amount_after_adding_annual_rate, lenom_fees, avialble_amount):
    """
    check if Investor balancce  can cover the required total amount for the leon
    :param leon_amount_after_adding_annual_rate: leon amount with annual rate added to it
    :param lenom_fees: lenom fees amount that investor will pay
    :param avialble_amount: investor balance amount
    :return: boolean
    """
    return (leon_amount_after_adding_annual_rate + lenom_fees) <= avialble_amount


def leonSchedule(leon_status, leon_amount, leon_period, annual_rate_percentage, annual_rate,
                 leon_amount_after_adding_annual_rate, investor_total_fund, lenom_fees):
    """
    schedule the leon for certain period
    :param leon_status: current status for borrower lean
    :param leon_amount: amount of the request leon
    :param leon_period: period that borrower take to pay the leon back
    :param annual_rate_percentage: investore offer annual rate percentage for the borrower leon
    :param annual_rate: amount of the annual rate calulated based on leon amount
    :param leon_amount_after_adding_annual_rate: leon amount with annual rate added to it
    :param investor_total_fund: total amount that investor will pay
    :param lenom_fees: lenom fees amount that investor will pay
    :return: object
    """

    if (leon_status != "Funded"):
        raise ValueError('Investor must fund the leon first')

    # save in queing system the leon data to triget events base on the leon period
    # send notification to Borrower and Investore with leon status is completed
    return {
        'leon_status': 'Completed',
        'leon_amount': leon_amount,
        'leon_period': leon_period,
        'annual_rate_percentage': annual_rate_percentage,
        'annual_rate': annual_rate,
        'leon_amount_after_adding_annual_rate': leon_amount_after_adding_annual_rate,
        'investor_total_fund': investor_total_fund,
        'lenom_fees': lenom_fees
    }


def processLeon(leon_amount, leon_period, lenom_fees, avialble_amount):
    """

    :param leon_amount: amount of the request leon
    :param leon_period: period that borrower take to pay the leon back
    :param lenom_fees: lenom fees amount that investor will pay
    :param avialble_amount: Investor balance amount
    :return: object
    """

    # borrower create request to get a leon
    borrower_leon = borrowerRequestLoan(leon_amount, leon_period)

    # check if borrower has submit his request
    if (not borrower_leon["leon_status"] == "submited"):
        raise ValueError('Borrower Must Submit request first')

    # get investor offer for borrower submitted leon request
    investor_offer = investorOffer(borrower_leon["leon_amount"], borrower_leon["leon_period"])

    # get acceptace or rejectance on the investore offer from borrower
    borrower_response = borrowerResponseOffer(investor_offer["annual_rate_percentage"],
                                              investor_offer["annual_rate"],
                                              investor_offer["leon_amount_after_adding_annual_rate"],
                                              investor_offer["leon_period"], leon_amount)

    # fund leon with annual rate and lenom fees from investore balance
    fund_loan = fundLoanFromInvestor(borrower_response["leon_status"],
                                     borrower_response["leon_amount"],
                                     borrower_response["leon_period"],
                                     borrower_response["annual_rate_percentage"],
                                     borrower_response["annual_rate"],
                                     borrower_response["leon_amount_after_adding_annual_rate"],
                                     lenom_fees, avialble_amount)

    # schedule the leon
    leon_schedule = leonSchedule(fund_loan["leon_status"],
                                 fund_loan["leon_amount"],
                                 fund_loan["leon_period"],
                                 fund_loan["annual_rate_percentage"],
                                 fund_loan["annual_rate"],
                                 fund_loan["leon_amount_after_adding_annual_rate"],
                                 fund_loan["investor_total_fund"],
                                 lenom_fees)

    return leon_schedule



