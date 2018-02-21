from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
db = SQLAlchemy()
class BasTipoMaquina(db.Model):
    __tablename__='BAS_TIPO_MAQUINA'
    tip_cod = db.Column(db.Integer, primary_key=True)
    tip_dscrpcion = db.Column(db.String(40), nullable=False)
    tip_referencia = db.Column(db.String(20), nullable=False)
    tip_Ptncia_Nmnal = db.Column(db.Float)
    detailSample = db.relationship('TrnDetalleMuestra', backref='BasTipoMaquina_TrnDetalleMuestra', cascade="all, delete-orphan")
class BasOficiona(db.Model):
    __tablename__ = 'BAS_OFICINA'
    ofi_serial = db.Column(db.Integer, primary_key=True)
    ofi_tmpo_uso = db.Column(db.Float)
    ofi_tmpo_fntsma=db.Column(db.Float)
    ofi_dscrpcion = db.Column(db.CHAR(1), nullable=False)
    ofi_anio = db.Column(db.String(4), nullable=False)
    detailSample = db.relationship('TrnDetalleMuestra', backref='BasOficiona_TrnDetalleMuestra', cascade="all, delete-orphan")
class TrnDetalleMuestra(db.Model):
    __tablename__='TRN_DETALLE_MUESTRA'
    det_serial = db.Column(db.Integer, primary_key=True)
    id_Oficina = db.Column(db.Integer, db.ForeignKey('BAS_OFICINA.ofi_serial'))
    id_Maquina = db.Column(db.Integer, db.ForeignKey('BAS_TIPO_MAQUINA.tip_cod'))
    id_Muestra = db.Column(db.Integer, db.ForeignKey('BAS_MUESTRA.mue_id'))
    id_Factor = db.Column(db.Integer, db.ForeignKey('BAS_FACTOR_EMISION.fac_idfactor'))
    det_cantidad = db.Column(db.Integer, nullable=False)
    det_enrgia_cnsmda = db.Column(db.Float)
    det_co2e_gnrdo = db.Column(db.Float)
class BasFactorEmision(db.Model):
    __tablename__ = 'BAS_FACTOR_EMISION'
    fac_idfactor = db.Column(db.Integer, primary_key=True)
    fac_resolucion = db.Column(db.String(50))
    fac_anio = db.Column(db.Integer)
    fac_Factor = db.Column(db.Float, nullable=False)
    fac_unidad = db.Column(db.String(10))
    calculation = db.relationship('TrnDetalleMuestra', backref='BasFactorEmision_TrnDetalleMuestra', cascade="all, delete-orphan")
class BasMuestra(db.Model):
    __tablename__ = 'BAS_MUESTRA'
    mue_id = db.Column(db.Integer, primary_key=True)
    res_cedula = db.Column(db.Integer, db.ForeignKey('BAS_RESPONSABLE.res_cedula'))
    mue_dscrpcion = db.Column(db.String(150), nullable=False)
    mue_anio = db.Column(db.String(4), nullable=False)
    detailSample = db.relationship('TrnDetalleMuestra', backref='BasMuestra_TrnDetalleMuestra', cascade="all, delete-orphan")
class BasResponsable(db.Model):
    __tablename__ = 'BAS_RESPONSABLE'
    res_cedula = db.Column(db.Integer, primary_key=True)
    res_nombre = db.Column(db.String(40), nullable=False)
    res_apellido = db.Column(db.String(40), nullable=False)
    cod_cargo= db.Column(db.Integer, db.ForeignKey('BAS_CARGO.car_codigo'))
    sample = db.relationship('BasMuestra', backref='BasResponsable_BasMuestra', cascade="all, delete-orphan")
class BasCargo(db.Model):
    __tablename__ = 'BAS_CARGO'
    car_codigo = db.Column(db.Integer, primary_key=True)
    car_dscrpcion = db.Column(db.String(35), nullable=False)
    responsable = db.relationship('BasResponsable', backref='BasCargo_BasResponsable', cascade="all, delete-orphan")
class BasUser(db.Model):
    __tablename__ = 'BAS_USER'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(35), nullable=False)
    user_pass = db.Column(db.String(35), nullable=False)

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
