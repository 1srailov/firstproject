import sqlite3
import asyncio


db = sqlite3.connect('users.db')
sql = db.cursor()

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('users.db')
        
    async def add_user(self, user_id):
        if await self.__user_exists(user_id):
            return 
        
        query = f"INSERT INTO users (user_id) VALUES ('{user_id}')"

        await self.__write_data(query)
    
    
    async def update_photo_path(self, user_id, new_path):
        query = f"UPDATE users SET photo_path = '{new_path}' WHERE user_id = {user_id}"
        
        return await self.__write_data(query)
    
    async def update_last_msg_id(self, user_id, new_msg_id):
        query = f"UPDATE users SET last_msg_id = '{new_msg_id}' WHERE user_id = {user_id}"
        
        return await self.__write_data(query)
    
