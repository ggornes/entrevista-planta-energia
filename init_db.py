# import sqlite3 module
import sqlite3

# create con object to connect
# the database geeks_db.db
con = sqlite3.connect("planta.db")

# create the cursor object
cur = con.cursor()

# execute the script by creating the table
# named geeks1 and insert the data
cur.executescript("""
	create table dispositivos(
		ID INTEGER PRIMARY KEY AUTOINCREMENT,
		nombre TEXT NOT NULL,
		id_tipo_dispositivo INTEGER NOT NULL,
		id_status_dispositivo INTEGER NOT NULL,
		potencia_actual REAL NOT NULL,
		fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	""")

cur.executescript("""
CREATE TABLE status_dispositivo(
		id,
		descripcion
	);
insert into status_dispositivo values ( '1', 'operacion' );
insert into status_dispositivo values ( '2', 'mantenimiento' );
	""")

cur.executescript("""
CREATE TABLE tipo_dispositivo(
		id,
		nombre_tipo_dispositivo
	);
insert into tipo_dispositivo values ( '1', 'aero_generador' );
insert into tipo_dispositivo values ( '2', 'celda_fotovaltica' );
insert into tipo_dispositivo values ( '3', 'turbina_hidroelectrica' );
	""")

cur.executescript("""
	create table lecturas(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		id_dispositivo,
		id_tipo_dispositivo,
		potencia_actual,
		timestamp
	);
	""")


