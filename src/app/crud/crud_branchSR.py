from fastcrud import FastCRUD

from ..models.branch_service_region import BranchServiceRegion 
from ..schemas.branch_service_region import BranchSRCreateInternal, BranchSRDelete, BranchSRUpdate, BranchSRUpdateInternal 

CRUDBranchSR = FastCRUD[BranchServiceRegion, BranchSRCreateInternal, BranchSRDelete, BranchSRUpdate, BranchSRUpdateInternal]
crud_branchSR = CRUDBranchSR(BranchServiceRegion)
