from flask import Flask,render_template, request, jsonify
from models import db,BasTipoMaquina, BasOficiona, BasCargo, BasResponsable, BasFactorEmision, BasMuestra,\
    AlchemyEncoder, json,TrnDetalleMuestra
from config import DevelopmentConfig
from horarios import Horario
from flask_wtf import CSRFProtect
from  flask import session
import form

app = Flask("InfoVerde")
app.config.from_object(DevelopmentConfig)
#csrf = CSRFProtect(app)

listPotencia = list()
listPotenciaFanta = list()
@app.route("/login",methods=['GET','POST'])
def login():
    login = form.Login(request.form)
    if request.method == "POST" and login.validate():
        session['username'] = login.userName.data
    else:
        print("Error en el formulario")
    return render_template('login.html', form=login)
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/maquina")
def machine():
    return render_template('machine.html')
@app.route("/oficina")
def office():
    return render_template('office.html')
@app.route("/detalleMuestra")
def detalleMuestra():
    return render_template('detalleMuestra.html')
@app.route("/prueba")
def prueba():
    return render_template('prueba.html')
@app.route("/cargo")
def cargo():
    return render_template('cargo.html')
@app.route("/responsable")
def responsable():
    return render_template('responsable.html')
@app.route("/muestra")
def muestra():
    return render_template('muestra.html')
@app.route("/factorEmision")
def factorEmision():
    return render_template('factorEmision.html')
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('index.html')
@app.route("/api/responsable",methods=['GET','POST','PUT'])
@app.route("/api/responsable/<int:Id>", methods=['DELETE'])
def Responsable(Id=0):
    if request.method == "GET":
        lista = list()
        response = dict()
        query = db.engine.execute("SELECT BAS_RESPONSABLE.res_cedula,BAS_RESPONSABLE.res_nombre,"
                                  "BAS_RESPONSABLE.res_apellido,BAS_CARGO.car_dscrpcion,BAS_CARGO.car_codigo "
                                  "FROM BAS_CARGO INNER JOIN BAS_RESPONSABLE ON BAS_CARGO.car_codigo = "
                                  "BAS_RESPONSABLE.cod_cargo")
        for row in query:
            response = {'id': row[0], 'name': row[1], 'lastName': row[2], 'position': row[3],
                        'idPostion': str(row[4])}
            lista.append(response)
            response = json.dumps(lista)
        response = jsonify(response)
        return response
    elif request.method == 'POST':
        data = request.json
        respon = BasResponsable(res_cedula=data["cedula"], res_nombre=data["nombre"], res_apellido=data["apellido"],
                                cod_cargo=data["cargo"])
        db.session.add(respon)
        return jsonify(db.session.commit())
    elif request.method == 'DELETE':
        db.session.query(BasResponsable).filter(BasResponsable.res_cedula == Id).delete()
        return jsonify(db.session.commit())
    else:
        data = request.json
        update_this = BasResponsable.query.filter_by(res_cedula=data["cedula"]).first()
        update_this.res_nombre = data["nombre"]
        update_this.res_apellido = data["apellido"]
        update_this.cod_cargo = data["cargo"]
        return jsonify(db.session.commit())
@app.route("/api/machine",methods=['GET','POST','PUT'])
@app.route("/api/machine/<int:Id>", methods=['DELETE'])
def Machine(Id=0):
    if request.method == "GET":
        consulta = BasTipoMaquina.query.all()
        response = json.dumps(consulta, cls=AlchemyEncoder)
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
@app.route("/api/position",methods=['GET','POST','PUT'])
@app.route("/api/position/<int:Id>", methods=['DELETE'])
def Cargo(Id=0):
    if request.method == "GET":
        consulta = BasCargo.query.all()
        response = json.dumps(consulta, cls=AlchemyEncoder)
        response = jsonify(response)
        return response
    elif request.method == 'POST':
        data = request.json
        cargo = BasCargo(car_dscrpcion=data["description"])
        db.session.add(cargo)
        return jsonify(db.session.commit())
    elif request.method == 'DELETE':
        db.session.query(BasCargo).filter(BasCargo.car_codigo == Id).delete()
        return jsonify(db.session.commit())
    else:
        data = request.json
        update_this = BasCargo.query.filter_by(car_codigo=data["id"]).first()
        update_this.car_dscrpcion = data["description"]
        return jsonify(db.session.commit())
