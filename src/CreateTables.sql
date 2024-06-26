-- Creación de la tabla User
CREATE TABLE IF NOT EXISTS "User" (
    userId BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    registrationDate DATE NOT NULL
);

-- Creación de la tabla ToDo
CREATE TABLE IF NOT EXISTS ToDo (
    todoId BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    creationDate DATE NOT NULL,
    limitDate DATE NOT NULL,
    status SMALLINT NOT NULL,
    priority SMALLINT NOT NULL
);

-- Creación de la tabla User-ToDo
CREATE TABLE IF NOT EXISTS UserToDo (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    userId BIGINT NOT NULL REFERENCES "User"(userId) ON UPDATE CASCADE,
    todoId BIGINT NOT NULL REFERENCES ToDo(todoId) ON UPDATE CASCADE,
    CONSTRAINT user_todo_unique UNIQUE (userId, todoId)
);
