from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Lance(Base):
    __tablename__ = 'lance'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o lance e uma rachadinha.
    # Aqui está sendo definido a coluna 'rachadinha' que vai guardar
    # a referencia a rachadinha, a chave estrangeira que relaciona
    # uma rachadinha ao lance.
    rachadinha = Column(Integer, ForeignKey("rachadinha.pk_rachadinha"), nullable=False)

    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Lance

        Argumentos:
            texto: o texto de um lance.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
