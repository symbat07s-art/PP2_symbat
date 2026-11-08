-- Practice 8: PostgreSQL stored procedures

-- 1. Insert a contact, or update the phone if the name already exists
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_name IS NULL OR TRIM(p_name) = '' THEN
        RAISE EXCEPTION 'Name cannot be empty';
    END IF;

    IF p_phone IS NULL OR p_phone !~ '^\+?[0-9]{7,15}$' THEN
        RAISE EXCEPTION 'Invalid phone number. Use 7 to 15 digits, optionally starting with +';
    END IF;

    IF EXISTS (
        SELECT 1 FROM contacts WHERE name = p_name
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- 2. Process many contacts and return invalid rows
-- Input format:
-- [
--   {"name": "Daniel", "phone": "87001112233"},
--   {"name": "", "phone": "123"}
-- ]
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    IN p_contacts JSONB,
    INOUT p_invalid JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    item JSONB;
    v_name VARCHAR;
    v_phone VARCHAR;
    v_error TEXT;
BEGIN
    p_invalid := '[]'::JSONB;

    IF jsonb_typeof(p_contacts) IS DISTINCT FROM 'array' THEN
        RAISE EXCEPTION 'Input must be a JSON array';
    END IF;

    FOR item IN
        SELECT value FROM jsonb_array_elements(p_contacts)
    LOOP
        v_name := item->>'name';
        v_phone := item->>'phone';

        IF v_name IS NULL OR TRIM(v_name) = ''
           OR v_phone IS NULL
           OR v_phone !~ '^\+?[0-9]{7,15}$'
        THEN
            p_invalid := p_invalid || jsonb_build_array(
                item || jsonb_build_object(
                    'error', 'Invalid name or phone number'
                )
            );
        ELSE
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM contacts WHERE name = v_name
                ) THEN
                    UPDATE contacts
                    SET phone = v_phone
                    WHERE name = v_name;
                ELSE
                    INSERT INTO contacts(name, phone)
                    VALUES (v_name, v_phone);
                END IF;

            EXCEPTION
                WHEN OTHERS THEN
                    GET STACKED DIAGNOSTICS v_error = MESSAGE_TEXT;

                    p_invalid := p_invalid || jsonb_build_array(
                        item || jsonb_build_object('error', v_error)
                    );
            END;
        END IF;
    END LOOP;
END;
$$;


-- 3. Delete contacts by name or phone
-- Pass NULL for the search field that is not being used.
CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_name IS NULL AND p_phone IS NULL THEN
        RAISE EXCEPTION 'Provide a name or a phone number';
    END IF;

    DELETE FROM contacts
    WHERE (p_name IS NOT NULL AND name = p_name)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;
