create or alter proc carga_merger as 

-- store procedure de carga das dimensões
-- Tb_MoviePopular
merge Tb_MoviePopular T
using tmp_MoviePopular S  on t.id = s.ID
when matched THEN
update set   ID = s.ID
            ,Titulo = s.Titulo
            ,Resumo = s.Resumo
            ,Popularidade = s.Popularidade
            ,QtdVotos = s.QtdVotos
            ,DataLancamento = s.DataLancamento
when not matched by TARGET
then insert (ID,Titulo,Resumo,Popularidade,QtdVotos,DataLancamento)
values(s.ID,s.Titulo,s.Resumo,s.Popularidade,s.QtdVotos,s.DataLancamento)
when not matched by source
then 
Delete;


-- Tb_MovieRecomendacao
merge Tb_MovieRecomendacao T
using tmp_MovieRecomendacao S  on t.id = s.ID
when matched THEN
update set     ID = s.ID
              ,IdiomaOriginal = s.IdiomaOriginal
              ,TituloOriginal = s.TituloOriginal
              ,Resumo = s.Resumo
              ,Titulo = s.Titulo
              ,DataLancamento = s.DataLancamento
              ,Popularidade = s.Popularidade
              ,MediaVotos = s.MediaVotos
              ,QtdVotos = s.QtdVotos
when not matched by TARGET
then insert ( ID,IdiomaOriginal,TituloOriginal,Resumo,Titulo,DataLancamento,Popularidade,MediaVotos,QtdVotos)
values( s.ID,s.IdiomaOriginal,s.TituloOriginal,s.Resumo,s.Titulo,s.DataLancamento,s.Popularidade,s.MediaVotos,s.QtdVotos)
when not matched by source
then 
Delete;

-- Tb_MovieReview
merge Tb_MovieReview T
using tmp_MovieReview S  on t.updated_at = s.updated_at
when matched THEN
update set Autor = s.Autor
          ,DetalheAutor = s.DetalheAutor
          ,Ussername = s.Ussername
          ,Avatar = s.Avatar
          ,Rating = s.Rating
          ,content = s.content
          ,created_at = s.created_at
          ,updated_at = s.updated_at
when not matched by TARGET
then insert (Autor ,DetalheAutor ,Ussername ,Avatar ,Rating ,content ,created_at ,updated_at)
values(s.Autor ,s.DetalheAutor ,s.Ussername ,s.Avatar ,s.Rating ,s.content ,s.created_at ,s.updated_at)
when not matched by source
then 
Delete;

--- TB_Popular
merge Tb_Popular T
using tmp_Popular S  on t.id = s.ID
when matched THEN
update set   id = s.id
            ,Name = s.Name
            ,IdiomaOriginal = s.IdiomaOriginal
            ,QtdVotos = s.QtdVotos
            ,DtEstreia = s.DtEstreia
            ,Popularidade = s.Popularidade
            ,Resumo = s.Resumo
when not matched by TARGET
then insert (id ,Name ,IdiomaOriginal ,QtdVotos ,DtEstreia ,Popularidade ,Resumo)
values(s.id ,s.Name ,s.IdiomaOriginal ,s.QtdVotos ,s.DtEstreia ,s.Popularidade ,s.Resumo)
when not matched by source
then 
Delete;



select * from tmp_MoviePopular

insert into tmp_MoviePopular values(777355,'Hunter X Hunter', 'Anime estilo luta', 881.32 ,45,'2020-12-31')
update tmp_MoviePopular
set QtdVotos = 100
where id = 777355   

select * from Tb_MoviePopular where id = 777355

sp_help 'tmp_Popular'

--Analise dados DW 
select * from dwproducao.dbo.DimAccount

update dwproducao.dbo.DimAccount
    set ParentAccountKey = 1
where AccountKey = 1





