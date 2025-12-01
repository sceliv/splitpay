from app.database import engine

def test_connection():
    try:
        conn = engine.connect()
        print("Conexión exitosa a MySQL")
        conn.close()
    except Exception as e:
        print("Error:", e)

test_connection()
