import os
import psycopg2
from flask_sqlalchemy import SQLAlchemy

class ChatbotMemory:
    def __init__(self):
#         kwargs = {
#     "user": "postgres",
#     "password": "Ammubibi@2405",
#     "host": "localhost",
#     "port": "5432",
#     "database": "postgres",
#     "sslmode": "disable"  # Disable SSL
# }

#         # Connect to the database
        # self.conn = psycopg2.connect(**kwargs)
        # Get connection URL from env
        os.environ['DATABASE_URL'] = "postgres://zmsatwzykkntar:51d4a604128d4424a8e5d0f206d16c418ad99c5db56bca9021891da202b618e5@ec2-52-73-166-232.compute-1.amazonaws.com:5432/d73l0t540al4dn"
        conn_string = os.environ['DATABASE_URL']

        # Connect to the database
        self.conn = psycopg2.connect(conn_string)
        self.cur = self.conn.cursor()

        # Execute a CREATE TABLE statement
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs_new (
            session_uuid UUID,
            msg_id SERIAL,
            user_query TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            source TEXT,
            rating INTEGER,
            user_comment TEXT
        )
        """)

        # Commit the transaction
        self.conn.commit()

    def add_message_to_session(self, session_id, user_query, bot_response, sources=None):
        # Check if the source is available
        if sources is not None:
            sources_str = ', '.join(sources)
            # Source is available, include it in the INSERT statement
            self.cur.execute("""
                INSERT INTO chat_logs_new (session_uuid, user_query, bot_response, source) 
                VALUES (%s, %s, %s, %s) RETURNING msg_id
            """, (str(session_id), user_query, str(bot_response), sources_str))
        else:
            # Source is not available, exclude it from the INSERT statement
            self.cur.execute("""
                INSERT INTO chat_logs_new (session_uuid, user_query, bot_response) 
                VALUES (%s, %s, %s) RETURNING msg_id
            """, (str(session_id), user_query, str(bot_response)))
            
        msg_id = self.cur.fetchone()[0]
        self.conn.commit()
        return msg_id

    def get_messages_for_session(self, session_id):
        self.cur.execute("SELECT user_query, bot_response FROM chat_logs_new WHERE session_uuid = %s ORDER BY msg_id DESC", (str(session_id),))
        rows = self.cur.fetchall()
        modified_text = []
        for row in rows:
            modified_text.append({"role": "user", "content": row[0]})
            modified_text.append({"role": "assistant", "content": row[1]})
        return modified_text
    
    
    def get_sources(self, session_id):
        self.cur.execute("SELECT user_query, bot_response, source FROM chat_logs_new WHERE session_uuid = %s ORDER BY msg_id DESC LIMIT 1", (str(session_id),))
        rows = self.cur.fetchall()
        modified_text = []
        for row in rows:
            modified_text.append({"role": "user", "content": row[0]})
            modified_text.append({"role": "assistant", "content": row[1]})
            source = row[2]
            modified_text.append(source)
            print(modified_text)
        return modified_text
    
    def get_history(self, session_id):
        self.cur.execute("SELECT user_query, bot_response FROM chat_logs_new WHERE session_uuid = %s ORDER BY msg_id DESC", (str(session_id),))
        rows = self.cur.fetchall()
        rows = rows[:3]
        rows = rows[::-1]
        history = []
        for row in rows:
            history.append({"role": "user", "content": row[0]})
            history.append({"role": "assistant", "content": row[1]})
        return history

    def SaveRatings (self, data_to_sql):
        print("Found rating for msg ", data_to_sql['message_id'])
        if 'reaction' in data_to_sql:
            print("Reaction: ", data_to_sql['reaction'])
            self.cur.execute("UPDATE chat_logs_new SET rating = %s WHERE msg_id = %s", (data_to_sql['reaction'], data_to_sql['message_id']))
        elif 'userComment' in data_to_sql:
            print("Comment: ", data_to_sql['userComment'])
            self.cur.execute("UPDATE chat_logs_new SET user_comment = %s WHERE msg_id = %s", (data_to_sql['userComment'], data_to_sql['message_id']))
        self.conn.commit()