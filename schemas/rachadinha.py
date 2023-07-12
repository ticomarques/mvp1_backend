from pydantic import BaseModel
from typing import Optional, List
from model.rachadinha import Rachadinha

from schemas import LanceSchema


class RachadinhaSchema(BaseModel):
    """ Define como uma nova rachadinha a ser inserida deve ser representado
    """
    id: int = 1
    nome: str = "Banana Prata"
    link: str = "http://www.teste.com.br"
    quantidade_participantes: Optional[int] = 4
    valor: float = 12.50


class RachadinhaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do item a ser rachado.
    """
    nome: str = "Teste"


class ListagemRachadinhasSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    rachadinhas:List[RachadinhaSchema]


def apresenta_produtos(rachadinhas: List[Rachadinha]):
    """ Retorna uma representação do produto seguindo o schema definido em
        RachadinhaViewSchema.
    """
    result = []
    for rachadinha in rachadinhas:
        result.append({
            "id": rachadinha.id,
            "nome": rachadinha.nome,
            "link":  rachadinha.link,
            "quantidade_participantes": rachadinha.quantidade_participantes,
            "valor": rachadinha.valor,
        })

    return {"rachadinhas": result}


class RachadinhaViewSchema(BaseModel):
    """ Define como uma rachadinha será retornada: rachadinha + lances.
    """
    id: int = 1
    nome: str = "Banana Prata"
    link: str = "http://www.site.com.br"
    quantidade_participantes: Optional[int] = 12
    valor: float = 12.50
    total_cometarios: int = 1
    lances:List[LanceSchema]


class RachadinhaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_produto(rachadinha: Rachadinha):
    """ Retorna uma representação do produto seguindo o schema definido em
        RachadinhaViewSchema.
    """
    return {
        "id": rachadinha.id,
        "nome": rachadinha.nome,
        "link": rachadinha.link,
        "quantidade_participantes": rachadinha.quantidade_participantes,
        "valor": rachadinha.valor,
        "total_cometarios": len(rachadinha.lances),
        "lances": [{"texto": c.texto} for c in rachadinha.lances]
    }
