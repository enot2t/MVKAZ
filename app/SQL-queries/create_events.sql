CREATE TABLE events (
    id SERIAL PRIMARY KEY,  -- Уникальный идентификатор (автоинкремент)
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Время создания записи (автогенерация)
    user_id INT NOT NULL,  -- ID пользователя
    start_dt DATE NOT NULL,  -- Дата начала события
    end_dt DATE NOT NULL,  -- Дата окончания события
    name TEXT,  -- Название события
    mode VARCHAR(50) NOT NULL,  -- Тип события (временное или постоянное)
    place TEXT,  -- Место проведения события
    description TEXT,  -- Описание события
    duration INT  -- Длительность события в днях
);