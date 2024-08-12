# Teste de conhecimentos adquiridos no Treinamento Python

### Instrutor: Adriano Mota e Souza

## Descritivo para Implementação de Aplicação de um Blog

#### Objetivo

O objetivo deste teste técnico é avaliar sua capacidade de implementar uma aplicação web utilizando o framework Flask, com foco em boas práticas de desenvolvimento, integração de bibliotecas e gerenciamento de banco de dados. A aplicação a ser desenvolvida será um blog com funcionalidades básicas e administração.

#### Requisitos

1. **Configuração do Ambiente**

   - Utilize Docker para gerenciar a configuração do ambiente.
   - Crie um `Dockerfile` e um arquivo `docker-compose.yml` para facilitar a criação e a execução dos containers.
   - O banco de dados deve ser PostgreSQL.
2. **Modelagem e Persistência de Dados**

   - Utilize SQLAlchemy para a modelagem das entidades.
   - Crie as seguintes entidades no banco de dados:
     - **User**
       - `id`: Integer, chave primária, auto incremento.
       - `username`: String, único, obrigatório, máximo 80 caracteres.
       - `email`: String, único, obrigatório, máximo 120 caracteres.
       - `password_hash`: String, obrigatório, armazenar a senha criptografada.
       - `created_at`: DateTime, obrigatório, data de criação do usuário.
       - `updated_at`: DateTime, data da última atualização do usuário.
     - **Post**
       - `id`: Integer, chave primária, auto incremento.
       - `title`: String, obrigatório, máximo 200 caracteres.
       - `body`: Text, obrigatório, conteúdo da postagem.
       - `author_id`: Integer, obrigatório, chave estrangeira referenciando `User.id`.
       - `created_at`: DateTime, obrigatório, data de criação da postagem.
       - `updated_at`: DateTime, data da última atualização da postagem.
     - **Comment**
       - `id`: Integer, chave primária, auto incremento.
       - `body`: Text, obrigatório, conteúdo do comentário.
       - `post_id`: Integer, obrigatório, chave estrangeira referenciando `Post.id`.
       - `author_id`: Integer, obrigatório, chave estrangeira referenciando `User.id`.
       - `created_at`: DateTime, obrigatório, data de criação do comentário.
       - `updated_at`: DateTime, data da última atualização do comentário.
     - **Like**
       - `id`: Integer, chave primária, auto incremento.
       - `post_id`: Integer, obrigatório, chave estrangeira referenciando `Post.id`.
       - `user_id`: Integer, obrigatório, chave estrangeira referenciando `User.id`.
       - `created_at`: DateTime, obrigatório, data de criação da curtida.
3. **Autenticação e Autorização**

   - Implemente a autenticação de usuários utilizando `Flask-Login`.
   - Utilize tokens e criptografia para a segurança dos dados de autenticação.
   - Assegure que apenas usuários autenticados possam criar, editar e excluir postagens e comentários.
4. **Administração**

   - Utilize `Flask-Admin` para criar um painel administrativo.
   - No painel administrativo, deve ser possível gerenciar usuários, postagens, comentários e curtidas.
5. **Funcionalidades do Blog**

   - Cadastro de usuários.
   - Login e logout de usuários.
   - Criação, edição e exclusão de postagens.
   - Adição de comentários em postagens.
   - Adição e remoção de curtidas em postagens.
   - Visualização de postagens com seus comentários e curtidas.
6. **Histórico de Alterações**

   - Utilize `Flask-History` para rastrear e gerenciar as alterações feitas nas postagens e nos comentários.
7. **Persistência em Redis**

   - Configure o Redis como banco de dados para armazenar sessões de usuários e cache.
8. **Testes**

   - Utilize a biblioteca `Behave` para escrever cenários de teste que validem todas as funcionalidades da aplicação.
   - Garanta que todos os testes sejam executados e aprovados antes de entregar a aplicação.

### Passos Detalhados

1. **Configuração do Docker**

   - Crie um `Dockerfile` para configurar o ambiente da aplicação Flask.
   - Crie um `docker-compose.yml` para orquestrar os serviços necessários, incluindo o serviço do banco de dados PostgreSQL e Redis.
2. **Modelagem com SQLAlchemy**

   - Defina as classes de modelo para `User`, `Post`, `Comment` e `Like`.
   - Configure a conexão com o banco de dados PostgreSQL.
   - Utilize migrations para criar e atualizar o esquema do banco de dados (sugestão: utilizar `Flask-Migrate`).
3. **Autenticação e Criptografia**

   - Configure `Flask-Login` para gerenciar a sessão de usuários.
   - Utilize `Werkzeug` ou outra biblioteca para criptografar senhas.
   - Implemente endpoints de API para registro e login de usuários, retornando tokens de autenticação.
