https://www.youtube.com/watch?v=8fNm6LLZ5WY

* CREATE USER wikijs WITH PASSWORD 'd2lraWpzZGI=';
* ALTER USER wikijs CREATEDB;
* GRANT ALL PRIVILEGES ON DATABASE wikidb TO wikijs;
* CREATE DATABASE wikidb;
* \c wikidb;
* GRANT CREATE ON SCHEMA public TO wikijs;


psql -h 3.135.184.94 -p 30705 -U user -d database -W

3.135.184.94:31226
