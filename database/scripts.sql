-- Create a new schema called 'data'
CREATE SCHEMA healthcare_data;

-- Create table 'schema_details' within the 'data' schema
CREATE TABLE healthcare_data.schema_details (
    id SERIAL PRIMARY KEY,
    data_schema JSON NOT NULL,
    use_case_id INTEGER
);

-- Create table 'use_case' within the 'data' schema
CREATE TABLE healthcare_data.use_case (
    id SERIAL PRIMARY KEY,
    master_schema JSON NOT NULL
);

-- Add a foreign key constraint to the 'schema_details' table
ALTER TABLE healthcare_data.schema_details
ADD CONSTRAINT fk_use_case
FOREIGN KEY (use_case_id)
REFERENCES healthcare_data.use_case (id);
