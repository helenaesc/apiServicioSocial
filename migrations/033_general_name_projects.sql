UPDATE project
SET general_name = name
WHERE general_name IS NULL
   OR TRIM(general_name) = '';
