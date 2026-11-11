CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


INSERT INTO groups (name)
VALUES
    ('Family'),
    ('Work'),
    ('Friend'),
    ('Other')
ON CONFLICT (name) DO NOTHING;



ALTER TABLE contacts
ADD COLUMN IF NOT EXISTS email VARCHAR(100),
ADD COLUMN IF NOT EXISTS birthday DATE,
ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id),
ADD COLUMN IF NOT EXISTS date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP;


UPDATE contacts
SET group_id = (
    SELECT id FROM groups WHERE name = 'Other'
)
WHERE group_id IS NULL;


CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (
        type IN ('home', 'work', 'mobile')
    ),
    UNIQUE (contact_id, phone)
);



INSERT INTO phones (contact_id, phone, type)
SELECT id, phone, 'mobile'
FROM contacts
WHERE phone IS NOT NULL AND TRIM(phone) <> ''
ON CONFLICT (contact_id, phone) DO NOTHING;