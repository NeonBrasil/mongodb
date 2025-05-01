import psycopg2
from pymongo import MongoClient

# 1. Conexão com o PostgreSQL
conn_pg = psycopg2.connect(
    dbname="Faculdade",
    user="neon",
    password="1234",
    host="localhost"
)
cur = conn_pg.cursor()

# 2. Conexão com o MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db_nosql = mongo_client["DocumentStore"]

# ====== MIGRANDO ALUNOS ======
cur.execute("SELECT RA, CPF, Nome, Email, curso_id FROM Aluno")
for ra, cpf, nome, email, curso_id in cur.fetchall():
    db_nosql.alunos.insert_one({
        "_id": ra,
        "cpf": cpf,
        "nome": nome,
        "email": email,
        "curso_id": curso_id
    })

# ====== MIGRANDO PROFESSORES ======
cur.execute("SELECT RA, CPF, Nome, Email, Salario, nome_dept FROM Professor")
for ra, cpf, nome, email, salario, nome_dept in cur.fetchall():
    db_nosql.professores.insert_one({
        "_id": ra,
        "cpf": cpf,
        "nome": nome,
        "email": email,
        "salario": float(salario),
        "nome_dept": nome_dept
    })

# ====== MIGRANDO DEPARTAMENTOS ======
cur.execute("SELECT nome_dept, Orcamento, Predio, chefe_ra FROM Departamento")
for nome_dept, orcamento, predio, chefe_ra in cur.fetchall():
    db_nosql.departamentos.insert_one({
        "_id": nome_dept,
        "orcamento": float(orcamento),
        "predio": predio,
        "chefe_ra": chefe_ra
    })

# ====== MIGRANDO CURSOS ======
cur.execute("SELECT curso_id, nome_curso, nome_dept FROM Curso")
for curso_id, nome_curso, nome_dept in cur.fetchall():
    db_nosql.cursos.insert_one({
        "_id": curso_id,
        "nome_curso": nome_curso,
        "nome_dept": nome_dept
    })

# ====== MIGRANDO DISCIPLINAS (Materia) ======
cur.execute("SELECT materia_id, nome_materia, nome_dept, curso_id FROM Materia")
for materia_id, nome_materia, nome_dept, curso_id in cur.fetchall():
    db_nosql.disciplinas.insert_one({
        "_id": materia_id,
        "nome_materia": nome_materia,
        "nome_dept": nome_dept,
        "curso_id": curso_id
    })

# ====== MIGRANDO CURSANDO ======
cur.execute("SELECT RA, materia_id, Semestre, Ano, Nota, status FROM Cursando")
for ra, materia_id, semestre, ano, nota, status in cur.fetchall():
    db_nosql.cursando.insert_one({
        "_id": f"{ra}_{materia_id}_{semestre}_{ano}",
        "RA": ra,
        "disciplina_id": materia_id,
        "Semestre": semestre,
        "Ano": ano,
        "Nota": float(nota) if nota is not None else None,
        "status": status
    })

# ====== MIGRANDO LECIONA ======
cur.execute("SELECT RA_Prof, materia_id, Semestre, Ano, status FROM Leciona")
for ra_prof, materia_id, semestre, ano, status in cur.fetchall():
    db_nosql.leciona.insert_one({
        "RA_Prof": ra_prof,
        "materia_id": materia_id,
        "Semestre": semestre,
        "Ano": ano,
        "status": status
    })

# ====== MIGRANDO MATRIZ CURRICULAR ======
# Vamos usar o formato documentado, um por curso, com array de matérias:
cur.execute("SELECT curso_id, materia_id FROM MatrizCurricular")
matriz = {}
for curso_id, materia_id in cur.fetchall():
    if curso_id not in matriz:
        matriz[curso_id] = []
    matriz[curso_id].append(materia_id)
for curso_id, materias in matriz.items():
    db_nosql.matriz_curricular.insert_one({
        "curso_id": curso_id,
        "materias": materias
    })

# ====== MIGRANDO ORIENTADOR ======
# Recomenda-se agrupar por grupo_id, para formato NoSQL amigável:
cur.execute("SELECT grupo_id, prof_ra, aluno_ra FROM Orientador")
grupos = {}
for grupo_id, prof_ra, aluno_ra in cur.fetchall():
    if grupo_id not in grupos:
        grupos[grupo_id] = {'integrantes': [], 'orientador_ra': prof_ra}
    grupos[grupo_id]['integrantes'].append(aluno_ra)
for grupo_id, dados in grupos.items():
    db_nosql.orientador.insert_one({
        "grupo_id": grupo_id,
        "integrantes": dados["integrantes"],
        "orientador_ra": dados["orientador_ra"]
    })

# ------- FIM DA MIGRAÇÃO -------
cur.close()
conn_pg.close()
mongo_client.close()

print("Todos os dados foram migrados com sucesso!")
