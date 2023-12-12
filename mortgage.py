"""Perform fixed-rate mortgage calculations."""

from argparse import ArgumentParser
import math
import sys


def get_min_payment(mortgage_amount, annual_interest_rate, years=30, num_annual_payments=12):
    """ Calculate the minimum mortgage payment 
    
    Args:
        mortgage_amount (float): the total amount of mortgage.
        annual_interest_rate (float): the annual interest rate.
        years (int): the mortgage term in years.
        num_annual_payments (int): the number of payments per year.
        
    Returns:
        minimum_payment (int): the minimum payment amount rounded to the nearest number.
             
    """
    # r is the interest rate per payment
    r = annual_interest_rate / num_annual_payments
    
    # n is the total number of payments 
    n = years * num_annual_payments
    
    minimum_payment = mortgage_amount * r * (1 + r) ** n / (((1 + r) ** n) - 1)
    # return the minimum payment and round to closest integer
    return math.ceil(minimum_payment)

def interest_due(balance, annual_interest_rate, num_annual_payments=12):
    """ Compute the amount of interest due in the next payment
    
    Args:
        balance (float): the remaining balance of mortgage.
        annual_interest_rate (float): the annual interest rate.
        num_annual_payments (int): the number of payments per year (default is 12).
        
    Returns:
        interest_due (float): the interest amount due in the next payment.
             
    """
    # r is the interest rate per payment 
    r = annual_interest_rate / num_annual_payments
    interest_due = balance * r
    return interest_due

def remaining_payments(balance, annual_interest_rate, target_payment, num_annual_payments=12):

    """ Calculate the number of payments required to pay off the mortgage.
    
    Args:
        balance (float): the remaining balance of mortgage.
        annual_interest_rate (float): the annual interest rate.
        target_payment (float): the users desired payment amount.
        num_annual_payments (int): the number of payments per year (default is 12).
        
    Returns:
        payments (int): the number of needed payments for mortgage to be paid off.
             
    """
    payments = 0
    # Checks to see if there is any balance remaining
    while balance > 0:
        # Determines what portion of next payment is interest
        interest_due_value = interest_due(balance, annual_interest_rate, num_annual_payments)
        # Gets minimum payment is there is no target payment
        if target_payment is None:
            payment = get_min_payment(balance, annual_interest_rate)
        else:
            # Ensures the payment is not more than the remaining balance
            payment = min(target_payment, balance + interest_due_value)
        # Balance is reduced and payment counter gets increased by 1
        balance -= (payment - interest_due_value)
        payments += 1
    return payments

def main(mortgage_amount, annual_interest_rate, years=30, num_annual_payments=12, target_payment=None):
    """ Calculate mortgage details and display results.
    
    Args:
        mortgage_amount (float): the total amount of mortgage.
        annual_interest_rate (float): the annual interest rate.
        years (int): the mortgage term in years (default is 30).
        num_annual_payments (int): the number of payments per year (default is 12).
        target_payment (float, optional): the users desired payment amount (default is none).
        
    Side effects:
        Prints the minimum payment amount as well as user target payment (if applicable) and amount of payments needed to fulfill balance.
             
    """
    # Find and print the minimum payment
    minimum_payment = get_min_payment(mortgage_amount, annual_interest_rate, years, num_annual_payments)
    print(f"Minimum Payment: ${minimum_payment}")
    
    # If there is no minimum payment, set the target payment to minimum payment
    if target_payment is None:
        target_payment = minimum_payment
        
    # 
    if target_payment < minimum_payment:
        print("Your target payment is less than the minimum payment for this mortgage.")
    else:
        # Calculate and display the total number of payments required
        total_payments = remaining_payments(mortgage_amount, annual_interest_rate, target_payment, num_annual_payments)
        print(f"If you make payments of ${target_payment}, you will pay off the mortgage in {total_payments} payments.")


def parse_args(arglist):
    """Parse and validate command-line arguments.
    
    This function expects the following required arguments, in this order:
    
        mortgage_amount (float): total amount of a mortgage
        annual_interest_rate (float): the annual interest rate as a value
            between 0 and 1 (e.g., 0.035 == 3.5%)
        
    This function also allows the following optional arguments:
    
        -y / --years (int): the term of the mortgage in years (default is 30)
        -n / --num_annual_payments (int): the number of annual payments
            (default is 12)
        -p / --target_payment (float): the amount the user wants to pay per
            payment (default is the minimum payment)
    
    Args:
        arglist (list of str): list of command-line arguments.
    
    Returns:
        namespace: the parsed arguments (see argparse documentation for
        more information)
    
    Raises:
        ValueError: encountered an invalid argument.
    """
    # set up argument parser
    parser = ArgumentParser()
    parser.add_argument("mortgage_amount", type=float,
                        help="the total amount of the mortgage")
    parser.add_argument("annual_interest_rate", type=float,
                        help="the annual interest rate, as a float"
                             " between 0 and 1")
    parser.add_argument("-y", "--years", type=int, default=30,
                        help="the term of the mortgage in years (default: 30)")
    parser.add_argument("-n", "--num_annual_payments", type=int, default=12,
                        help="the number of payments per year (default: 12)")
    parser.add_argument("-p", "--target_payment", type=float,
                        help="the amount you want to pay per payment"
                        " (default: the minimum payment)")
    # parse and validate arguments
    args = parser.parse_args()
    if args.mortgage_amount < 0:
        raise ValueError("mortgage amount must be positive")
    if not 0 <= args.annual_interest_rate <= 1:
        raise ValueError("annual interest rate must be between 0 and 1")
    if args.years < 1:
        raise ValueError("years must be positive")
    if args.num_annual_payments < 0:
        raise ValueError("number of payments per year must be positive")
    if args.target_payment and args.target_payment < 0:
        raise ValueError("target payment must be positive")
    
    return args


if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    main(args.mortgage_amount, args.annual_interest_rate, args.years,
         args.num_annual_payments, args.target_payment)
