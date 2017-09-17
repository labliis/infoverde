angular.module('HV').controller('Agent', ['$scope','Crud',function (controller,api) {
    controller.dataAgent = {machine : "",};//nombre de la otra foranea
    controller.createAgent = function(){
        alert(controller.dataAgent.machine);
    };
    /*controller.data = {description : "", references : "",potencyN:"", id:0};
    controller.create = function(){
        api.post("/agent",controller.data).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.searchAgent = function(){
        api.get("/agent").then(function(response){
            controller.dataSearch = JSON.parse(response);
        });
    };
    controller.deleteAgent = function(data){
        api.delete("/agent/"+data.tip_cod).then(function(response){
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearFieldAgent = function(){
        controller.data = {description : "", references : "",potencyN:""};
    };
    controller.showFormUpdateAgent = function(data){
        controller.data.description = data.tip_dscrpcion;
        controller.data.references = data.tip_referencia;
        controller.data.potencyN =  data.tip_Ptncia_Nmnal;
        controller.data.id = data.tip_cod;
        controller.updateFields = true;
    };
    controller.updateAgent = function(){
        api.put("/agent",controller.data).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };*/
}]);