4. **Painel Administrativo**

   - Configure `Flask-Admin` para criar um painel administrativo.
   - Adicione views administrativas para gerenciar usuários, postagens, comentários e curtidas.
5. **Desenvolvimento das Funcionalidades do Blog**

   - Implemente as rotas e views necessárias para:
     - Cadastro e login de usuários.
     - Criação, edição e exclusão de postagens.
     - Comentários em postagens.
     - Curtidas em postagens.
   - Assegure que somente usuários autenticados possam realizar ações restritas.
   - Implemente a documentação da API do blog utilizando o plugin do flask para Swagger(flask-apispec)
6. **Histórico de Alterações**

   - Implemente o rastreamento de alterações em postagens e comentários utilizando `Flask-History`.
   - Assegure que todas as modificações sejam registradas e possam ser revertidas.
7. **Persistência em Redis**

   - Configure o Redis para armazenar sessões de usuários.
   - Utilize Redis para cache de dados frequentemente acessados para melhorar a performance.
8. **Testes**

   - Utilize a biblioteca `Behave` para escrever cenários de teste que validem todas as funcionalidades da aplicação.
   - Garanta que todos os testes sejam executados e aprovados antes de entregar a aplicação.

### Cenários de Teste propostos

#### Funcionalidade: Cadastro de Usuário

```gherkin
Feature: Cadastro de usuário
  Como um novo usuário
  Eu quero me registrar no blog
  Para que eu possa criar postagens e comentários

  Scenario: Usuário se registra com dados válidos
    Given que estou na página de cadastro
    When eu preencho "username" com "novo_usuario"
    And eu preencho "email" com "usuario@example.com"
    And eu preencho "password" com "senha_segura"
    And eu clico em "Registrar"
    Then eu devo ver a mensagem "Cadastro realizado com sucesso"

  Scenario: Usuário se registra com email já existente
    Given que estou na página de cadastro
    When eu preencho "username" com "novo_usuario"
    And eu preencho "email" com "existente@example.com"
    And eu preencho "password" com "senha_segura"
    And eu clico em "Registrar"
    Then eu devo ver a mensagem "Email já está em uso"
```

#### Funcionalidade: Login de Usuário

```gherkin
Feature: Login de usuário
  Como um usuário registrado
  Eu quero fazer login no blog
  Para que eu possa acessar minhas funcionalidades restritas

  Scenario: Usuário faz login com credenciais válidas
    Given que estou na página de login
    When eu preencho "email" com "usuario@example.com"
    And eu preencho "password" com "senha_segura"
    And eu clico em "Login"
    Then eu devo ver a mensagem "Login realizado com sucesso"

  Scenario: Usuário faz login com credenciais inválidas
    Given que estou na página de login
    When eu preencho "email" com "usuario@example.com"
    And eu preencho "password" com "senha_incorreta"
    And eu clico em "Login"
    Then eu devo ver a mensagem "Email ou senha incorretos"
```

#### Funcionalidade: Criação de Postagem

```gherkin
Feature: Criação de postagem
  Como um usuário autenticado
  Eu quero criar postagens no blog
  Para compartilhar meu conteúdo com outros usuários

  Scenario: Usuário cria uma postagem com dados válidos
    Given que estou logado
    And que estou na página de criação de postagens
    When eu preencho "title" com "Minha Primeira Postagem"
    And eu preencho "body" com "Este é o conteúdo da minha primeira postagem"
    And eu clico em "Publicar"
    Then eu devo ver a mensagem "Postagem criada com sucesso"
    And eu devo ver a postagem "Minha Primeira Postagem" na lista de postagens

  Scenario: Usuário tenta criar uma postagem sem título
    Given que estou logado
    And que estou na página de criação de postagens
    When eu preencho "body" com "Este é o conteúdo da minha postagem"
    And eu clico em "Publicar"
    Then eu devo ver a mensagem "Título é obrigatório"
```

#### Funcionalidade: Adição de Comentário

```gherkin
Feature: Adição de comentário
  Como um usuário autenticado
  Eu quero adicionar comentários nas postagens
  Para interagir com o conteúdo do blog

  Scenario: Usuário adiciona um comentário com sucesso
    Given que estou logado
    And que estou visualizando uma postagem
    When eu preen

cho "comment" com "Ótima postagem!"
    And eu clico em "Comentar"
    Then eu devo ver a mensagem "Comentário adicionado com sucesso"
    And eu devo ver o comentário "Ótima postagem!" na lista de comentários

  Scenario: Usuário tenta adicionar um comentário vazio
    Given que estou logado
    And que estou visualizando uma postagem
    When eu clico em "Comentar" sem preencher "comment"
    Then eu devo ver a mensagem "Comentário não pode ser vazio"
```

#### Funcionalidade: Curtidas em Postagem

