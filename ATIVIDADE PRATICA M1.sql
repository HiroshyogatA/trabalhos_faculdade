CREATE DATABASE veterinario_sql;
USE veterinario_sql;

CREATE TABLE Pacientes ( #CRIAR TABELA PACIENTES
    id_paciente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    especie VARCHAR(50),
    idade INT 
);

INSERT INTO Pacientes (nome, especie, idade) VALUES 
('Costela', 'Cachorro', 5),
('Trovão', 'Gato', 3),
('Joaquim', 'Cachorro', 2);

SELECT * FROM Pacientes;

CREATE TABLE Veterinarios ( #CRIAR TABELA VETERINARIOS
    id_veterinario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    especialidade VARCHAR(50)
);

INSERT INTO Veterinarios (nome, especialidade) VALUES 
('Mario', 'Aves'),
('Danilo', 'Insetos');

SELECT * FROM Veterinarios;

CREATE TABLE Consultas ( #CRIAR TABELA CONSULTAS
    id_consulta INT PRIMARY KEY AUTO_INCREMENT,
    id_paciente INT,
    id_veterinario INT,
    data_consulta DATE,
    custo DECIMAL(10,2),
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente),
    FOREIGN KEY (id_veterinario) REFERENCES Veterinarios(id_veterinario)
);

INSERT INTO Consultas (id_paciente, id_veterinario, data_consulta, custo) VALUES 
(1, 1, '2024-09-19', 150.00);

SELECT * FROM Consultas;

# PROCEDURES
DELIMITER // 

CREATE PROCEDURE agendar_consulta (
    IN id_paciente INT,
    IN id_veterinario INT,
    IN data_consulta DATE,
    IN custo DECIMAL(10, 2)
)
BEGIN
    INSERT INTO Consultas (id_paciente, id_veterinario, data_consulta, custo)
    VALUES (id_paciente, id_veterinario, data_consulta, custo);
END //

DELIMITER ;
CALL agendar_consulta(1, 2, '2024-09-20', 666.00);

DELIMITER //

CREATE PROCEDURE atualizar_paciente (
    IN id_paciente INT,
    IN novo_nome VARCHAR(100),
    IN nova_especie VARCHAR(50),
    IN nova_idade INT
)
BEGIN
    UPDATE pacientes
    SET nome = novo_nome,
        especie = nova_especie,
        idade = nova_idade
    WHERE id_paciente = id_paciente;
END //

DELIMITER ;

CALL atualizar_paciente(1, 'Costelinha', 'Cachorro', 7);

DELIMITER //

CREATE PROCEDURE remover_consulta (
    IN id_consulta INT
)
BEGIN
    DELETE FROM Consultas
    WHERE id_consulta = id_consulta;
END //

DELIMITER ;
CALL remover_consulta(1);

DELIMITER //
#FUNCTIONS
CREATE FUNCTION total_gasto_paciente(id_paciente INT) 
RETURNS DECIMAL(10, 2)
BEGIN
    DECLARE total DECIMAL(10, 2);
    
    SELECT COALESCE(SUM(custo), 0) INTO total
    FROM Consultas
    WHERE id_paciente = id_paciente;
    
    RETURN total;
END //

DELIMITER ;
SELECT total_gasto_paciente(1) AS gasto_total;

DELIMITER //
#TRIGGER
CREATE TRIGGER verificar_idade_paciente
BEFORE INSERT ON Pacientes
FOR EACH ROW
BEGIN
    IF NEW.idade < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Idade inválida: deve ser um número positivo.';
    END IF;
END //

DELIMITER ;
INSERT INTO Pacientes (nome, especie, idade) VALUES ('Centopeia', 'Chilopoda', -2);

CREATE TABLE Log_Consultas ( 
    id_log INT PRIMARY KEY AUTO_INCREMENT,
    id_consulta INT,
    custo_antigo DECIMAL(10, 2),
    custo_novo DECIMAL(10, 2)
);

DELIMITER //

CREATE TRIGGER atualizar_custo_consulta
AFTER UPDATE ON Consultas
FOR EACH ROW
BEGIN
    IF NEW.custo <> OLD.custo THEN
        INSERT INTO Log_Consultas (id_consulta, custo_antigo, custo_novo) 
        VALUES (OLD.id_consulta, OLD.custo, NEW.custo);
    END IF;
END //

DELIMITER ;
UPDATE Consultas SET custo = 790.00 WHERE id_consulta = 1; 

SELECT*FROM log_consultas