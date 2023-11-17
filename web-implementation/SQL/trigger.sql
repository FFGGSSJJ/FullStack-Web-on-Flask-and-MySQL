CREATE TRIGGER before_register BEFORE INSERT ON account_info FOR EACH ROW
BEGIN
    SET @num = (SELECT COUNT(account_name) FROM account_info WHERE account_name = NEW.account_name);
    IF @num >= 1 THEN
        SET new.userID = 666;
    END IF;
    IF LEN(NEW.account_passwd)<=5 THEN
        SET new.userID = 888;
    END IF;
END;
    