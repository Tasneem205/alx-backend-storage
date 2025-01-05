-- average score

DELIMITER //

DROP PROCEDURE IF EXISTS computeAverage;

CREATE PROCEDURE computeAverage(
    IN user_id INT
)
BEGIN
    DECLARE avg_score FLOAT;
    
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END //

DELIMITER ;
