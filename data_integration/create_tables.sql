-- create restaurant table

CREATE TABLE IF NOT EXISTS restaurant (
	rest_code CHAR(4) PRIMARY KEY,
	budget INT NOT NULL,
	is_vat_included BOOLEAN,
	is_voucher_enabled BOOLEAN,
	is_super_vendor BOOLEAN,
	vertical_segment VARCHAR(30),
	customer_type VARCHAR(10),
	latitude NUMERIC(10,8) NOT NULL,
	area VARCHAR(30),
	longitude NUMERIC(10,8) NOT NULL,
	post_code INT,
	primary_cuisine_id INT,
	rating NUMERIC(3,2) CHECK (rating >= 0 AND rating <= 5),
	review_number INT,
	chain_main_vendor_code CHAR(4)
);


-- create menu table

CREATE TABLE IF NOT EXISTS menu (
	food_id INT PRIMARY KEY,
	food_name VARCHAR(100) NOT NULL,
	master_category_id INT,
	is_express_item BOOLEAN,
	category_name VARCHAR(100),
	rest_code CHAR(4) NOT NULL,
	CONSTRAINT fk_rest_code
		FOREIGN KEY(rest_code)
			REFERENCES restaurant(rest_code)
			ON DELETE CASCADE
);


-- create variations table

CREATE TABLE IF NOT EXISTS variations (
	var_id INT PRIMARY KEY,
	var_name VARCHAR(255),
	price NUMERIC(6,1) NOT NULL,
	food_id INT NOT NULL,
	rest_code CHAR(4) NOT NULL,
	CONSTRAINT fk_rest_code
		FOREIGN KEY(rest_code)
			REFERENCES restaurant(rest_code)
			ON DELETE CASCADE,
	CONSTRAINT fk_food_id
		FOREIGN KEY(food_id)
			REFERENCES menu(food_id)
			ON DELETE CASCADE
);


-- create cuisines table

CREATE TABLE IF NOT EXISTS cuisines (
	cui_id INT PRIMARY KEY,
	cui_name VARCHAR(255) NOT NULL,
);


-- create cui_rest dim table

CREATE TABLE IF NOT EXISTS cui_rest_dim (
	cr_id SERIAL PRIMARY KEY,
	cui_id INT NOT NULL,
	rest_code CHAR(4) NOT NULL,
	CONSTRAINT fk_rest_code
		FOREIGN KEY(rest_code)
			REFERENCES restaurant(rest_code)
			ON DELETE CASCADE,
	CONSTRAINT fk_cui_id
		FOREIGN KEY(cui_id)
			REFERENCES cuisines(cui_id)
			ON DELETE CASCADE
);
