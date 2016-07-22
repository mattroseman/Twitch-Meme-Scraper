# Twitch-Meme-Scraper
Dependencies
```
Python 2.7 only
sudo apt-get install python-mysqldb

WINDOWS - .exe file
https://pypi.python.org/pypi/MySQL-python/1.2.5

```

Reference
```
http://zetcode.com/db/mysqlpython/
http://code.activestate.com/recipes/299411-connect-to-an-irc-server-and-store-messages-into-a/
http://stackoverflow.com/questions/23100704/running-infinite-loops-using-threads-in-python
https://pymotw.com/2/threading/ -- Daemon threading

```
MYSQL Function Syntax
(this is the current function we have)

```
DELIMITER $$
DROP PROCEDURE IF EXISTS `updateTimestamp` $$
CREATE DEFINER=`root`@`%` PROCEDURE `updateTimestamp`()
BEGIN
DECLARE increment INT;
DECLARE toplimit INT;
DECLARE formatThis VARCHAR(255);
DECLARE formatted DATETIME;
SET increment = 1;
SET toplimit = (SELECT COUNT(id) FROM messages);
WHILE (increment <= toplimit) DO
    SET formatThis = (SELECT timestamp FROM `messages` WHERE id = increment);
    SET formatted = str_to_date(formatThis, '%b %d %T %Y');
    UPDATE `messages` SET `time` = formatted WHERE `messages`.`id` = increment;
    SET increment = increment + 1;
  END WHILE;
END $$
DELIMITER ;
```
To call updateTimestamp just do 
```
call updateTimestamp();
```

TODO: 
  1. Create/Destroy/Join threads to properly terminate program


