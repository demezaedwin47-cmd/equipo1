import functions_framework
import pymysql

DB_CONFIG = {
    "host": "136.114.184.231",
    "user": "webuser",
    "password": "Huevos12345678.",
    "database": "mi_proyecto_db",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "connect_timeout": 10
}

@functions_framework.http
def hello_http(request):
    mensaje = ""
    usuarios_html = ""
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG, ssl={'fake_flag_to_enable_tls': True})
        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            email = request.form.get("email", "").strip()
            if nombre and email:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s)", (nombre, email))
                conn.commit()
                mensaje = "✅ Usuario guardado correctamente."

        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre, email, fecha_registro FROM usuarios ORDER BY id DESC LIMIT 10")
            for row in cursor.fetchall():
                usuarios_html += f"<p><b>#{row['id']}</b> {row['nombre']} - {row['email']}<br><small>{row['fecha_registro']}</small></p>"
    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if conn: conn.close()

    return f"<html><head><meta charset='utf-8'><title>Registro</title><style>body{{font-family:Arial;padding:20px;}}.container{{max-width:400px;margin:auto;background:white;padding:20px;border-radius:10px;box-shadow:0 0 10px gray;}}input{{width:100%;padding:10px;margin:5px 0;box-sizing:border-box;}}button{{width:100%;padding:10px;background:#4285F4;color:white;border:none;cursor:pointer;}}</style></head><body><div class='container'><h2>Registro de Usuario</h2><div style='color:blue;'>{mensaje}</div><form method='POST'><input name='nombre' placeholder='Nombre' required><input name='email' type='email' placeholder='Email' required><button>Guardar</button></form><h3>Registrados</h3>{usuarios_html}</div></body></html>", 200, {'Content-Type': 'text/html; charset=utf-8'}
