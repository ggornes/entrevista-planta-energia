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
		id,
		nombre,
		id_tipo_dispositivo,
		id_status_dispositivo,
		potencia_actual,
		fecha_alta,
		fecha_actualizacion
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
		id,
		id_dispositivo,
		id_tipo_dispositivo,
		potencia_actual,
		timestamp
	);
	""")


