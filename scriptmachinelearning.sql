USE TutorialDB;
SELECT * FROM [dbo].[rental_data];

-- Stored procedure that trains and generates a Python model using the rental_data and a linear regression algorithm
DROP PROCEDURE IF EXISTS generate_rental_py_model;
go
CREATE PROCEDURE generate_rental_py_model (@trained_model varbinary(max) OUTPUT)
AS
BEGIN
    EXECUTE sp_execute_external_script
      @language = N'Python'
    , @script = N'
from sklearn.linear_model import LinearRegression
import pickle

df = rental_train_data

# Get all the columns from the dataframe.
columns = df.columns.tolist()

# Store the variable well be predicting on.
target = "RentalCount"

# Initialize the model class.
lin_model = LinearRegression()

# Fit the model to the training data.
lin_model.fit(df[columns], df[target])

# Before saving the model to the DB table, convert it to a binary object
trained_model = pickle.dumps(lin_model)'

, @input_data_1 = N'select "RentalCount", "Year", "Month", "Day", "WeekDay", "Snow", "Holiday" from dbo.rental_data where Year < 2015'
, @input_data_1_name = N'rental_train_data'
, @params = N'@trained_model varbinary(max) OUTPUT'
, @trained_model = @trained_model OUTPUT;
END;
GO

USE TutorialDB;
DROP TABLE IF EXISTS dbo.rental_py_models;
GO
CREATE TABLE dbo.rental_py_models (
    model_name VARCHAR(30) NOT NULL DEFAULT('default model') PRIMARY KEY,
    model VARBINARY(MAX) NOT NULL
);
GO

DECLARE @model VARBINARY(MAX);
EXECUTE generate_rental_py_model @model OUTPUT;

INSERT INTO rental_py_models (model_name, model) VALUES('linear_model', @model);