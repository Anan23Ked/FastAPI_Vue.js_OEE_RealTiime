from fastapi import APIRouter, Depends, HTTPException

from operations.oee import oee_calculation


router = APIRouter(
    prefix="/oee",
    tags=["oee"],
    # dependencies=[Depends(get_token_hearer)]
    responses={404:{"description" :"Not found"}},
)

@router.get("/")
async def home():
    print("router says hi")
    return {"router-msg":"hello from the router side"}


@router.get("/machine/{machineClicked}")
def get_machine(machineClicked : str):
    oee_res = oee_calculation(machineClicked)
    # print(oee_res)
    # return{"clicked machine from backend is" : oee_res}
    return{"machine clicked from router backend": machineClicked, "oee result frtom routewr backend": oee_res}

