-- 1)Buscar o nome e o CPF dos médicos que também são pacientes do hospital
SELECT M.nome, M.cpf
FROM Médicos M
JOIN Pacientes P ON M.cpf = P.cpf;

-- 2) Buscar o nome e o CPF dos médicos ortopedistas, e a data das suas consultas, para os ortopedistas que têm consulta marcada com a paciente Ana
SELECT M.nome, M.cpf, C.data
FROM Médicos M
JOIN Consultas C ON M.codm = C.codm
JOIN Pacientes P ON C.codp = P.codp
WHERE M.specialidade = 'Ortopedista' AND P.nome = 'Ana';

-- 3)Buscar o nome e o CPF dos médicos que têm consultas marcadas com todos os pacientes:
SELECT M.nome, M.cpf
FROM Médicos M
WHERE NOT EXISTS (
    SELECT 1 
    FROM Pacientes P
    WHERE NOT EXISTS (
        SELECT 1
        FROM Consultas C
        WHERE C.codm = M.codm AND C.codp = P.codp
    )
);

-- 4)Buscar o nome e o CPF dos médicos ortopedistas que têm consultas marcadas com todos os pacientes de Florianópolis:

SELECT M.nome, M.cpf
FROM Médicos M
WHERE M.specialidade = 'Ortopedista'
AND NOT EXISTS (
    SELECT 1 
    FROM Pacientes P
    WHERE P.cidade = 'Florianópolis'
    AND NOT EXISTS (
        SELECT 1
        FROM Consultas C
        WHERE C.codm = M.codm AND C.codp = P.codp
    )
);

-- subconsultas na cláusula FROM
-- 1) Buscar a data e a hora das consultas marcadas para a médica Maria

SELECT C.data, C.hora
FROM (
    SELECT codm
    FROM Médicos
    WHERE nome = 'Maria'
) AS M
JOIN Consultas C ON M.codm = C.codm;

--2) Buscar o nome e a cidade dos pacientes que têm consultas marcadas com ortopedistas
SELECT P.nome, P.cidade
FROM (
    SELECT codm
    FROM Médicos
    WHERE specialidade = 'Ortopedista'
) AS M
JOIN Consultas C ON M.codm = C.codm
JOIN Pacientes P ON C.codp = P.codp;

--3)Buscar o nome e o CPF dos médicos que atendem no mesmo ambulatório do médico Pedro

SELECT M.nome, M.cpf
FROM (
    SELECT A.nroa
    FROM Médicos M
    JOIN Ambulatórios A ON M.codm = A.nroa
    WHERE M.nome = 'Pedro'
) AS Amb
JOIN Médicos M ON M.nroa = Amb.nroa;
