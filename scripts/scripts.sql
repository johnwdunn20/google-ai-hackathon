-- Create a new schema called 'data'
-- CREATE SCHEMA healthcare_data;

DROP TABLE IF EXISTS healthcare_data.schema_details;
DROP TABLE IF EXISTS healthcare_data.use_case;

-- Create table 'use_case' within the 'data' schema
CREATE TABLE healthcare_data.use_case (
    id SERIAL PRIMARY KEY,
    description VARCHAR,
    master_schema JSONB NOT NULL
);

-- Create table 'schema_details' within the 'data' schema
CREATE TABLE healthcare_data.schema_details (
    id SERIAL PRIMARY KEY,
    data_schema JSONB NOT NULL,
    comparison_to_master_schema VARCHAR,
    use_case_id INTEGER,
    CONSTRAINT fk_use_case FOREIGN KEY (use_case_id)
        REFERENCES healthcare_data.use_case (id)
);

-- Insert data into the 'use_case' table
INSERT INTO healthcare_data.use_case (master_schema, description)
VALUES
('{ "patient": { "id": "int", "name": "text", "age": "int" }, "visit": { "id": "int", "date": "date" } }'::jsonb, 'Simple Example');

-- Insert data into the 'schema_details' table
INSERT INTO healthcare_data.schema_details (data_schema, use_case_id)
VALUES
('{ "patient": { "id": "int", "name": "text", "age": "int" }, "visit": { "id": "int", "date": "date" } }'::jsonb, 1),
('{ "patient": { "id": "int", "name": "text" }, "visit": { "id": "int", "date": "date" } }'::jsonb, 1);