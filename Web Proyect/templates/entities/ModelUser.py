from templates.entities.User import User

class ModelUser():

    @classmethod
    def login(self, mysql, user):

        try:
            connection=mysql.connect()
            cursor= connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                user = User(row[0], row[1], User.check_password(row[2],user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, mysql, id):

        try:
            connection=mysql.connect()
            cursor= connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)