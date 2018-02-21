angular.module('HV').controller('DetailSample', ['$scope','Crud',function (controller,api) {
    controller.dataDetailSample = {factor : "",oficina : "", maquina:"", cantidad:"", muestra:"" , id:""};//nombre de la otra foranea
    controller.createDetailSample = function(){
        api.post("/api/detailSample",controller.dataDetailSample).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.addMachineQuantity = function(){
        api.patch("/api/detailSample", controller.dataDetailSample).then(function(response){
        });
    };
    controller.deleteDetailSample = function(data){
        api.delete("/api/detailSample/"+data.det_serial).then(function(response){
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearField = function(){
        controller.dataDetailSample = {factor : "",oficina : "", maquina:"", cantidad:"", muestra:"" , id:""};
        controller.updateFields = false;
    };

    controller.showFormUpdate = function(data){
        controller.dataDetailSample.cantidad = data.det_cantidad;
        controller.dataDetailSample.oficina = data.id_Oficina;
        controller.dataDetailSample.oficina = data.id_Maquina;
        controller.dataDetailSample.oficina = data.id_Muestra;
        controller.dataDetailSample.oficina = data.id_Factor;
        controller.dataDetailSample.id = data.det_serial;
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