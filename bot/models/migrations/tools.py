from tortoise import Tortoise, BaseDBAsyncClient







class HelpMigration:
    def __init__(self, conn: BaseDBAsyncClient):
        self.conn = conn

    async def table_exists(self, table_name: str) -> bool:
        result = await self.conn.execute_query_dict("SHOW TABLES LIKE %s;", (table_name,))
        return len(result) > 0

    async def get_existing_columns(self, column: str):
        result = await self.conn.execute_query_dict(f"SHOW COLUMNS FROM {column};")
        return {row["Field"] for row in result}







