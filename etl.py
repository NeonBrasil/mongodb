import psycopg2
from pymongo import MongoClient
import logging
from typing import List, Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_data():
    conn_pg = None
    mongo_client = None
    
    try:
        # Conexões
        conn_pg = psycopg2.connect(
            dbname="Faculdade",
            user="neon", 
            password="1234",
            host="localhost"
        )
        cur = conn_pg.cursor()
        
        mongo_client = MongoClient("mongodb://localhost:27017/")
        db_nosql = mongo_client["DocumentStore"]
        
        # Limpar coleções existentes (opcional)
        collections = ['alunos', 'professores', 'departamentos', 'cursos', 
                      'disciplinas', 'cursando', 'leciona', 'matriz_curricular', 'orientador']
        for col in collections:
            db_nosql[col].delete_many({})
        
        # MIGRAR ALUNOS
        logger.info("Migrando alunos...")
        cur.execute("SELECT RA, CPF, Nome, Email, curso_id FROM Aluno")
        alunos = []
        for ra, cpf, nome, email, curso_id in cur.fetchall():
            alunos.append({
                "_id": ra,
                "cpf": cpf,
                "nome": nome,
                "email": email,
                "curso_id": curso_id
            })
        if alunos:
            db_nosql.alunos.insert_many(alunos, ordered=False)
        
        # MIGRAR PROFESSORES
        logger.info("Migrando professores...")
        cur.execute("SELECT RA, CPF, Nome, Email, Salario, nome_dept FROM Professor")
        professores = []
        for ra, cpf, nome, email, salario, nome_dept in cur.fetchall():
            professores.append({
                "_id": ra,
                "cpf": cpf,
                "nome": nome,
                "email": email,
                "salario": float(salario) if salario is not None else None,
                "nome_dept": nome_dept
            })
        if professores:
            db_nosql.professores.insert_many(professores, ordered=False)
        
        # MIGRAR DEPARTAMENTOS
        logger.info("Migrando departamentos...")
        cur.execute("SELECT nome_dept, Orcamento, Predio, chefe_ra FROM Departamento")
        departamentos = []
        for nome_dept, orcamento, predio, chefe_ra in cur.fetchall():
            departamentos.append({
                "_id": nome_dept,
                "orcamento": float(orcamento) if orcamento is not None else None,
                "predio": predio,
                "chefe_ra": chefe_ra
            })
        if departamentos:
            db_nosql.departamentos.insert_many(departamentos, ordered=False)
        
        # MIGRAR CURSOS
        logger.info("Migrando cursos...")
        cur.execute("SELECT curso_id, nome_curso, nome_dept FROM Curso")
        cursos = []
        for curso_id, nome_curso, nome_dept in cur.fetchall():
            cursos.append({
                "_id": curso_id,
                "nome_curso": nome_curso,
                "nome_dept": nome_dept
            })
        if cursos:
            db_nosql.cursos.insert_many(cursos, ordered=False)
        
        # MIGRAR DISCIPLINAS
        logger.info("Migrando disciplinas...")
        cur.execute("SELECT materia_id, nome_materia, nome_dept, curso_id FROM Materia")
        disciplinas = []
        for materia_id, nome_materia, nome_dept, curso_id in cur.fetchall():
            disciplinas.append({
                "_id": materia_id,
                "nome_materia": nome_materia,
                "nome_dept": nome_dept,
                "curso_id": curso_id
            })
        if disciplinas:
            db_nosql.disciplinas.insert_many(disciplinas, ordered=False)
        
        # MIGRAR CURSANDO
        logger.info("Migrando cursando...")
        cur.execute("SELECT RA, materia_id, Semestre, Ano, Nota, status FROM Cursando")
        cursando = []
        for ra, materia_id, semestre, ano, nota, status in cur.fetchall():
            cursando.append({
                "_id": f"{ra}_{materia_id}_{semestre}_{ano}",
                "RA": ra,
                "disciplina_id": materia_id,
                "Semestre": semestre,
                "Ano": ano,
                "Nota": float(nota) if nota is not None else None,
                "status": status
            })
        if cursando:
            db_nosql.cursando.insert_many(cursando, ordered=False)
        
        # MIGRAR LECIONA
        logger.info("Migrando leciona...")
        cur.execute("SELECT RA_Prof, materia_id, Semestre, Ano, status FROM Leciona")
        leciona = []
        for ra_prof, materia_id, semestre, ano, status in cur.fetchall():
            leciona.append({
                "RA_Prof": ra_prof,
                "materia_id": materia_id,
                "Semestre": semestre,
                "Ano": ano,
                "status": status
            })
        if leciona:
            db_nosql.leciona.insert_many(leciona, ordered=False)
        
        # MIGRAR MATRIZ CURRICULAR
        logger.info("Migrando matriz curricular...")
        cur.execute("SELECT curso_id, materia_id FROM MatrizCurricular")
        matriz = {}
        for curso_id, materia_id in cur.fetchall():
            if curso_id not in matriz:
                matriz[curso_id] = []
            matriz[curso_id].append(materia_id)
        
        matriz_docs = []
        for curso_id, materias in matriz.items():
            matriz_docs.append({
                "curso_id": curso_id,
                "materias": materias
            })
        if matriz_docs:
            db_nosql.matriz_curricular.insert_many(matriz_docs, ordered=False)
        
        # MIGRAR ORIENTADOR
        logger.info("Migrando orientador...")
        cur.execute("SELECT grupo_id, prof_ra, aluno_ra FROM Orientador")
        grupos = {}
        for grupo_id, prof_ra, aluno_ra in cur.fetchall():
            if grupo_id not in grupos:
                grupos[grupo_id] = {'integrantes': [], 'orientador_ra': prof_ra}
            grupos[grupo_id]['integrantes'].append(aluno_ra)
        
        orientador_docs = []
        for grupo_id, dados in grupos.items():
            orientador_docs.append({
                "grupo_id": grupo_id,
                "integrantes": dados["integrantes"],
                "orientador_ra": dados["orientador_ra"]
            })
        if orientador_docs:
            db_nosql.orientador.insert_many(orientador_docs, ordered=False)
        
        logger.info("Migração concluída com sucesso!")
        
    except psycopg2.Error as e:
        logger.error(f"Erro PostgreSQL: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro na migração: {e}")
        raise
    finally:
        if conn_pg:
            conn_pg.close()
        if mongo_client:
            mongo_client.close()

if __name__ == "__main__":
    migrate_data()
