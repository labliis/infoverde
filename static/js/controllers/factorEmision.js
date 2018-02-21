angular.module('HV').controller('FactorEmision', ['$scope','Crud',function (controller,api) {
    controller.dataFactorEmision = {resolucion : "",anio : "",factor : "",unidad : "",id:0};//nombre de la otra foranea esta es una variable global
    controller.createFactorEmision = function(){//es la funcion crear Cargo
        api.post("/api/factorEmision",controller.dataFactorEmision).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.deleteFactorEmision = function(data){
        api.delete("/api/factorEmision/"+data.fac_idfactor).then(function(response){
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearField = function(){//limpia los campos textos
        controller.dataFactorEmision = {resolucion : "",anio : "",factor : "",unidad : "",id:0};
        controller.updateFields = false;
    };

    controller.showFormUpdate = function(data){
        console.log(data);
        controller.dataFactorEmision.resolucion = data.fac_resolucion;
        controller.dataFactorEmision.id =  data.fac_idfactor;
        controller.dataFactorEmision.anio =  data.fac_anio;
        controller.dataFactorEmision.factor =  data.fac_Factor;
        controller.dataFactorEmision.unidad =  data.fac_unidad;
        controller.updateFields = true;
    };
     controller.update = function(){
        api.put("/api/factorEmision",controller.dataFactorEmision).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    }
    controller.search = function(){
        api.get("/api/factorEmision").then(function(response){
            controller.dataSearch = JSON.parse(response);
        });
    };
}]);