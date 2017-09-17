from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
db = SQLAlchemy()

class BasTipoMaquina(db.Model):
    __tablename__='BAS_TIPO_MAQUINA'
    tip_cod = db.Column(db.Integer,primary_key=True)
    tip_dscrpcion = db.Column(db.String(40))
    tip_referencia = db.Column(db.String(20))
    tip_Ptncia_Nmnal = db.Column(db.Float)
    def __init__(self,tip_dscrpcion,tip_referencia,tip_Ptncia_Nmnal):
        self.tip_dscrpcion=tip_dscrpcion
        self.tip_referencia=tip_referencia
        self.tip_Ptncia_Nmnal=tip_Ptncia_Nmnal


class BasOficiona(db.Model):
    __tablename__ = 'BAS_OFICINA'
    ofi_serial = db.Column(db.Integer,primary_key=True)
    ofi_dscrpcion = db.Column(db.String(30))
class TrnDetalleMuestra(db.Model):
    __tablename__='TRN_DETALLE_MUESTRA'
    det_serial = db.Column(db.Integer,primary_key=True)
    id_Oficina = db.Column(db.Integer,db.ForeignKey('BAS_OFICINA.ofi_serial'))
    id_Maquina = db.Column(db.Integer,db.ForeignKey('BAS_TIPO_MAQUINA.tip_cod'))
    id_Muestra = db.Column(db.Integer,db.ForeignKey('BAS_MUESTRA.mue_id'))
    cantidad = db.Column(db.Integer)
class DetalleOficina(db.Model):
    __tablename__ = 'Trn_DETALLE_OFICINA'
    id = db.Column(db.Integer,primary_key=True)
    id_Oficiona = db.Column(db.Integer,db.ForeignKey('BAS_OFICINA.ofi_serial'))
    id_Maquina = db.Column(db.Integer, db.ForeignKey('BAS_OFICINA.ofi_serial'))
    cantidad = db.Column(db.Integer)
class BasCargo(db.Model):
    __tablename__ = 'BAS_CARGO'
    car_codigo = db.Column(db.Integer, primary_key=True)
    car_dscrpcion = db.Column(db.String(30))
class BasResponsable(db.Model):
    __tablename__ = 'BAS_RESPONSABLE'
    res_cedula = db.Column(db.Integer, primary_key=True)
    res_nombre = db.Column(db.String(30))
    res_apellido = db.Column(db.String(30))
    cod_cargo= db.Column(db.Integer, db.ForeignKey('BAS_CARGO.car_codigo'))
class BasFactorEmision(db.Model):
    __tablename__ = 'BAS_FACTOR_EMISION'
    fac_idfactor = db.Column(db.Integer, primary_key=True)
    fac_resolucion = db.Column(db.String(50))
    fac_anio = db.Column(db.Integer)
    fac_Factor = db.Column(db.Float)
    fac_unidad = db.Column(db.String(6))
class BasMuestra(db.Model):
    __tablename__ = 'BAS_MUESTRA'
    mue_id = db.Column(db.Integer,primary_key=True)
    res_cedula = db.Column(db.Integer, db.ForeignKey('BAS_RESPONSABLE.res_cedula'))
    mue_dscrpcion = db.Column(db.String(40))
    mue_mes_ini = db.Column(db.String(11))
    mue_mes_fin = db.Column(db.String(11))
    mue_cant_meses = db.Column(db.Integer)
class BasCalculo(db.Model):
    __tablename__ = 'BAS_CALCULO'
    cal_id = db.Column(db.Integer, primary_key=True)
    cal_idFactor = db.Column(db.Integer, db.ForeignKey('BAS_FACTOR_EMISION.fac_idfactor'))
    cal_idMuestra = db.Column(db.Integer, db.ForeignKey('BAS_MUESTRA.mue_id'))
    cal_tmpo_uso = db.Column(db.Float)
    cal_tmpo_fntsma= db.Column(db.Float)
    cal_energia_cnsmda= db.Column(db.Float)
    cal_co2e_gnrdo= db.Column(db.Float)

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)
def clearQuery(response):
    res = ""
    for i in response:
        res += i
    res = res.replace("\"query\": null,", "")
    res = res.replace("\"query_class\": null,", "")
    return res