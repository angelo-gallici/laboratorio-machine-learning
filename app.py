import pickle
import json
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)  # Creamos la aplicación Flask

# Cargar modelos y archivos
FEATURES = pickle.load(open("churn/models/features.pk", "rb"))
model = pickle.load(open("churn/models/model.pk", "rb"))
column_equivalence = pickle.load(open("churn/models/column_equivalence.pk", "rb"))

# Función para convertir valores en numéricos
def convert_numerical(features):
    output = []
    for i, feat in enumerate(features):
        if i in column_equivalence:
            output.append(column_equivalence[i].get(feat, 0))  # Convertir texto en número
        else:
            try:
                output.append(pd.to_numeric(feat))
            except:
                output.append(0)
    return output

# Definir la API que recibe datos y hace predicciones
@app.route('/query', methods=['GET', 'POST'])
def query_example():
    try:
        if request.method == 'GET':
            feats = request.args.get('feats')  # Leer datos desde la URL
        else:
            data = request.get_json()  # Leer datos desde el cuerpo (POST)
            feats = data.get('feats')

        if not feats:
            return jsonify({'error': 'No features provided'}), 400

        features = convert_numerical(feats.split(','))  # Convertir datos

        prediction = model.predict([features])  # Hacer predicción

        return jsonify({'prediction': int(prediction[0])})  # Enviar respuesta en JSON

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Manejo de errores

if __name__ == '__main__':
    app.run(debug=True, port=3001)


"""
import pickle
import json
from flask import Flask, request
import pandas as pd


FEATURES = pickle.load(open("churn/models/features.pk", "rb"))

model = pickle.load(open("churn/models/model.pk", "rb"))
column_equivalence = pickle.load(open("churn/models/column_equivalence.pk", "rb"))

# create the Flask app
app = Flask(__name__)

def convert_numerical(features):
    output = []
    for i, feat in enumerate(features):
        if i in column_equivalence:
            output.append(column_equivalence[i][feat])
        else:
            try:
                output.append(pd.to_numeric(feat))
            except:
                output.append(0)
    return output

@app.route('/query')
def query_example():
    features = convert_numerical(request.args.get('feats').split(','))
    response = {
        'response': [int(x) for x in model.predict([features])]
    }
    return json.dumps(response)

if __name__ == '__main__':
    # run app in debug mode on port 3001
    app.run(debug=True, port=3001)
"""