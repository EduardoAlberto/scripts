-- procedure 
create or alter proc sp_carga_vendas
as 
 if not exists(select * from sys.objects where name = 'tb_bi_vendas')
    begin 
        create table tb_bi_vendas(
             id_num         int IDENTITY(1,1)
            ,id	            bigint
            ,dt_date        date
            ,price	        int
            ,bedrooms	    int
            ,bathrooms	    int
            ,sqft_living    int
            ,sqft_lot	    int
            ,floors	        int
            ,waterfront	    int
            ,views	        int
            ,condition	    int
            ,grade	        int
            ,sqft_above	    int
            ,sqft_basement	int
            ,yr_built	    int
            ,yr_renovated	int
            ,zipcode	    int
            ,lat	        numeric(15,8)
            ,long	        numeric(15,6)
            ,sqft_living15	int
            ,sqft_lot15	    int
            ,dtatualizacao  datetime
        )
    end
    insert into tb_bi_vendas
    (
         id	            
        ,dt_date        
        ,price	        
        ,bedrooms	    
        ,bathrooms	    
        ,sqft_living    
        ,sqft_lot	    
        ,floors	        
        ,waterfront	    
        ,views	        
        ,condition	    
        ,grade	        
        ,sqft_above	    
        ,sqft_basement	
        ,yr_built	    
        ,yr_renovated	
        ,zipcode	    
        ,lat	        
        ,long	        
        ,sqft_living15	
        ,sqft_lot15	    
        ,dtatualizacao  

    )
    select 
         convert(bigint,left(replace(b.id,'.',''),10))
        ,convert(date,left(b.dt_date,8))        
        ,convert(float,b.price)	        
        ,convert(float,replace(replace(b.bedrooms,'.',''),'nn',''))
        ,convert(float,b.bathrooms)
        ,convert(int,replace(b.sqft_living,'.',''))    
        ,convert(int,replace(b.sqft_lot,'.',''))	    
        ,convert(float,replace(replace(b.floors,'.',''),'nn',''))	        
        ,convert(float,b.waterfront)	    
        ,convert(float,b.views)	        
        ,convert(float,b.condition)	    
        ,convert(float,b.grade)	        
        ,convert(float,b.sqft_above)	    
        ,convert(float,b.sqft_basement)	
        ,convert(float,b.yr_built)	    
        ,convert(float,b.yr_renovated)	
        ,convert(float,b.zipcode)	    
        ,convert(numeric(15,8),b.lat)	        
        ,convert(numeric(15,6),b.long)	        
        ,convert(float,b.sqft_living15)	
        ,convert(float,b.sqft_lot15)	
        ,convert(date,getdate()) as  dtatualizacao          
    from stg_bi_vendas b
    where not exists(select id_num, dtatualizacao from tb_bi_vendas a where a.id_num = convert(bigint,left(replace(b.id,'.',''),10))  and a.dtatualizacao = dtatualizacao )
    
    TRUNCATE TABLE stg_bi_vendas

    select count(*) from tb_bi_vendas
    select count(*) from stg_bi_vendas

    select * from tb_bi_vendas
    select * from stg_bi_vendas


MERGE stg_bi_vendas T
USING tb_bi_vendas S ON T.id_num=S.convert(bigint,left(replace(b.id,'.',''),10))
and s.dtatualizacao = T.dtatualizacao
WHEN NOT MATCHED BY TARGET 
THEN 
INSERT (LocationID,LocationName)
VALUES (S.LocationID,S.LocationName); 

truncate table tb_bi_vendaså
truncate table stg_bi_vendas


exec sp_carga_vendas 


-- teste de merge no sql server

  

