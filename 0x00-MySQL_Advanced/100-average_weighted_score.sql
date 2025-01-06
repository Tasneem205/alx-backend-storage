-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Create the procedure
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_sum FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    DECLARE score FLOAT;
    DECLARE weight INT;
    
    -- Calculate weighted sum and total weight
    DECLARE cur CURSOR FOR
        SELECT c.score, p.weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;
    
    OPEN cur;
    
    -- Iterate through each correction to calculate the weighted sum and total weight
    read_loop: LOOP
        FETCH cur INTO score, weight;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET weighted_sum = weighted_sum + (score * weight);
        SET total_weight = total_weight + weight;
    END LOOP;
    
    CLOSE cur;
    
    -- If total_weight is greater than 0, compute the weighted average, otherwise set it to 0
    IF total_weight > 0 THEN
        UPDATE users SET average_score = weighted_sum / total_weight WHERE id = user_id;
    ELSE
        UPDATE users SET average_score = 0 WHERE id = user_id;
    END IF;
END$$
DELIMITER ;