@app.route("/api/office",methods=['GET','POST','PUT','PATCH'])
@app.route("/api/office/<int:Id>", methods=['DELETE'])
def Office(Id=0):
    if request.method == "GET":
        consulta = BasOficiona.query.all()
        response = json.dumps(consulta, cls=AlchemyEncoder)
        response = jsonify(response)

        return response
    elif request.method == 'POST':
        data = request.json
        office = BasOficiona(ofi_reserva_anual=data["reservaAnual"],ofi_dscrpcion=data["description"],
                             ofi_anio=data["anio"])
        db.session.add(office)
        return jsonify(db.session.commit())
    elif request.method == 'PATCH':
        db.engine.execute("delete from BAS_OFICINA")
        horario = Horario()
        horario = horario.getHorario()
        for i in horario:
            office = BasOficiona(ofi_dscrpcion=i["name"],
                                 ofi_anio=i["anio"], ofi_tmpo_uso=i["uso"], ofi_tmpo_fntsma=8760-i["uso"])
            db.session.add(office)
            db.session.commit()
        return ""
    elif request.method == 'DELETE':
        db.session.query(BasOficiona).filter(BasOficiona.ofi_serial == Id).delete()
        return jsonify(db.session.commit())
    else:
        data = request.json
        update_this = BasOficiona.query.filter_by(ofi_serial=data["id"]).first()
        update_this.ofi_reserva_anual = data["reservaAnual"]
        update_this.ofi_dscrpcion = data["description"]
        update_this.ofi_anio = data["anio"]
        return jsonify(db.session.commit())

@app.route("/api/muestra",methods=['GET','POST','PUT'])
@app.route("/api/muestra/<int:Id>", methods=['DELETE'])
def Muestra(Id=0):
    if request.method == "GET":
        consulta = BasMuestra.query.all()
        response = json.dumps(consulta, cls=AlchemyEncoder)
        response = jsonify(response)
        return response
    elif request.method == 'POST':
        data = request.json
        muestra = BasMuestra(res_cedula=data["cedula"], mue_dscrpcion=data["descripcion"], mue_anio=data["anio"])
        db.session.add(muestra)
        return jsonify(db.session.commit())
    elif request.method == 'DELETE':
        db.session.query(BasMuestra).filter(BasMuestra.mue_id == Id).delete()
        return jsonify(db.session.commit())
    else:
        data = request.json
        update_this = BasMuestra.query.filter_by(mue_id=data["mue_id"]).first()
        update_this.res_cedula = data["cedula"]
        update_this.mue_dscrpcion = data["descripcion"]
        update_this.mue_anio = data["anio"]
        return jsonify(db.session.commit())
@app.route("/api/factorEmision",methods=['GET','POST','PUT'])
@app.route("/api/factorEmision/<int:Id>", methods=['DELETE'])
def FactorEmision(Id=0):
    if request.method == "GET":
        consulta = BasFactorEmision.query.all()
        response = json.dumps(consulta, cls=AlchemyEncoder)
        response = jsonify(response)
        return response
    elif request.method == 'POST':
        data = request.json
        factor = BasFactorEmision(fac_resolucion=data["resolucion"],fac_anio=data["anio"],fac_Factor=data["factor"],
                                  fac_unidad=data["unidad"])
        db.session.add(factor)
        return jsonify(db.session.commit())
    elif request.method == 'DELETE':
        db.session.query(BasFactorEmision).filter(BasFactorEmision.fac_idfactor == Id).delete()
        return jsonify(db.session.commit())
    else:
        data = request.json
        update_this = BasFactorEmision.query.filter_by(fac_idfactor=data["id"]).first()
        update_this.fac_resolucion = data["resolucion"]
        update_this.fac_anio = data["anio"]
        update_this.fac_Factor = data["factor"]
        update_this.fac_unidad = data["unidad"]
        return jsonify(db.session.commit())

