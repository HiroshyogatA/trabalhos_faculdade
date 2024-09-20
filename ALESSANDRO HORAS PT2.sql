use veterinario_sql;
CREATE TABLE Internacoes ( #CRIAR TABELA INTERNAÇÕES
    id_internacoes INT PRIMARY KEY AUTO_INCREMENT,
    id_paciente INT,
    id_veterinario INT,
    data_internacao DATE,
    custo_i DECIMAL(10,2),
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente),
    FOREIGN KEY (id_veterinario) REFERENCES Veterinarios(id_veterinario)
);
INSERT INTO Internacoes (id_paciente, id_veterinario, data_internacao, custo_i ) VALUES 
(1, 1, '2024-09-19', 140.00);
SELECT * FROM Internacoes;

CREATE TABLE unidades_atdm ( #CRIAR TABELA DE UNIDADES DE ATENDIMENTO
id_unidade INT PRIMARY KEY auto_increment,
cep VARCHAR(20),
rua VARCHAR(50),
numero INT, 
bairro VARCHAR (50),
cidade VARCHAR(50),
hr_abrt TIME,
hr_fech TIME,
resp_und VARCHAR(50)
);
INSERT INTO unidades_atdm (cep, rua, numero, bairro, cidade, hr_abrt, hr_fech, resp_und ) VALUES 
('0841145', 'rua teste', '666', 'centro', 'Suzano', 0800, 1800, 'Dagoberto');
SELECT * FROM unidades_atdm;

CREATE TABLE Medicamentos (#CRIA TABELA DE REGISTRO DE MEDICAMENTOS
id_medicamento INT PRIMARY KEY auto_increment,
dt_aqs DATE,
cst DECIMAL (10,2),
vlr_rvd DECIMAL (10,2),
tp_uso VARCHAR (50),
estoque INT, 
fnd_uso VARCHAR (50)
);
INSERT INTO Medicamentos (dt_aqs, cst, vlr_rvd, tp_uso, estoque, fnd_uso ) VALUES 
('2024-09-19', 200.00, 600.00, 'injetavel', 36, 'FEBRE');
SELECT * FROM Medicamentos;
#TRIGGERS
DELIMITER //

CREATE TRIGGER verificar_estoque_baixo
AFTER INSERT ON Medicamentos
FOR EACH ROW
BEGIN
    IF NEW.estoque < 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Aviso: O estoque do medicamento está baixo!';
    END IF;
END; //

DELIMITER ;
INSERT INTO Medicamentos (dt_aqs, cst, vlr_rvd, tp_uso, estoque, fnd_uso) VALUES 
('2024-09-19', 200.00, 600.00, 'injetavel', 5, 'FEBRE');

DELIMITER //

CREATE TRIGGER verificar_horarios
AFTER INSERT ON unidades_atdm
FOR EACH ROW
BEGIN
    DECLARE msg VARCHAR(255);

    # Verifica se a unidade abre antes das 8 da manhã
    IF NEW.hr_abrt < '08:00:00' THEN
        SET msg = CONCAT('Aviso: A unidade ', NEW.id_unidade, ' abre antes das 8 da manhã.');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;

END; //

DELIMITER ;
INSERT INTO unidades_atdm (cep, rua, numero, bairro, cidade, hr_abrt, hr_fech, resp_und) VALUES 
('0841145', 'rua teste', 666, 'centro', 'Suzano', '07:30:00', '19:00:00', 'Dagoberto');
SELECT*FROM unidades_atdm;
SHOW TRIGGERS LIKE 'unidades_atdm';

DELIMITER //

CREATE TRIGGER mst_internacao
AFTER INSERT ON Internacoes
FOR EACH ROW
BEGIN
    DECLARE msg VARCHAR(255);
    SET msg = CONCAT('Paciente ID ', NEW.id_paciente, ' foi internado em ', NEW.data_internacao, 
                     ' com custo de R$', NEW.custo_i);
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
END; //

DELIMITER ;
INSERT INTO Internacoes (id_paciente, id_veterinario, data_internacao, custo_i) VALUES 
(1, 1, '2024-09-20', 150.00);

DELIMITER //

CREATE TRIGGER calcular_lucro_medicamento
AFTER INSERT ON Medicamentos
FOR EACH ROW
BEGIN
    DECLARE lucro DECIMAL(10, 2);

    # Calcula o lucro
    SET lucro = NEW.vlr_rvd - NEW.cst;

    # Exibe o lucro
    SELECT NEW.id_medicamento AS id_medicamento, lucro AS lucro;
END //

DELIMITER ;
 
 DELIMITER //

