from fastapi import APIRouter, Depends
from compania import dependencias

router = APIRouter(
    prefix="/companiasapi",
    tags=["Companias API"],
    dependencies=[Depends(dependencias.obter_cabecalho_token)],
    responses={418: {"descrição": "Somente uso interno"}}
)


@router.get("/")
async def nome_compania():
    return {"nome_compania": "Uma compania qualquer, LCD"}


@router.get("/")
async def numero_de_empregados():
    return 157