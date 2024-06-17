from fastcrud import FastCRUD

from ..models.branch import Branch 
from ..schemas.branch import BranchCreateInternal, BranchDelete, BranchUpdate, BranchUpdateInternal 

CRUDBranch = FastCRUD[Branch, BranchCreateInternal, BranchDelete, BranchUpdate, BranchUpdateInternal]
crud_branch = CRUDBranch(Branch)