```gherkin
Feature: Curtidas em postagem
  Como um usuário autenticado
  Eu quero curtir postagens
  Para expressar minha apreciação pelo conteúdo

  Scenario: Usuário curte uma postagem
    Given que estou logado
    And que estou visualizando uma postagem
    When eu clico em "Curtir"
    Then eu devo ver a mensagem "Você curtiu esta postagem"
    And o número de curtidas deve aumentar

  Scenario: Usuário remove a curtida de uma postagem
    Given que estou logado
    And que estou visualizando uma postagem que já curti
    When eu clico em "Descurtir"
    Then eu devo ver a mensagem "Você removeu a curtida desta postagem"
    And o número de curtidas deve diminuir
```

Estes são alguns cenários propostos, você poderá propor outros cenários possíveis.

### Perguntas Conceituais para Avaliação

#### Docker

1. O que é Docker e quais são suas principais vantagens no desenvolvimento de aplicações web?
2. Explique a diferença entre um `Dockerfile` e um arquivo `docker-compose.yml`.
3. O que são volumes e networks no contexto do Docker e como eles são utilizados?
4. Como você configuraria um serviço de banco de dados PostgreSQL utilizando Docker Compose?

#### SQLAlchemy e PostgreSQL

1. O que é SQLAlchemy e como ele facilita o mapeamento objeto-relacional (ORM)?
2. Explique o uso de `session` em SQLAlchemy. Qual é o papel dela no contexto de uma aplicação web?
3. O que são migrations no contexto do SQLAlchemy e por que elas são importantes?
4. Descreva a diferença entre uma relação one-to-many e many-to-many no contexto do SQLAlchemy. Dê exemplos de cada uma.

#### Flask-Admin

1. O que é Flask-Admin e quais são seus principais usos em uma aplicação Flask?
2. Como você configuraria uma view administrativa para gerenciar uma entidade `User` utilizando Flask-Admin?
3. Quais são os benefícios de utilizar Flask-Admin em uma aplicação web?

#### Flask-Login e Autenticação

1. O que é Flask-Login e como ele auxilia na gestão de autenticação de usuários em uma aplicação Flask?
2. Explique como implementar uma funcionalidade de login seguro utilizando Flask-Login e criptografia de senhas.
3. O que são tokens de autenticação e como eles podem ser utilizados para manter sessões seguras?
4. Explique o conceito de "decorators" em Flask e como eles são usados para proteger rotas.

#### Flask-History

1. O que é Flask-History e quais são seus principais usos em uma aplicação Flask?
2. Como você configuraria o Flask-History para rastrear alterações em uma entidade `Post`?
3. Quais são os benefícios de manter um histórico de alterações em uma aplicação web?

#### Redis

1. O que é Redis e quais são suas principais vantagens em comparação com outros bancos de dados?
2. Explique como configurar o Redis para armazenamento de sessões em uma aplicação Flask.
3. Como o uso de Redis pode melhorar a performance de uma aplicação web?
4. O que são operações atômicas em Redis e como elas garantem a integridade dos dados?

#### Desenvolvimento Web com Flask

1. Explique a arquitetura MVC (Model-View-Controller) e como ela é aplicada em uma aplicação Flask.
2. Quais são as diferenças entre métodos HTTP (GET, POST, PUT, DELETE) e como eles são utilizados em rotas Flask?
3. Como você configuraria uma aplicação Flask para diferentes ambientes (desenvolvimento, teste, produção)?

#### Testes com Behave

1. O que é a biblioteca Behave e qual é sua utilidade em testes de software?
2. Explique a estrutura básica de um arquivo de feature no Behave.
3. Quais são os componentes principais de um cenário de teste em Behave (Given, When, Then)?
4. Como você integraria testes Behave com a sua aplicação Flask para garantir que as funcionalidades estão corretas?

### Avaliação

Os seguintes critérios serão utilizados para avaliar a sua implementação:

* **Correção Funcional:** A aplicação deve atender a todos os requisitos funcionais listados acima.
* **Boas Práticas de Programação:** Código limpo, organizado e bem documentado.
* **Segurança:** Uso adequado de tokens e criptografia para proteger dados de autenticação.
* **Configuração do Ambiente:** Uso correto de Docker para facilitar a configuração e execução do ambiente.
* **Modelagem de Dados:** Modelagem correta das entidades e seus relacionamentos no banco de dados PostgreSQL.
* **Administração:** Painel administrativo funcional e fácil de usar.
* **Testes:** Presença e qualidade dos testes de comportamento escritos com Behave.

### Entrega

Por favor, entregue o código fonte da sua aplicação em um repositório Git (por exemplo, GitHub, GitLab), com instruções claras de como configurar e executar a aplicação utilizando Docker, bem como como executar os testes.
