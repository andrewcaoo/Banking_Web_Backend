from typing import Annotated, Any
from starlette.config import Config
import os
from datetime import datetime
from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

from ...api.dependencies import get_current_superuser, get_current_user, verify_admin_acc, login_require, verify_admin_employee
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_transaction import crud_transaction
from ...schemas.transaction import TransactionRead, TransactionCreate, TransactionCreateInternal, TransactionUpdate, TransactionUpdateInternal, TransactionReadInternal
from ...core.constants import account_permission, transaction_method, transaction_status
from ...schemas.order import Order
from ..helper import get_payment_url, Vnpay

# Load the env variables
current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", "..","..", ".env")
config = Config(env_path)

router = APIRouter(tags=["Online transaction"])

@router.post("/get_order")
async def get_order(
    request: Request, 
    values: Order,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None, Depends(login_require)]
) -> dict:
    try:
        order_id = datetime.now().strftime('%Y%m%d%H%M%S')

        new_transaction = TransactionCreate(**{
            'amount': values.amount,
            'method': transaction_method['online'],
            'status':transaction_status['prepare'],
            'date': datetime.now(),
            'payment_id': values.payment_id
        })

        created_new_transaction = await crud_transaction.create(db=db, object=new_transaction)
        order_id = str(created_new_transaction.transaction_id) + '-' + str(values.payment_id)

        # Replace with your actual config values
        tmn_code = config('vnp_TmnCode')
        secret_key = config('vnp_HashSecret')
        vnp_url = config('vnp_Url') # Adjust this URL as per your environment
        return_url = config('vnp_ReturnUrl') # Replace with your return URL
        # Prepare the parameters
        now = datetime.now()
        create_date = now.strftime('%Y%m%d%H%M%S')
       
        locale = values.language if values.language else 'vn'
        curr_code = 'VND'

        vnp_params = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': tmn_code,
            'vnp_Locale': locale,
            'vnp_CurrCode': curr_code,
            'vnp_TxnRef': order_id,
            'vnp_OrderInfo': values.order_description,
            'vnp_OrderType': values.order_type,
            'vnp_Amount': (int(values.amount)*1000000) * 100,  # Convert to integer amount in cents
            'vnp_ReturnUrl': return_url,
            'vnp_CreateDate': create_date,
            'vnp_IpAddr': '127.0.0.1',  # Replace with actual IP address
        }

        if values.bank_code:
            vnp_params['vnp_BankCode'] = values.bank_code

        # Build the final URL using the get_payment_url function
        payment_url = get_payment_url(vnp_url, secret_key, vnp_params)

        return {'order_url': payment_url,
                "return_code": 1}
        print(request)
        return {}
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))


@router.get("/payment_return")
async def get_order(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict:
    try:
        inputData = dict(request.query_params)

        if inputData:
            vnp = Vnpay()
            vnp.responseData = inputData

            order_id = inputData.get('vnp_TxnRef', '')
            amount = (float(inputData.get('vnp_Amount', 0))/1000000) / 100
            order_desc = inputData.get('vnp_OrderInfo', '')
            vnp_TransactionNo = inputData.get('vnp_TransactionNo', '')
            vnp_ResponseCode = inputData.get('vnp_ResponseCode', '')
            vnp_TmnCode = inputData.get('vnp_TmnCode', '')
            vnp_PayDate = inputData.get('vnp_PayDate', '')
            vnp_BankCode = inputData.get('vnp_BankCode', '')
            vnp_CardType = inputData.get('vnp_CardType', '')

            secret_key =  config('vnp_HashSecret') # Replace with your actual VNPAY secret key
            transaction_id = int(order_id.split('-')[0])

            global values
            db_tran = await crud_transaction.get(db=db, schema_to_select=TransactionReadInternal, transaction_id=transaction_id)
            if db_tran is None:
                raise NotFoundException()
            if vnp.validate_response(secret_key):
                if vnp_ResponseCode == "00":
                    values = {
                        'status': transaction_status['completed'],
                        'method': transaction_method['online'],
                        'amount': amount,
                        'payment_id': int(order_id.split('-')[1])
                    }
                    await crud_transaction.update(db=db, object=TransactionUpdate(**values), transaction_id=transaction_id)
                    return JSONResponse({
                        "title": "Kết quả thanh toán",
                        "result": "Thành công",
                        "order_id": order_id,
                        "amount": amount,
                        "order_desc": order_desc,
                        "vnp_TransactionNo": vnp_TransactionNo,
                        "vnp_ResponseCode": vnp_ResponseCode
                    })
                    
                else:
                    values = {
                        'status': transaction_status['failure'],
                        'method': transaction_method['online'],
                        'amount': amount,
                        'payment_id': int(order_id.split('-')[1])
                    }
                    await crud_transaction.update(db=db, object=TransactionUpdate(**values), transaction_id=transaction_id)
                    return JSONResponse({
                        "title": "Kết quả thanh toán",
                        "result": "Lỗi",
                        "order_id": order_id,
                        "amount": amount,
                        "order_desc": order_desc,
                        "vnp_TransactionNo": vnp_TransactionNo,
                        "vnp_ResponseCode": vnp_ResponseCode
                    })
            else:
                values = {
                        'status': transaction_status['failure'],
                        'method': transaction_method['online'],
                        'amount': amount,
                        'payment_id': int(order_id.split('-')[1])
                    }
                await crud_transaction.update(db=db, object=TransactionUpdate(**values), transaction_id=transaction_id)
                return JSONResponse({
                    "title": "Kết quả thanh toán",
                    "result": "Lỗi",
                    "order_id": order_id,
                    "amount": amount,
                    "order_desc": order_desc,
                    "vnp_TransactionNo": vnp_TransactionNo,
                    "vnp_ResponseCode": vnp_ResponseCode,
                    "msg": "Sai checksum"
                })
        else:
            values = {
                        'status': transaction_status['failure'],
                        'method': transaction_method['online'],
                        'amount': amount,
                        'payment_id': int(order_id.split('-')[1])
                    }
            await crud_transaction.update(db=db, object=TransactionUpdate(**values), transaction_id=transaction_id)
            return JSONResponse({
                "title": "Kết quả thanh toán",
                "result": ""
            })

    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))