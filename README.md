# Projeto Banco de Dados NoSQL - Document Store (MongoDB)

## 👨‍🏫 Integrantes do Grupo

- **Cayque** – matrícula `22221005-6`

---

## 📝 Descrição do Projeto

Este projeto implementa um banco de dados NoSQL no **MongoDB** para uma instituição de ensino superior, baseado em um modelo relacional previamente desenvolvido em **PostgreSQL**.

As coleções representam entidades acadêmicas como:

- Alunos  
- Professores  
- Departamentos  
- Cursos  
- Disciplinas  
- Matrizes curriculares  
- Histórico escolar  
- Atividades de docência  
- Grupos de TCC

O objetivo é demonstrar a equivalência prática e a flexibilidade do modelo **NoSQL**, bem como atender a requisitos de relatórios e consultas acadêmicas avançadas no contexto de uma **Document Store**.

---

## ⚙️ Como Executar o Código

### 1. Instale as dependências (Python)

Certifique-se de ter o **Python 3** instalado em sua máquina.

Instale as bibliotecas necessárias com o comando:

```bash
pip install psycopg2 pymongo
```
### 2. Configure o banco SQL de origem
Importe/popule o banco PostgreSQL com o esquema e dados correspondentes ao modelo relacional.

### 3. Execute o script de ETL
No arquivo etl.py (fornecido junto ao projeto):

Configure as credenciais de acesso ao PostgreSQL e ao MongoDB.

Execute o script para migrar os dados do PostgreSQL para o MongoDB:

```
python etl.py
```
O script irá criar e popular as coleções em um banco de dados chamado DocumentStore.
(Também é possível criar esse banco vazio, visto que as queries para criação das collections está disponível [AQUI](https://github.com/NeonBrasil/mongodb/blob/main/queries%20criar%20banco))
### 4. Conferência dos dados no MongoDB
Abra o MongoDB Compass ou utilize o shell do MongoDB e confirme as coleções criadas e os documentos inseridos.
#### Exemplo de consulta simples para listar todos os alunos:

```javascript
db.alunos.find()
```

---

## 📊 Como Validar as Queries dos Relatórios

Após a migração dos dados, existem **cinco relatórios principais** que devem ser validados.

As queries estão disponíveis neste repositório:  
🔗 [https://github.com/NeonBrasil/mongodb/blob/main/queries%20an%C3%A1lise](https://github.com/NeonBrasil/mongodb/blob/main/queries%20an%C3%A1lise)

Você pode executar essas queries via:

- **MongoDB Compass**
- **Terminal (mongo shell)**

---

### 💻 Usando o MongoDB Compass

1. Selecione o banco `DocumentStore` no menu lateral.
2. Escolha a coleção relevante à query (`cursando`, `leciona`, `alunos`, etc).

#### Para consultas agregadas (`aggregate`):

- Vá até a aba **"Aggregations"** da coleção desejada.
- Cole o **pipeline completo** (array de stages) na área de edição.
- Clique em **"Run"** para visualizar os resultados.

#### Para buscas simples (`find`):

- Vá até a aba **"Documents"**.
- Insira o filtro no campo de busca e clique em **"Find"**.

---

### ✏️ Personalize os parâmetros

Substitua os valores de exemplo:

- `<RA_do_aluno>`
- `<RA_professor>`
- `<semestre>`
- `<ano>`

Por valores reais presentes no seu banco de dados.

---

### 📥 Resultados

O **MongoDB Compass** exibirá os documentos retornados diretamente na interface.  
Você pode:

- Exportar
- Copiar
- Analisar os dados retornados conforme a necessidade do trabalho

---

