-- Create a new schema called 'data'
CREATE SCHEMA healthcare_data;

-- Create table 'use_case' within the 'data' schema
CREATE TABLE healthcare_data.use_case (
    id SERIAL PRIMARY KEY,
    master_schema JSONB NOT NULL
);

-- Create table 'schema_details' within the 'data' schema
CREATE TABLE healthcare_data.schema_details (
    id SERIAL PRIMARY KEY,
    data_schema JSONB NOT NULL,
    -- *** Need to add a field that's the comparison to the master_schema ***
    use_case_id INTEGER,
    CONSTRAINT fk_use_case FOREIGN KEY (use_case_id)
        REFERENCES healthcare_data.use_case (id)
);

-- Insert data into the 'use_case' table
INSERT INTO healthcare_data.use_case (master_schema)
VALUES
('{ "patient": { "id": "int", "name": "text", "age": "int" }, "visit": { "id": "int", "date": "date" } }'::jsonb);

-- Insert data into the 'schema_details' table
INSERT INTO healthcare_data.schema_details (data_schema, use_case_id)
VALUES
('{ "patient": { "id": 101, "name": "John Doe", "age": 30 }, "visit": { "id": 501, "date": "2023-10-01" } }'::jsonb, 1),
('{ "patient": { "id": 102, "name": "Jane Smith", "age": 25 }, "visit": { "id": 502, "date": "2023-10-02" } }'::jsonb, 1);
