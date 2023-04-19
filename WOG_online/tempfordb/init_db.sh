echo "******** Creating DB, Table and user"

mysql -u root -p$MYSQL_ROOT_PASSWORD --execute \
"
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE TABLE $DB_NAME.$TABLE_NAME (
        id int not null auto_increment primary key,
        username varChar(255),
        score int,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
CREATE USER '$USER_NAME'@'%' IDENTIFIED BY '$USER_PASSWORD';
GRANT SELECT, INSERT, UPDATE, DELETE ON $DB_NAME.$TABLE_NAME TO '$USER_NAME'@'%';
FLUSH PRIVILEGES;
"

echo "******** Finished creating DB, Table and user"