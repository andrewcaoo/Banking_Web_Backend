account_permission = {
    'admin': 0,
    'employee': 1, 
    'client': 2
}

payment_type = {
    'fixed_interest' : 1,
    'reduced_debt': 2
}

interest_type = {
    'each_month': 1,
    'each_quarter': 2,
    'each_year': 3
}

payment_status = {
    'pending': 1,
    'processing': 2,
    'completed': 3,
    'expired': 4,
}

transaction_method = {
    'online': 1,
    'atm': 2,
    'cash': 3
}

transaction_status = {
    'prepare': 1,
    'processing': 2,
    'completed': 3,
    'failure': 4
}

loan_status = {
    'submitted': 1,
    'reviewed': 2,
    'approved': 3,
    'rejected': 4,
    'disbursed': 5,
    'bad_debt': 6,
    'completed': 7
}