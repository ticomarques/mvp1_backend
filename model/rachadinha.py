from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Lance


class Rachadinha(Base):
    __tablename__ = 'rachadinha'

    id = Column("pk_rachadinha", Integer, primary_key=True)
    nome = Column(String(140))
    link = Column(String(140))
    quantidade_participantes = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a rachadinha e o lance.
    # Essa relação é implicita, não está salva na tabela 'rachadinha',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    lances = relationship("Lance")

    def __init__(self, nome:str, link:str, quantidade_participantes:int, valor:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma rachadinha

        Arguments:
            nome: nome do produto para entrar na rachadinha.
            link: site do produto a ser rachado.
            quantidade_participantes: quantidade de participantes para essa rachadinha.
            valor: valor do produto a ser rachado.
            data_insercao: data de quando a rachadinha foi inserida no sistema

            exemplo de corpo de requisição (JSON):
            {
                nome: "nome do produto",
                link: "http://www.teste.com.br",
                quantidade_participantes: 4,
                valor: 389,90
            }

        """
        self.nome = nome
        self.link = link
        self.quantidade_participantes = quantidade_participantes
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, lance:Lance):
        """ Adiciona um novo lance a rachadinha
        """
        self.lances.append(lance)

