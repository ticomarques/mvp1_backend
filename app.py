from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Rachadinha, Lance
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Rachadinha", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
rachadinha_tag = Tag(name="Rachadinha", description="CRUD de rachadinha")
lance_tag = Tag(name="Lance", description="Lances dentro de uma rachadinha")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/rachadinha', tags=[rachadinha_tag],
          responses={"200": RachadinhaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: RachadinhaSchema):
    """Adiciona uma rachadinha 

    Retorna uma representação de rachadinhas.
    {
        nome: "Abacaxi",
        link: "http://www.google.com.br",
        quantidade_participantes: 2,
        valor: 2.50
    }

    """
    rachadinha = Rachadinha(
        nome = request.json['nome'],
        link = request.json['link'],
        quantidade_participantes = request.json['quantidade_participantes'],
        valor = request.json['valor'])
    logger.debug(f"Adicionando produto de nome: '{rachadinha.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando uma rachadinha
        session.add(rachadinha)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado rachadinha de nome: '{rachadinha.nome}'")
        return apresenta_produto(rachadinha), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Rachadinha de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar rachadinha '{rachadinha.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar rachadinha '{rachadinha.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/rachadinhas', tags=[rachadinha_tag],
         responses={"200": ListagemRachadinhasSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todas as rachadinhas cadastradas

    Retorna uma representação da listagem de rachadinhas.
    """
    logger.debug(f"Coletando rachdinhas")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    rachadinhas = session.query(Rachadinha).all()

    if not rachadinhas:
        # se não há rachadinhas cadastrados
        return {"rachadinhas": []}, 200
    else:
        logger.debug(f"%d Rachadinhas econtradas" % len(rachadinhas))
        # retorna a representação de produto
        print(rachadinhas)
        return apresenta_produtos(rachadinhas), 200


@app.get('/rachadinha', tags=[rachadinha_tag],
         responses={"200": RachadinhaViewSchema, "404": ErrorSchema})
def get_produto(query: RachadinhaBuscaSchema):
    """Faz a busca por uma Rachadinha a partir do id da rachadinha

    Retorna uma representação das rachadinhas e lances associados.
    """
    rachadinha_id = query.nome
    logger.debug(f"Coletando dados sobre produto #{rachadinha_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    rachadinha = session.query(Rachadinha).filter(Rachadinha.nome == rachadinha_id).first()

    if not rachadinha:
        # se a rachadinha não foi encontrado
        error_msg = "Rachadinha não encontrada na base :/"
        logger.warning(f"Erro ao buscar produto '{rachadinha_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{rachadinha.nome}'")
        # retorna a representação da rachadinha
        return apresenta_produto(rachadinha), 200


@app.delete('/rachadinha', tags=[rachadinha_tag],
            responses={"200": RachadinhaDelSchema, "404": ErrorSchema})
def del_produto(query: RachadinhaBuscaSchema):
    """Deleta uma rachadinha a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    rachadinha_nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando dados sobre produto #{rachadinha_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Rachadinha).filter(Rachadinha.nome == rachadinha_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{rachadinha_nome}")
        return {"message": "Produto removido", "id": rachadinha_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{rachadinha_nome}', {error_msg}")
        return {"message": error_msg}, 404












@app.post('/lance', tags=[lance_tag],
          responses={"200": LanceSchema, "404": ErrorSchema})
def add_comentario(form: LanceSchema):
    """Adiciona de um novo lance à um produtos cadastrado na base identificado pelo id

    Retorna uma representação dos produtos e comentários associados.
    """
    rachadinha_id  = form.rachadinha_id
    logger.debug(f"Adicionando comentários ao produto #{rachadinha_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    rachadinha = session.query(Rachadinha).filter(Rachadinha.id == rachadinha_id).first()

    if not rachadinha:
        # se produto não encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao produto '{rachadinha_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando o comentário
    texto = form.texto
    lance = Lance(texto)

    # adicionando o comentário ao produto
    rachadinha.adiciona_comentario(lance)
    session.commit()

    logger.debug(f"Adicionado comentário ao produto #{rachadinha_id}")

    # retorna a representação de produto
    return apresenta_produto(rachadinha), 200





