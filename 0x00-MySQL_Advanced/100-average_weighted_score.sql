-- Average weighted score
-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id int)
BEGIN
    DECLARE average FLOAT;
    SET average=(SELECT SUM(score*weight) / SUM(weight)
    FROM users AS u JOIN corrections as c ON u.id=c.user_id
    JOIN projects AS p ON c.project_id=p.id WHERE u.id=user_id);
    UPDATE users SET average_score=average WHERE id=user_id;
END;$$
