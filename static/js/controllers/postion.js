angular.module('HV').controller('Position', ['$scope','Crud',function (controller,api) {
    controller.dataPosition = {description : "",id:0};//nombre de la otra foranea esta es una variable global
    controller.createPosition = function(){//es la funcion crear Cargo
        api.post("/api/position",controller.dataPosition).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.deletePosition = function(data){
        api.delete("/api/position/"+data.car_codigo).then(function(response){
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearField = function(){//limpia los campos textos
        controller.dataPosition = {description : "", id:0};
        controller.updateFields = false;
    };

    controller.showFormUpdate = function(data){
        console.log(data);
        controller.dataPosition.description = data.car_dscrpcion;
        controller.dataPosition.id =  data.car_codigo;
        controller.updateFields = true;
    };
     controller.update = function(){
        api.put("/api/position",controller.dataPosition).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    }
    controller.search = function(){
        api.get("/api/position").then(function(response){
            controller.dataSearch = JSON.parse(response);
        });
    };
}]);