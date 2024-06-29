from fastcrud import FastCRUD

from ..models.region import Region 
from ..schemas.region import RegionCreateInternal, RegionDelete, RegionUpdate, RegionUpdateInternal

CRUDRegion = FastCRUD[Region, RegionCreateInternal, RegionUpdate, RegionUpdateInternal, RegionDelete]
crud_region = CRUDRegion(Region)
