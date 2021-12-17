
-- script alter name
use master;
ALTER DATABASE dbproducao SET SINGLE_USER WITH ROLLBACK IMMEDIATE
GO
ALTER DATABASE dbproducao MODIFY NAME = dwproducao ;
GO 
ALTER DATABASE dwproducao SET MULTI_USER
GO

use master;
ALTER DATABASE AdventureWorks2019 MODIFY NAME = dbproducao ;
ALTER DATABASE AdventureWorksDW2019 MODIFY NAME = dwproducao ;
GO



