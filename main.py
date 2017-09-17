from flask import Flask,render_template,request,jsonify
from models import db,BasTipoMaquina, BasOficiona ,AlchemyEncoder,clearQuery
from config import DevelopmentConfig
import json
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/machine")
def machine():
    return render_template('machine.html')
@app.route("/agent")
def agent():
    return render_template('agent.html')
@app.route("/office")
def office():
    return render_template('office.html')
@app.route("/sampleDetail")
def detalleMuestra():
    return render_template('detalleMuestra.html')
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('index.html')
@app.route("/api/machine",methods=['GET','POST','PUT'])
@app.route("/api/machine/<int:Id>", methods=['DELETE'])
def Machine(Id=0):
    if request.method == "GET":
        consulta = BasTipoMaquina.query.all()
        response = json.dumps(consulta, cls=AlchemyEncoder)
        response = clearQuery(response)
        response = jsonify(response)
        return response
    elif request.method == 'POST':
        data = request.json
        tMaquina = BasTipoMaquina(tip_dscrpcion=data["description"],
                                  tip_referencia=data["references"],
                                  tip_Ptncia_Nmnal=data["potencyN"],
                                  )
        db.session.add(tMaquina)
        return jsonify(db.session.commit())
    elif request.method == 'DELETE':
        db.session.query(BasTipoMaquina).filter(BasTipoMaquina.tip_cod == Id).delete()
        return jsonify(db.session.commit())
    else:
        data = request.json
        update_this = BasTipoMaquina.query.filter_by(tip_cod=data["id"]).first()
        update_this.tip_dscrpcion = data["description"]
        update_this.tip_referencia = data["references"]
        update_this.tip_Ptncia_Nmnal = data["potencyN"]
        return jsonify(db.session.commit())

@app.route("/api/office",methods=['GET','POST','PUT'])
@app.route("/api/office/<int:Id>", methods=['DELETE'])
def Office(Id=0):
    if request.method == "GET":
        consulta = BasOficiona.query.all()
        response = json.dumps(consulta, cls=AlchemyEncoder)
        response = clearQuery(response)
        response = jsonify(response)
        return response
    elif request.method == 'POST':
        data = request.json
        office = BasOficiona(ofi_dscrpcion=data["description"])
        db.session.add(office)
        return jsonify(db.session.commit())
    elif request.method == 'DELETE':
        db.session.query(BasOficiona).filter(BasOficiona.ofi_serial == Id).delete()
        return jsonify(db.session.commit())
    else:
        data = request.json
        print(data)
        update_this = BasOficiona.query.filter_by(ofi_serial=data["id"]).first()
        update_this.ofi_dscrpcion = data["description"]
        return jsonify(db.session.commit())


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():  # contexto de la aplicacion
        db.create_all()  # crea todas las tablas que no esten creadas
    app.run(debug=True, port=5000)

