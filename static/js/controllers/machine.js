angular.module('HV').controller('Machine', ['$scope','Crud',function (controller,api) {
    controller.data = {description : "", references : "",potencyN:"", id:0};
    controller.create = function(){
        api.post("/api/machine",controller.data).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.search = function(){
        api.get("/api/machine").then(function(response){
            controller.dataSearch = JSON.parse(response);
        });
    };
    controller.deleteMachine = function(data){
        api.delete("/api/machine/"+data.tip_cod).then(function(response){
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearField = function(){
        controller.data = {description : "", references : "",potencyN:""};
        controller.updateFields = false;
    };
    controller.showFormUpdate = function(data){
        controller.data.description = data.tip_dscrpcion;
        controller.data.references = data.tip_referencia;
        controller.data.potencyN =  data.tip_Ptncia_Nmnal;
        controller.data.id = data.tip_cod;
        controller.updateFields = true;
    };
    controller.update = function(){
        api.put("/api/machine",controller.data).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
}]);