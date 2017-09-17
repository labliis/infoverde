angular.module('HV').controller('Office', ['$scope','Crud',function (controller,api) {
    controller.dataOffice = {description : "",id:0};//nombre de la otra foranea
    controller.createOffice = function(){
        api.post("/api/office",controller.dataOffice).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.deleteOffice = function(data){
        api.delete("/api/office/"+data.ofi_serial).then(function(response){
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearField = function(){
        controller.dataOffice = {description : "", id:0};
        controller.updateFields = false;
    };

    controller.showFormUpdate = function(data){
        controller.dataOffice.description = data.ofi_dscrpcion;
        controller.dataOffice.id =  data.ofi_serial;
        controller.updateFields = true;
    };
     controller.update = function(){
        api.put("/api/office",controller.dataOffice).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    }
    controller.search = function(){
        api.get("/api/office").then(function(response){
            controller.dataSearch = JSON.parse(response);
        });
    };
}]);