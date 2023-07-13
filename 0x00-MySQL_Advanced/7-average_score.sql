-- Average score
-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student. Note: An average score can be a decimal
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id int)
BEGIN
    UPDATE users SET average_score=(SELECT AVG(score) FROM corrections AS user WHERE user.user_id=user_id)
    WHERE id=user_id;
END;$$
