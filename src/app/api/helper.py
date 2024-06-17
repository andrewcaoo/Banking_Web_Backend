from ..schemas.base_account import BaseAccountRead

def check_permission(acc: BaseAccountRead, permission: int) -> bool:
    return acc['permission'] == permission