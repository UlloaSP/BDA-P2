-- Creación de la tabla User
CREATE TABLE User (
    userId BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    registrationDate DATE NOT NULL
);

-- Creación de la tabla ToDo
CREATE TABLE ToDo (
    todoId BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    creationDate DATE NOT NULL,
    limitDate DATE NOT NULL,
    status TINYINT NOT NULL,
    priority TINYINT NOT NULL
);

-- Creación de la tabla UserToDo (tabla intermedia)
CREATE TABLE UserToDo (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    userId BIGINT NOT NULL REFERENCES User(userId) ON DELETE CASCADE ON UPDATE CASCADE,
    todoId BIGINT NOT NULL REFERENCES ToDo(todoId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT user_todo_unique UNIQUE (userId, todoId)
);