CREATE TRIGGER mstr_cep_und
AFTER INSERT ON unidades_atdm
FOR EACH ROW
BEGIN
    DECLARE msg VARCHAR(255);
    SET msg = CONCAT('Nosso CEP é: ', NEW.cep);
    # Exibir o CEP
    SIGNAL SQLSTATE '01000' SET MESSAGE_TEXT = msg; 
END //

DELIMITER ;
INSERT INTO unidades_atdm (cep, rua, numero, bairro, cidade, hr_abrt, hr_fech, resp_und) VALUES 
('0841145', 'rua teste', 666, 'centro', 'Suzano', '08:00:00', '18:00:00', 'Dagoberto');
SHOW TRIGGERS LIKE 'unidades_atdm';
#PROCEDURES
#ALTERAR VALOR DO MEDICAMENTO
DELIMITER //

CREATE PROCEDURE Alt_vlr_Med(
    IN sp_id_medicamento INT,
    IN sp_novo_valor DECIMAL(10,2)
)
BEGIN
    UPDATE Medicamentos
    SET vlr_rvd = sp_novo_valor
    WHERE id_medicamento = sp_id_medicamento;
END //

DELIMITER ;
CALL Alt_vlr_Med(1, 66.00);
SELECT*FROM Medicamentos;

#ALTERAR DADOS DO MEDICAMENTO
DELIMITER //

CREATE PROCEDURE AlterarDadosMedicamento(
    IN sp_id_medicamento INT,
    IN sp_dt_aqs DATE,
    IN sp_cst DECIMAL(10,2),
    IN sp_vlr_rvd DECIMAL(10,2),
    IN sp_tp_uso VARCHAR(50),
    IN sp_estoque INT,
    IN sp_fnd_uso VARCHAR(50)
)
BEGIN
    UPDATE Medicamentos
    SET 
        dt_aqs = sp_dt_aqs,
        cst = sp_cst,
        vlr_rvd = sp_vlr_rvd,
        tp_uso = sp_tp_uso,
        estoque = sp_estoque,
        fnd_uso = sp_fnd_uso
    WHERE id_medicamento = sp_id_medicamento;
END //

DELIMITER ;
CALL AlterarDadosMedicamento(1, '1999-01-30', 49.90, 99.80, 'Oral', 69, 'Tratamento carrapato');
SELECT*FROM Medicamentos;

#ALTERAR DADOS DA INTERNAÇÃO
DELIMITER //

CREATE PROCEDURE AlterarDadosInternacao(
    IN sp_id_internacoes INT,
    IN sp_id_paciente INT,
    IN sp_id_veterinario INT,
    IN sp_data_internacao DATE,
    IN sp_custo_i DECIMAL(10,2)
)
BEGIN
    UPDATE Internacoes
    SET 
        id_paciente = sp_id_paciente,
        id_veterinario = sp_id_veterinario,
        data_internacao = sp_data_internacao,
        custo_i = sp_custo_i
    WHERE id_internacoes = sp_id_internacoes;
END //

DELIMITER ;

CALL AlterarDadosInternacao(1, 2, 3, '1995-09-12', 500.00);
SELECT*FROM internacoes;

#ALTERAR DADOS DA UNIDADE

DELIMITER //

CREATE PROCEDURE AlterarDadosUnidade(
    IN sp_id_unidade INT,
    IN sp_cep VARCHAR(20),
    IN sp_rua VARCHAR(50),
    IN sp_numero INT,
    IN sp_bairro VARCHAR(50),
    IN sp_cidade VARCHAR(50),
    IN sp_hr_abrt TIME,
    IN sp_hr_fech TIME,
    IN sp_resp_und VARCHAR(50)
)
BEGIN
    UPDATE unidades_atdm
    SET 
        cep = sp_cep,
        rua = sp_rua,
        numero = sp_numero,
        bairro = sp_bairro,
        cidade = sp_cidade,
        hr_abrt = sp_hr_abrt,
        hr_fech = sp_hr_fech,
        resp_und = sp_resp_und
    WHERE id_unidade = sp_id_unidade;
END //

DELIMITER ;
CALL AlterarDadosUnidade(1, '08712635', 'Rua Casteluche' ,'100', 'Bairro Cidade', 'Guarulhos', '08:00:00', '17:00:00', 'Responsável Danilo');
SELECT*FROM unidades_atdm;

#ALTERAR QUANTIDADE DE MEDICAMENTO EM ESTOQUE

DELIMITER //

CREATE PROCEDURE AlterarEstoqueMedicamento(
    IN sp_id_medicamento INT,
    IN sp_novo_estoque INT
)
BEGIN
    UPDATE Medicamentos
    SET estoque = sp_novo_estoque
    WHERE id_medicamento = sp_id_medicamento;
END //

DELIMITER ;

CALL AlterarEstoqueMedicamento(1, 666);
SELECT*FROM medicamentos;