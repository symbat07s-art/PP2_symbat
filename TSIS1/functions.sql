-- TSIS 1: Stored functions

-- Search by contact name, email, or any phone number.
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
    SELECT DISTINCT c.id, c.name, c.email, c.birthday, g.name, c.date_added
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    ORDER BY c.name;
$$;

-- Filter contacts by group name.
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
    SELECT c.id, c.name, c.email, c.birthday, g.name, c.date_added
    FROM contacts c
    JOIN groups g ON g.id = c.group_id
    WHERE g.name ILIKE p_group_name
    ORDER BY c.name;
$$;

-- Return one page of contacts.
CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INTEGER, p_offset INTEGER)
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
    SELECT c.id, c.name, c.email, c.birthday, g.name, c.date_added
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    ORDER BY c.name
    LIMIT p_limit OFFSET p_offset;
$$;
