import psycopg2
conn = psycopg2.connect(database="student_info", user="postgres", \
                        password="123456789", host="localhost", port="5432")