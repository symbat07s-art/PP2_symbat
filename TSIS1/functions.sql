-- 1. Search contacts by name, email, or phone
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    date_added TIMESTAMP
)
LANGUAGE SQL
AS $$
    SELECT DISTINCT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        c.date_added
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    ORDER BY c.id;
$$;


-- 2. Search contacts by group
CREATE OR REPLACE FUNCTION filter_contacts_by_group(p_group_name TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    date_added TIMESTAMP
)
LANGUAGE SQL
AS $$
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        c.date_added
    FROM contacts c
    JOIN groups g ON c.group_id = g.id
    WHERE g.name ILIKE p_group_name
    ORDER BY c.name;
$$;


-- 3. Pagination
DROP FUNCTION IF EXISTS get_contacts_page(INTEGER, INTEGER);

CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INTEGER,
    p_offset INTEGER,
    p_sort TEXT
)
RETURNS TABLE (
    contact_id INTEGER,
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    date_added TIMESTAMP
)
LANGUAGE SQL AS $$
    SELECT c.id, c.name, c.email, c.birthday, g.name, c.date_added
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY
        CASE WHEN p_sort = 'name' THEN c.name END,
        CASE WHEN p_sort = 'birthday' THEN c.birthday END,
        CASE WHEN p_sort = 'date_added' THEN c.date_added END
    LIMIT p_limit OFFSET p_offset;
$$;