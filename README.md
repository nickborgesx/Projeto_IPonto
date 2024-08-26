# Ponto Eletrônico API

Este projeto consiste em uma API em microsserviços no qual foi desenvolvida para gerenciar pontos eletrônicos de funcionários em relação a escala de trabalho. Ele está dividido em dois componentes principais: iPonto e msAuthentication. Cada componente possui suas funcionalidades específicas e está organizado de forma modular, permitindo uma fácil manutenção e expansão.

![Ilustração do SQL](drawsql.png)

### Módulo Company (Empresa)
Função: Gerencia as empresas registradas no sistema.

- Endpoint: POST /api/v1/company

Descrição: Este endpoint cria uma nova empresa no sistema utilizando os dados fornecidos no JSON.
_____________________________________________________________________________
### Módulo Employees (Funcionários)
Função: Gerencia os funcionários da empresa.

- Endpoint: POST /api/v1/employee

  Descrição: Este endpoint adiciona um novo funcionário à empresa especificada.

- Endpoint: POST /api/v1/employee/{id}/point

  Descrição: Este endpoint permite que o funcionário bata o ponto eletrônico. É possível bater até 4 pontos por dia.

- Endpoint: GET /api/v1/employees/

  Descrição: Este endpoint lista todos os funcionários e suas descrições.

- Endpoint: PUT /api/v1/employee/<int:id>/

  Descrição: Este endpoint edita os dados do funcionário.
_____________________________________________________________________________
### Módulo Roles (Cargos)
Função: Gerencia os cargos disponíveis para os funcionários.

- Endpoint: POST /api/v1/role

  Descrição: Este endpoint cria um novo cargo no sistema.
_____________________________________________________________________________
### Módulo Scale (Escalas)
Função: Gerencia as escalas de trabalho dos funcionários.

- Endpoint: POST /api/v1/scale

  Descrição: Cria as escalas dos funcionários dado a lista com os ID's dos funcionários.

- Endpoint: GET /api/v1/scale

  Descrição: Retorna as escalas de trabalho cadastradas no sistema.
_____________________________________________________________________________
### Módulo User (Usuários)
Função: Gerencia a autenticação e autorização dos usuários do sistema.

- Endpoint: POST /api/v1/authentication/token/

  Descrição: Este endpoint gera um token do usuário.

- Endpoint: POST /api/v1/authentication/validation/

  Descrição: Este endpoint valida se o token ainda está disponível ou não.
_____________________________________________________________________________
### Bibliotecas e Ferramentas Utilizadas
- Python
- Flask
- Psycopg2
- PostgreSQL
- Postman
- pyjwt
- drawsql
