import psycopg2
from tabulate import tabulate
import pandas as pd
import emoji
from tqdm import tqdm
from Utils.logger import logger


class PostgresTool():
    
    def __init__(self, host, user, port, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database

        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            port=port,
            password=password
        )
        self.conn.autocommit = False
        self.cur = self.conn.cursor()
    
    def close(self):
        self.cur.close()
        self.conn.close()

    def query(self, sql_query, show=True):
        print(sql_query)
        try:
            self.cur.execute("ROLLBACK")
            self.cur.execute(sql_query)
            if sql_query.strip().upper().startswith("SELECT"):
                if show:
                    rows = self.cur.fetchall()
                    print(tabulate(rows, headers=[desc[0] for desc in self.cur.description], tablefmt='psql'))
                else:
                    return self.cur.fetchall()
            # else:
            #     self.conn.commit()  # Commit giao dịch cho các truy vấn không phải SELECT
        except Exception as e:
            # logger.error(f"Có lỗi xảy ra: {e}")
            pass

    def get_columns(self, table_name):
        query = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
        """
        self.cur.execute(query)
        columns = [row[0] for row in self.cur.fetchall()]
        return columns

    def get_all_table(self,):
        self.cur.execute("ROLLBACK")
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'")
        tables = [i[0] for i in self.cur.fetchall()]
        return tables
    


    def export_to_csv(self, table_name, output_path):
        try:
            query = f'SELECT * FROM "{table_name}";'
            self.cur.execute(query)
            rows = self.cur.fetchall()
            columns = [desc[0] for desc in self.cur.description]

            df = pd.DataFrame(rows, columns=columns)
            df.to_csv(output_path, index=False)
            logger(f'./logs/export_{table_name}.log', emoji.emojize(f":check_mark_button: Data exported successfully to {output_path}! :check_mark_button:"))
        except Exception as e:
            error_message = f":cross_mark: {str(e)}"
            logger(f'./logs/export_{table_name}.log', emoji.emojize(error_message))

    def push_data(self, table_name, data):
        try:
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            query = f'INSERT INTO "{table_name}" ({columns}) VALUES ({values})'
    
            self.cur.execute(query, list(data.values()))
            self.conn.commit()
            logger(f'./logs/export_{table_name}.log', emoji.emojize(f":check_mark_button: Data pushed successfully to {table_name}! :check_mark_button:"))
        except Exception as e:
            self.conn.rollback()
            error_message = f":cross_mark: {str(e)}"
            logger(f'./logs/export_{table_name}.log', emoji.emojize(error_message))
