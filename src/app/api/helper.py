from ..schemas.base_account import BaseAccountRead

# def check_permission(acc: BaseAccountRead, permission: int) -> bool:
#     return acc['permission'] == permission

def convert_interest_by_interest_each_month(interest: int, interest_type: int):
    if interest_type == 2:
        return interest / 3
    elif interest_type == 3:
        return interest / 12
    else:
        return interest

