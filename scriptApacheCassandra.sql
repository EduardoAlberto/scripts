CREATE KEYSPACE dbcassandra WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};

CREATE TYPE dbcassandra.address (
  street text,
  city text,
  state_or_province text,
  postal_code text,
  country text );

CREATE TABLE dbcassandra.dbcassandras_by_poi (
  poi_name text,
  dbcassandra_id text,
  name text,
  phone text,
  address frozen<address>,
  PRIMARY KEY ((poi_name), dbcassandra_id) )
  WITH comment = 'Q1. Find dbcassandras near given poi'
  AND CLUSTERING ORDER BY (dbcassandra_id ASC) ;

CREATE TABLE dbcassandra.dbcassandras (
  id text PRIMARY KEY,
  name text,
  phone text,
  address frozen<address>,
  pois set )
  WITH comment = 'Q2. Find information about a dbcassandra';

CREATE TABLE dbcassandra.pois_by_dbcassandra (
  poi_name text,
  dbcassandra_id text,
  description text,
  PRIMARY KEY ((dbcassandra_id), poi_name) )
  WITH comment = 'Q3. Find pois near a dbcassandra';

CREATE TABLE dbcassandra.available_rooms_by_dbcassandra_date (
  dbcassandra_id text,
  date date,
  room_number smallint,
  is_available boolean,
  PRIMARY KEY ((dbcassandra_id), date, room_number) )
  WITH comment = 'Q4. Find available rooms by dbcassandra date';

CREATE TABLE dbcassandra.amenities_by_room (
  dbcassandra_id text,
  room_number smallint,
  amenity_name text,
  description text,
  PRIMARY KEY ((dbcassandra_id, room_number), amenity_name) )
  WITH comment = 'Q5. Find amenities for a room';

CREATE TABLE dbcassandra.rental_data(
   Year	          int
  ,Month  	      int
  ,Day	          int
  ,RentalCount	  int
  ,WeekDay	      int
  ,Holiday	      int
  ,Snow	          int
  ,FHoliday	      text
  ,FSnow	        text
  ,FWeekDay	      text
  ,PRIMARY KEY(Year, Month, Day)
  )WITH comment = 'Tabela de teste de carga';