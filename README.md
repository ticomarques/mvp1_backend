# MVP 1 (Backend) - Engenharia de Software PUC-Rio (2023.2)

O rachadinha.com é uma ferramenta que nasceu com objetivo de democratizar o acesso a produtos, permitindo que pessoas possam rachar o valor e produtos. A ferramenta é simples, e de fácil uso, basta criar uma rachadinha e aguardar que outros usuários entrem na rachadinha.

---


# Backend tecnologias

O backend deste projeto foi desenvolido em Python com SQL Alchemy. Todas as dependencias podem ser consultadas no arquivo requirements.



## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

1- Criar
2- Ativar
3- Desativar

Como criar um virtal env:
```
python3 -m venv .env 
```

Como ativar um virtal env:
```
source env/bin/activate 
```

Como desativar um virtal env:
```
deactivate 
```

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 8000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 8000 --reload
```

Abra o [http://localhost:8000/#/](http://localhost:8000/#/) no navegador para verificar o status da API em execução.
