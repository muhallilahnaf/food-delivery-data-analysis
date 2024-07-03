-- change the CSV file path as necessary

COPY restaurant
	FROM 'C:\Users\Public\Documents\rest_clean.csv' 
	DELIMITER ',' CSV HEADER;

COPY menu
	FROM 'C:\Users\Public\Documents\menu_clean.csv' 
	DELIMITER ',' CSV HEADER;
	
COPY variations
	FROM 'C:\Users\Public\Documents\variations_clean.csv' 
	DELIMITER ',' CSV HEADER;
	
COPY cuisines
	FROM 'C:\Users\Public\Documents\cuisines.csv' 
	DELIMITER ',' CSV HEADER;
	
COPY cui_rest_dim(cui_id, rest_code)
	FROM 'C:\Users\Public\Documents\cuisines_rest.csv' 
	DELIMITER ',' CSV HEADER;
