angular.module('HV').controller('DetailSample', ['$scope','Crud',function (controller,api) {
    controller.dataDetailSample = {oficina : "", maquina:"", cantidad:0, muestra:"" , id:0};//nombre de la otra foranea
    controller.createDetailSample = function(){
        api.post("/api/detailSample",controller.dataDetailSample).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.deleteDetailSample = function(data){
        api.delete("/api/detailSample/"+data.ofi_serial).then(function(response){
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearField = function(){
        controller.dataDetailSample = {description : "", id:0};
        controller.updateFields = false;
    };

    controller.showFormUpdate = function(data){
        controller.dataDetailSample.description = data.ofi_dscrpcion;
        controller.dataDetailSample.id =  data.ofi_serial;
        controller.updateFields = true;
    };
     controller.update = function(){
        api.put("/api/detailSample",controller.dataDetailSample).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    }
    controller.search = function(){
        api.get("/api/detailSample").then(function(response){
            controller.dataSearch = JSON.parse(response);
        });
    };
}]);