@app.route("/api/detailSample",methods=['GET','POST','PUT','PATCH'])
@app.route("/api/detailSample/<Id>", methods=['DELETE'])
def detailSample(Id=0):
    if request.method == "GET":
        lista = list()
        query = db.engine.execute("SELECT BAS_OFICINA.ofi_dscrpcion,BAS_OFICINA.ofi_anio, BAS_TIPO_MAQUINA.tip_dscrpcion,BAS_TIPO_MAQUINA.tip_referencia,"
                                  "BAS_MUESTRA.mue_dscrpcion, BAS_MUESTRA.mue_anio, "
                                  "BAS_FACTOR_EMISION.fac_Factor, TRN_DETALLE_MUESTRA.det_enrgia_cnsmda, "
                                  "TRN_DETALLE_MUESTRA.det_co2e_gnrdo,TRN_DETALLE_MUESTRA.det_serial FROM ((((TRN_DETALLE_MUESTRA INNER JOIN "
                                  "BAS_TIPO_MAQUINA on TRN_DETALLE_MUESTRA.id_Maquina = BAS_TIPO_MAQUINA.tip_cod )"
                                  "INNER JOIN BAS_OFICINA on TRN_DETALLE_MUESTRA.id_Oficina = BAS_OFICINA.ofi_serial)"
                                  "INNER JOIN BAS_MUESTRA on TRN_DETALLE_MUESTRA.id_Muestra = BAS_MUESTRA.mue_id)"
                                  "INNER JOIN BAS_FACTOR_EMISION on BAS_FACTOR_EMISION.fac_idfactor = "
                                  "TRN_DETALLE_MUESTRA.id_Factor)")
        for row in query:
            response = {'oficina':row[0]+" "+row[1], 'maquina':row[2]+" "+row[3], 'muestra':row[4]+" "+str(row[5]), 'factor':row[6],
                        'consumo':row[7],'co2e':row[8], 'det_serial':row[9]}
            lista.append(response)
        response = json.dumps(lista)
        response = jsonify(response)
        return response
    elif request.method == 'PATCH':
        data = request.json
        machine = BasTipoMaquina.query.filter_by(tip_cod=data["maquina"]).first()
        respMachine = json.dumps(machine, cls=AlchemyEncoder)
        respMachine = json.loads(respMachine)
        cantidad = float(data['cantidad'])
        potencia,potenciaF = cantidad*respMachine['tip_Ptncia_Nmnal'], 5*cantidad
        listPotenciaFanta.append(potenciaF)
        listPotencia.append(potencia)
        return ""
    elif request.method == 'POST':
        data = request.json
        office = BasOficiona.query.filter_by(ofi_serial=data["oficina"]).first()
        machine = BasTipoMaquina.query.filter_by(tip_cod=data["maquina"]).first()
        muestra = BasMuestra.query.filter_by(mue_id=data["muestra"]).first()
        factor = BasFactorEmision.query.filter_by(fac_idfactor=data["factor"]).first()
        respOffice = json.dumps(office, cls=AlchemyEncoder)
        respOffice= json.loads(respOffice)
        respFactor = json.dumps(factor, cls=AlchemyEncoder)
        respFactor = json.loads(respFactor)
        consumoCo2e = getEconsumCo2e(respOffice, respFactor)
        officeDetail = TrnDetalleMuestra(det_cantidad=len(listPotencia), BasOficiona_TrnDetalleMuestra=office,
                                     BasTipoMaquina_TrnDetalleMuestra=machine,
                                    BasFactorEmision_TrnDetalleMuestra=factor,
                                    BasMuestra_TrnDetalleMuestra=muestra,
                                         det_enrgia_cnsmda=consumoCo2e[0],
                                         det_co2e_gnrdo =consumoCo2e[1]
                                         )
        db.session.add(officeDetail)
        listPotencia.clear()
        listPotenciaFanta.clear()
        return jsonify(db.session.commit())
    elif request.method == 'DELETE':
        db.session.query(TrnDetalleMuestra).filter(TrnDetalleMuestra.det_serial == Id).delete()
        return jsonify(db.session.commit())
    else:
        data = request.json
        update_this = TrnDetalleMuestra.query.filter_by(det_serial=data['id']).first()
        update_this.id_Oficina = data['oficina']
        update_this.id_Maquina = data['maquina']
        update_this.id_Muestra = data['muestra']
        update_this.id_Factor = data['factor']
        update_this.det_cantidad = data["cantidad"]
        return jsonify(db.session.commit())
