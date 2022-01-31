import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database/users.db')

    async def add_user(self, user_id):
        if await self.user_exists(user_id):
            return

        await self.__write(f"INSERT INTO users (user_id, ref) VALUES ('{user_id}', 0)")

    async def get_user(self, user_id):
        return await self.__read(f'SELECT * FROM users WHERE user_id = {user_id}')

    async def get_ref_count(self, user_id):
        temp = await self.__read(f'SELECT ref FROM users WHERE user_id = {user_id}')
        return temp[0][0]

    async def get_user_waiting_question(self, user_id):
        temp = await self.__read(f'SELECT wait_question FROM users WHERE user_id = {user_id}')
        return temp[0][0]

    async def get_image_accept(self, user_id):
        temp = await self.__read(f'SELECT image_accept FROM users WHERE user_id = {user_id}')
        return temp[0][0]

    async def get_user_lang(self, user_id):
        temp = await self.__read(f"SELECT user_lang FROM users WHERE user_id = {user_id}")
        return temp[0][0]

    async def increase_ref_count(self, user_id):
        n = await self.get_ref_count(user_id)

        await self.__write(f'UPDATE users SET ref = {n+1} WHERE user_id = {user_id}')

    async def user_exists(self, user_id):
        return await self.get_user(user_id)

    async def update_user_lang(self, lang, user_id):
        await self.__write(f"UPDATE users SET user_lang = '{lang}' WHERE user_id = {user_id}")

    async def update_image_accept(self, b: bool, user_id):
        await self.__write(f"UPDATE users SET image_accept = {b} WHERE user_id = {user_id}")

    async def update_wait_question(self, b: bool, user_id):
        await self.__write(f"UPDATE users SET wait_question = {b} WHERE user_id = {user_id}")

    async def __read(self, query):
        c = self.connection.cursor()
        c.execute(query)

        return c.fetchall()

    async def __write(self, query):
        c = self.connection.cursor()
        c.execute(query)

        c.close()
        self.connection.commit()
