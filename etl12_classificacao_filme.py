# extração das informações de melhores filmes

''' pip3.9 install tmdbv3api  sempre especificar a versão'''
import pandas as pd
import sqlalchemy as mssdb
from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import TV

# Carga no banco MSSQL
# engine = mssdb.create_engine("mssql+pyodbc://sa:Numsey@Password!@localhost,1401/DBDESENV?driver=ODBC+DRIVER+17+for+SQL+Server")
engine = mssdb.create_engine("mssql+pyodbc://sa:Numsey@Password!@0.0.0.0,1433/DBPRD?driver=ODBC+DRIVER+17+for+SQL+Server")

# chaves
tmdb = TMDb()
tmdb.api_key = '05f154090c26eb1a26cc6ad23399e396'
tmdb.language = 'en'
tmdb.debug = True

movie = Movie()
tv    = TV()

# Filmes mais popularies
popular = movie.popular()
tabela01 = []
for p in popular:
    tbl = [
        p.id,
        p.title,
        p.overview,
        p.popularity,
        p.vote_count,
        p.release_date
    ]
    tabela01.append(tbl)
MoviePopular = pd.DataFrame(tabela01,columns=['ID', 'Titulo', 'Resumo', 'Popularidade', 'QtdVotos', 'DataLancamento'])

# Filmes recomendados
recomendacao = movie.recommendations(movie_id=111)
tabela02 = []
for a in recomendacao:
    tbl = [
        a.id,
        a.original_language,
        a.original_title,
        a.overview,
        a.title,
        a.release_date,
        a.popularity,
        a.vote_average,
        a.vote_count
    ]
    tabela02.append(tbl)
MovieRecomendacao = pd.DataFrame(tabela02,columns=['ID', 'IdiomaOriginal', 'TituloOriginal', 'Resumo', 'Titulo' ,'DataLancamento', 'Popularidade', 'MediaVotos', 'QtdVotos'])

# review de Movies
review = movie.reviews(movie_id=11)
tabela03 = []
for r in review:
    tbl = [
        r.author,
        r.author_details.name,
        r.author_details.username,
        r.author_details.avatar_path,
        r.author_details.rating,
        r.content,
        r.created_at,
        r.updated_at

    ]
    tabela03.append(tbl)
MovieReview = pd.DataFrame(tabela03, columns=['Autor', 'DetalheAutor', 'Ussername', 'Avatar', 'Rating', 'content', 'created_at', 'updated_at'])


# series de TV Popular
TvPopular = tv.popular()
tabela04 = []
for tv in TvPopular:
    tbl = [
        tv.id,
        tv.name,
        tv.original_language,
        tv.vote_count,
        tv.first_air_date,
        tv.popularity,
        tv.overview
    ]
    tabela04.append(tbl)
TVPopular = pd.DataFrame(tabela04, columns=['id', 'Name', 'IdiomaOriginal', 'QtdVotos', 'DtEstreia', 'Popularidade', 'Resumo'])

MoviePopular.to_sql('stg_MoviePopular',con=engine, if_exists='replace', schema='dbo', index=False, chunksize = None)
MovieRecomendacao.to_sql('stg_MovieRecomendacao',con=engine, if_exists='replace', schema='dbo', index=False, chunksize = None)
MovieReview.to_sql('stg_MovieReview',con=engine, if_exists='replace', schema='dbo', index=False, chunksize = None)
TVPopular.to_sql('stg_Popular',con=engine, if_exists='replace', schema='dbo', index=False, chunksize = None)