@app.route("/api/prueba",methods=['GET','POST','PUT','PATCH'])
@app.route("/api/prueba/<Id>", methods=['DELETE'])
def Prueba(Id=0):
    if request.method == "GET":
        lista = list()
        query = db.engine.execute("SELECT BAS_OFICINA.ofi_dscrpcion,BAS_OFICINA.ofi_anio, BAS_TIPO_MAQUINA.tip_dscrpcion,BAS_TIPO_MAQUINA.tip_referencia,"
                                  "BAS_MUESTRA.mue_dscrpcion, BAS_MUESTRA.mue_anio, "
                                  "BAS_FACTOR_EMISION.fac_Factor, TRN_DETALLE_MUESTRA.det_enrgia_cnsmda, "
                                  "TRN_DETALLE_MUESTRA.det_co2e_gnrdo,TRN_DETALLE_MUESTRA.det_serial FROM ((((TRN_DETALLE_MUESTRA INNER JOIN "
                                  "BAS_TIPO_MAQUINA on TRN_DETALLE_MUESTRA.id_Maquina = BAS_TIPO_MAQUINA.tip_cod )"
                                  "INNER JOIN BAS_OFICINA on TRN_DETALLE_MUESTRA.id_Oficina = BAS_OFICINA.ofi_serial)"
                                  "INNER JOIN BAS_MUESTRA on TRN_DETALLE_MUESTRA.id_Muestra = BAS_MUESTRA.mue_id)"
                                  "INNER JOIN BAS_FACTOR_EMISION on BAS_FACTOR_EMISION.fac_idfactor = "
                                  "TRN_DETALLE_MUESTRA.id_Factor)")
        for row in query:
            response = {'oficina':row[0]+" "+row[1], 'maquina':row[2]+" "+row[3], 'muestra':row[4]+" "+str(row[5]), 'factor':row[6],
                        'consumo':row[7],'co2e':row[8], 'det_serial':row[9]}
            lista.append(response)
        response = json.dumps(lista)
        response = jsonify(response)
        return response
    elif request.method == 'PATCH':
        data = request.json
        machine = BasTipoMaquina.query.filter_by(tip_cod=data["maquina"]).first()
        respMachine = json.dumps(machine, cls=AlchemyEncoder)
        respMachine = json.loads(respMachine)
        cantidad = float(data['cantidad'])
        potencia,potenciaF = cantidad*respMachine['tip_Ptncia_Nmnal'], 5*cantidad
        listPotenciaFanta.append(potenciaF)
        listPotencia.append(potencia)
        return ""
    elif request.method == 'POST':
        data = request.json
        office = BasOficiona.query.filter_by(ofi_serial=data["oficina"]).first()
        machine = BasTipoMaquina.query.filter_by(tip_cod=data["maquina"]).first()
        muestra = BasMuestra.query.filter_by(mue_id=data["muestra"]).first()
        factor = BasFactorEmision.query.filter_by(fac_idfactor=data["factor"]).first()
        respOffice = json.dumps(office, cls=AlchemyEncoder)
        respOffice= json.loads(respOffice)
        respFactor = json.dumps(factor, cls=AlchemyEncoder)
        respFactor = json.loads(respFactor)
        consumoCo2e = getEconsumCo2e(respOffice, respFactor)
        officeDetail = TrnDetalleMuestra(det_cantidad=len(listPotencia), BasOficiona_TrnDetalleMuestra=office,
                                     BasTipoMaquina_TrnDetalleMuestra=machine,
                                    BasFactorEmision_TrnDetalleMuestra=factor,
                                    BasMuestra_TrnDetalleMuestra=muestra,
                                         det_enrgia_cnsmda=consumoCo2e[0],
                                         det_co2e_gnrdo =consumoCo2e[1]
                                         )
        db.session.add(officeDetail)
        return jsonify(db.session.commit())
    elif request.method == 'DELETE':
        db.session.query(TrnDetalleMuestra).filter(TrnDetalleMuestra.det_serial == Id).delete()
        return jsonify(db.session.commit())
    else:
        data = request.json
        update_this = TrnDetalleMuestra.query.filter_by(det_serial=data['id']).first()
        update_this.id_Oficina = data['oficina']
        update_this.id_Maquina = data['maquina']
        update_this.id_Muestra = data['muestra']
        update_this.id_Factor = data['factor']
        update_this.det_cantidad = data["cantidad"]
        return jsonify(db.session.commit())
def getEconsumCo2e(respOffice, respFactor):
    uso = totalPotencia()*respOffice['ofi_tmpo_uso']
    fan = totalPotenciaFan()*respOffice['ofi_tmpo_fntsma']
    consumo = (uso+fan)/1000
    Co2e = consumo*respFactor['fac_Factor']
    return [consumo,Co2e]
def totalPotencia():
    total = 0.0
    for i in listPotencia:
        total += i
    return total
def totalPotenciaFan():
    total = 0.0
    for i in listPotenciaFanta:
        total += i
    return total

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():  # contexto de la aplicacion
        db.create_all()  # crea todas las tablas que no esten creadas
    app.run(debug=True, port=5000)

