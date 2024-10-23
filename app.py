from flask import Flask, jsonify, request, render_template
from db_config import get_mongo_connection, get_mysql_connection

app = Flask(__name__)
from bson.objectid import ObjectId

@app.route('/asignar', methods=['GET', 'POST'])
def asignar_alumno_form():
    db_connection = get_mysql_connection()
    cursor = db_connection.cursor(dictionary=True)

    if request.method == 'POST':
        documento = request.form['documento']
        curso_id = request.form['curso_id']

        # Verificar si el alumno existe en MongoDB
        db = get_mongo_connection()
        alumno = db["alumnos"].find_one({"documento": documento})
        if not alumno:
            return jsonify({"error": "Alumno no encontrado"}), 404

        # Verificar si el curso existe en MySQL
        cursor.execute("SELECT * FROM cursos WHERE id = %s", (curso_id,))
        curso = cursor.fetchone()
        if not curso:
            return jsonify({"error": "Curso no encontrado"}), 404

        # Asignar el ID del alumno de MongoDB al curso en MySQL
        if curso['id_alumno']:
            id_alumnos = curso['id_alumno'].split(',')
        else:
            id_alumnos = []

        # Agregar el nuevo alumno si no está ya asignado
        if str(alumno["_id"]) not in id_alumnos:
            id_alumnos.append(str(alumno["_id"]))

        # Guardar los IDs actualizados en la base de datos
        cursor.execute("UPDATE cursos SET id_alumno = %s WHERE id = %s", (','.join(id_alumnos), curso_id))
        db_connection.commit()

        return jsonify({"message": f"Alumno con documento {documento} asignado al curso {curso_id}."})

    # Si es un GET, mostrar la lista de cursos con los alumnos asignados
    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    # Obtener los nombres de los alumnos desde MongoDB
    db = get_mongo_connection()
    for curso in cursos:
        if curso['id_alumno']:
            alumnos_ids = curso['id_alumno'].split(',')  # Obtener IDs de alumnos
            curso['alumnos'] = []
            for alumno_id in alumnos_ids:
                try:
                    # Convertir a ObjectId y buscar en MongoDB
                    alumno = db["alumnos"].find_one({"_id": ObjectId(alumno_id.strip())})
                    if alumno:
                        curso['alumnos'].append({"nombre": alumno['nombre'], "documento": alumno['documento']})
                    else:
                        curso['alumnos'].append({"nombre": "Alumno no encontrado", "documento": ""})
                except Exception as e:
                    curso['alumnos'].append({"nombre": "Error en búsqueda", "documento": str(e)})
        else:
            curso['alumnos'] = []

    return render_template('asignar.html', cursos=cursos)

if __name__ == '__main__':
    app.run(debug=True)
