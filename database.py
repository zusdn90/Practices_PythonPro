import sqlite3

# 영속 계층
class DatabaseManager:
    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        # 데이터 트랜잭션 처리를 위해 컨텍스트 매니저 사용
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])  # 전달된 값을 플레이스 홀더에 제공하여 구문을 실행한다.
            return cursor

    def create_table(self, table_name, columns):
        columns_with_types = [
            f"{column_name} {data_type}" for column_name, data_type in columns.items()
        ]

        self._execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            """
        )

    def drop_table(self, table_name):
        self._execute(f"DROP TABLE {table_name};")

    def add(self, table_name, data):
        placeholders = ", ".join("?" * len(data))
        column_names = ", ".join(data.keys())
        column_values = tuple(data.values())

        self._execute(
            f"""
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            """,
            column_values,
        )

    def delete(self, table_name, criteria):
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            """,
            tuple(criteria.values()),
        )

    def select(self, table_name, criteria=None, order_by=None):
        criteria = criteria or {}  # <1>

        query = f"SELECT * FROM {table_name}"

        if criteria:  # <2>
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            query += f" WHERE {select_criteria}"

        if order_by:  # <3>
            query += f" ORDER BY {order_by}"

        return self._execute(  # <4>
            query,
            tuple(criteria.values()),
        )

    def update(self, table_name, criteria, data):
        update_placeholders = [f"{column} = ?" for column in criteria.keys()]
        update_criteria = " AND ".join(update_placeholders)

        data_placeholders = ", ".join(f"{key} = ?" for key in data.keys())

        values = tuple(data.values()) + tuple(criteria.values())

        self._execute(
            f"""
            UPDATE {table_name}
            SET {data_placeholders}
            WHERE {update_criteria};
            """,
            values,
        )