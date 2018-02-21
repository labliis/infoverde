angular.module('HV').controller('Muestra', ['$scope','Crud',function (controller,api) {
    controller.dataMuestra = {cedula:"",descripcion:"",anio:"",id:""};//nombre de la otra foranea
    controller.createMuestra = function(){
        api.post("/api/muestra",controller.dataMuestra).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.deleteMuestra = function(data){
        api.delete("/api/muestra/"+data.mue_id).then(function(response){
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearField = function(){
        controller.dataMuestra = {cedula:"",descripcion:"",anio:""};
        controller.updateFields = false;
    };

    controller.showFormUpdate = function(data){
        controller.dataMuestra.cedula=data.res_cedula;
        controller.dataMuestra.descripcion=data.mue_dscrpcion;
        controller.dataMuestra.anio=data.mue_anio;
        controller.dataMuestra.mue_id=data.mue_id;
        controller.updateFields = true;
    };
     controller.update = function(){
        api.put("/api/muestra",controller.dataMuestra).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.search = function(){
        api.get("/api/muestra").then(function(response){
            controller.dataSearch = JSON.parse(response);
        });
    };
}]);