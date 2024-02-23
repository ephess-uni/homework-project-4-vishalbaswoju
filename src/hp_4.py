# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    dates = [datetime.strptime(old_date, "%Y-%m-%d").strftime('%d %b %Y') for old_date in old_dates]    
    return dates

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError()
    ranges = []
    for x in range(n):
        ranges.append(datetime.strptime(start, '%Y-%m-%d') + timedelta(days=x))
    return ranges


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    headers = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    fess_dict = defaultdict(float)
    with open(infile, 'r') as fl:
        lines_data = DictReader(fl, fieldnames=headers)
        rows = [row for row in lines_data]
    rows.pop(0)
    for book in rows:
        patronID = book['patron_id']
        original_date_due = datetime.strptime(book['date_due'], "%m/%d/%Y")
        returned_due_date = datetime.strptime(book['date_returned'], "%m/%d/%Y")
        delay_in_days = (returned_due_date - original_date_due).days
        
        fess_dict[patronID]+= 0.25 * delay_in_days if delay_in_days > 0 else 0.0
            
    final_line_format = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in fess_dict.items()
    ]
    with open(outfile, 'w') as fl:
        parton_id_late_fee = DictWriter(fl,['patron_id', 'late_fees'])
        parton_id_late_fee.writeheader()
        parton_id_late_fee.writerows(final_line_format)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
