# Teste de conhecimentos adquiridos no Treinamento Python

### Para rodar o sistema
Passos simples, levando em conta que o Docker já esteja instalado.
```
cd docker
docker-compose up --force-recreate 
```

# Perguntas Conceituais para Avaliação

## Docker

1. **O que é Docker e quais são suas principais vantagens no desenvolvimento de aplicações web?**
   - Docker é uma plataforma para criar, distribuir e executar aplicações em contêineres. As principais vantagens incluem consistência no ambiente de desenvolvimento, fácil escalabilidade, isolamento de dependências e portabilidade entre diferentes ambientes.

2. **Explique a diferença entre um Dockerfile e um arquivo docker-compose.yml.**
   - O Dockerfile é um script que define como criar uma imagem Docker, especificando os comandos para instalar e configurar dependências. O docker-compose.yml é um arquivo de configuração para definir e executar múltiplos contêineres Docker, especificando como eles interagem entre si e com o ambiente.

3. **O que são volumes e networks no contexto do Docker e como eles são utilizados?**
   - Volumes são usados para persistir dados gerados e utilizados pelos contêineres. Networks permitem que os contêineres se comuniquem entre si e com o host, definindo regras de acesso e isolamento.

4. **Como você configuraria um serviço de banco de dados PostgreSQL utilizando Docker Compose?**
   - Adicione um serviço para o PostgreSQL no arquivo `docker-compose.yml`, definindo a imagem do PostgreSQL, variáveis de ambiente para o banco de dados e as portas de exposição. Exemplo:
     ```yaml
     version: '3'
     services:
       db:
         image: postgres:latest
         environment:
           POSTGRES_DB: mydatabase
           POSTGRES_USER: user
           POSTGRES_PASSWORD: password
         ports:
           - "5432:5432"
     ```

## SQLAlchemy e PostgreSQL

1. **O que é SQLAlchemy e como ele facilita o mapeamento objeto-relacional (ORM)?**
   - SQLAlchemy é uma biblioteca Python que facilita o mapeamento entre classes Python e tabelas de banco de dados relacionais, permitindo que você manipule dados usando objetos Python em vez de SQL diretamente.

2. **Explique o uso de session em SQLAlchemy. Qual é o papel dela no contexto de uma aplicação web?**
   - A session em SQLAlchemy gerencia transações e interage com o banco de dados. Ela é usada para adicionar, consultar e modificar objetos, e para garantir que as alterações sejam confirmadas ou revertidas em uma transação.

3. **O que são migrations no contexto do SQLAlchemy e por que elas são importantes?**
   - Migrations são scripts que aplicam alterações na estrutura do banco de dados ao longo do tempo, como adicionar ou remover colunas. Elas são importantes para manter o banco de dados sincronizado com o modelo de dados da aplicação.

4. **Descreva a diferença entre uma relação one-to-many e many-to-many no contexto do SQLAlchemy. Dê exemplos de cada uma.**
   - One-to-many: Uma entidade pode estar relacionada a várias outras entidades. Exemplo: Um autor pode ter vários livros.
   - Many-to-many: Muitas entidades estão relacionadas a muitas outras entidades. Exemplo: Alunos e cursos, onde um aluno pode se inscrever em vários cursos e um curso pode ter vários alunos.

## Flask-Admin

1. **O que é Flask-Admin e quais são seus principais usos em uma aplicação Flask?**
   - Flask-Admin é uma extensão para Flask que fornece uma interface administrativa para gerenciar modelos e dados. É usado para criar rapidamente uma interface de administração para CRUD (Create, Read, Update, Delete) de dados.

2. **Como você configuraria uma view administrativa para gerenciar uma entidade User utilizando Flask-Admin?**
   - criaria uma classe `UserAdmin` que herda de `ModelView` e registrariaa com o `Admin` para a entidade `User`. Exemplo:
     ```python
     from flask_admin import Admin
     from flask_admin.contrib.sqla import ModelView
     from myapp.models import User
     from myapp import db

     admin = Admin(app, name='Admin')
     admin.add_view(ModelView(User, db.session))
     ```

3. **Quais são os benefícios de utilizar Flask-Admin em uma aplicação web?**
   - Oferece uma interface de administração pronta para uso, economizando tempo no desenvolvimento de funcionalidades administrativas e facilitando o gerenciamento de dados.

## Flask-Login e Autenticação

1. **O que é Flask-Login e como ele auxilia na gestão de autenticação de usuários em uma aplicação Flask?**
   - Flask-Login é uma extensão que gerencia sessões de usuário e fornece uma maneira de autenticar e gerenciar a identidade do usuário, facilitando a criação de sistemas de login e controle de acesso.

