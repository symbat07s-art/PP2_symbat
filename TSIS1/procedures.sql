CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_group_id INTEGER;
BEGIN
    SELECT id INTO new_group_id
    FROM groups
    WHERE name = p_group_name;

    IF new_group_id IS NULL THEN
        INSERT INTO groups (name)
        VALUES (p_group_name)
        RETURNING id INTO new_group_id;
    END IF;

    UPDATE contacts
    SET group_id = new_group_id
    WHERE name = p_contact_name;
END;
$$;