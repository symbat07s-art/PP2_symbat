CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.phone
    FROM contacts c
    WHERE c.first_name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%'
    ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    IF p_limit <= 0 OR p_limit > 100 THEN
        RAISE EXCEPTION 'Limit must be between 1 and 100';
    END IF;

    IF p_offset < 0 THEN
        RAISE EXCEPTION 'Offset cannot be negative';
    END IF;

    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;