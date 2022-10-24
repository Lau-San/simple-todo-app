INSERT INTO users (username, password)
VALUES
    ('test', '$2b$10$5ysgXZUJi7MkJWhEhFcZTObGe18G1G.0rnXkewEtXq6ebVx1qpjYW'),
    ('other', '$2b$10$Wdj1lOudt3JXEc6TBI2C6.Wafuv33FRdv9jRd9qtVdPYWmKmbtiTm');

INSERT INTO tasks (user_id, title, is_completed)
VALUES
    (1, 'Test task 1', false),
    (1, 'Test task 2', true),
    (2, 'Another test task', false);
