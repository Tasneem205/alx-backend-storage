-- validation
DROP TRIGGER IF EXISTS reset_valid;

DELIMITER //
CREATE TRIGGER reset_valid
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END //

DELIMITER ;
