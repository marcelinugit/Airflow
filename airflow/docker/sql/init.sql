CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuario (nome, email) VALUES
('João Silva', 'joao.silva@email.com'),
('Maria Souza', 'maria.souza@email.com'),
('Pedro Santos', 'pedro.santos@email.com'),
('Ana Oliveira', 'ana.oliveira@email.com'),
('Carlos Lima', 'carlos.lima@email.com');

CREATE TABLE produto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco NUMERIC(10,2) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO produto (nome, preco) VALUES
('Notebook Dell Inspiron', 4500.00),
('Monitor LG 24"', 899.90),
('Teclado Mecânico Redragon', 249.90),
('Mouse Logitech G305', 199.90),
('Headset HyperX Cloud', 349.90);