2. **Explique como implementar uma funcionalidade de login seguro utilizando Flask-Login e criptografia de senhas.**
   - Configure o Flask-Login com um gerenciador de sessão e use o `werkzeug.security` para criptografar senhas. Armazene senhas criptografadas no banco de dados e compare as senhas fornecidas com as criptografadas durante o login.

3. **O que são tokens de autenticação e como eles podem ser utilizados para manter sessões seguras?**
   - Tokens de autenticação são strings únicas geradas para identificar e autenticar usuários. Eles podem ser usados em cabeçalhos de requisições para verificar se o usuário está autenticado e autorizado a acessar recursos.

4. **Explique o conceito de "decorators" em Flask e como eles são usados para proteger rotas.**
   - Decorators são funções que modificam o comportamento de outras funções. Em Flask, decorators como `@login_required` são usados para restringir o acesso a certas rotas para usuários autenticados.

## Flask-History

1. **O que é Flask-History e quais são seus principais usos em uma aplicação Flask?**
   - Flask-History é uma extensão para rastrear e armazenar alterações feitas a modelos de dados. É usado para criar um histórico de mudanças, facilitando a auditoria e a recuperação de dados.

2. **Como você configuraria o Flask-History para rastrear alterações em uma entidade Post?**
   - configuraria o Flask-History para monitorar a entidade `Post` e registrar alterações. Exemplo:
     ```python
     from flask_history import History
     history = History(app)
     history.track(Post)
     ```

3. **Quais são os benefícios de manter um histórico de alterações em uma aplicação web?**
   - Permite auditar alterações, recuperar dados antigos, e monitorar mudanças para fins de conformidade e segurança.

## Redis

1. **O que é Redis e quais são suas principais vantagens em comparação com outros bancos de dados?**
   - Redis é um banco de dados em memória que oferece alta performance e suporte para estruturas de dados avançadas. Suas vantagens incluem velocidade, persistência opcional e suporte para operações complexas.

2. **Explique como configurar o Redis para armazenamento de sessões em uma aplicação Flask.**
   - Use a extensão `Flask-Session` para configurar o Redis como backend de sessão. Exemplo:
     ```python
     from flask_session import Session
     app.config['SESSION_TYPE'] = 'redis'
     app.config['SESSION_PERMANENT'] = False
     app.config['SESSION_USE_SIGNER'] = True
     app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379)
     Session(app)
     ```

3. **Como o uso de Redis pode melhorar a performance de uma aplicação web?**
   - Redis melhora a performance ao armazenar dados em memória, reduzindo a latência e aumentando a velocidade de acesso a informações frequentemente usadas.

4. **O que são operações atômicas em Redis e como elas garantem a integridade dos dados?**
   - Operações atômicas em Redis garantem que uma operação seja realizada completamente ou não seja realizada, evitando condições de corrida e mantendo a integridade dos dados.

## Desenvolvimento Web com Flask

1. **Explique a arquitetura MVC (Model-View-Controller) e como ela é aplicada em uma aplicação Flask.**
   - MVC é um padrão de arquitetura que separa a aplicação em três componentes: Model (dados), View (interface) e Controller (lógica). Em Flask, o Model é geralmente representado pelos modelos de dados, a View pelas rotas e templates, e o Controller pela lógica que manipula a interação entre Model e View.

2. **Quais são as diferenças entre métodos HTTP (GET, POST, PUT, DELETE) e como eles são utilizados em rotas Flask?**
   - GET: Recupera dados. POST: Envia dados para criar algo novo. PUT: Atualiza dados existentes. DELETE: Remove dados. Em Flask, eles são usados nas rotas para definir a ação que cada rota deve executar.

3. **Como você configuraria uma aplicação Flask para diferentes ambientes (desenvolvimento, teste, produção)?**
   - Usaria variáveis de ambiente ou arquivos de configuração separados para cada ambiente. Em Flask, configuraria o `app.config` para carregar as configurações apropriadas dependendo do ambiente.

## Testes com Behave

1. **O que é a biblioteca Behave e qual é sua utilidade em testes de software?**
   - Behave é uma biblioteca para testes de software baseada em BDD (Behavior Driven Development). Ela permite escrever testes em uma linguagem natural, facilitando a comunicação entre desenvolvedores e não desenvolvedores.

2. **Explique a estrutura básica de um arquivo de feature no Behave.**
   - Um arquivo de feature contém uma ou mais características descritas com cenários que detalham como o sistema deve se comportar. Cada cenário é descrito com passos Given, When e Then.

3. **Quais são os componentes principais de um cenário de teste em Behave (Given, When, Then)?**
   - Given: Define o estado inicial ou pré-condições. When: Define a ação ou evento que ocorre. Then: Define o resultado esperado após a ação.

4. **Como você integraria testes Behave com a sua aplicação Flask para garantir que as funcionalidades estão corretas?**
   - Escreveria testes em arquivos de feature para definir comportamentos esperados e implementaria os passos correspondentes em arquivos de código.

