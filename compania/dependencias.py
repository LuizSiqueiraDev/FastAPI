from fastapi import Header, HTTPException


async def obter_cabecalho_token(token_interno: str = Header(...)):
    if token_interno != "permitido":
        raise HTTPException(status_code=400, detail="Cabeçalho do token-interno inválido.")