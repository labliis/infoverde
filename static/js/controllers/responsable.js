angular.module('HV').controller('Responsable', ['$scope','Crud',function (controller,api) {
    controller.dataResponsable = {cedula:"",nombre:"",apellido:"",cargo:"",idPostion:""};//nombre de la otra foranea
    controller.createResponsable = function(){
        api.post("/api/responsable",controller.dataResponsable).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.deleteResponsable = function(data){
        api.delete("/api/responsable/"+data.id).then(function(response){
            console.log(data);
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearField = function(){
        controller.dataResponsable = {cedula:"",nombre:"",apellido:"", cargo:""};
        controller.updateFields = false;
    };

    controller.showFormUpdate = function(data){
        controller.dataResponsable.cedula=data.id;
        controller.dataResponsable.nombre=data.name;
        controller.dataResponsable.apellido=data.lastName;
        controller.dataResponsable.cargo = data.position;
        controller.updateFields = true;
    };
     controller.update = function(){
        api.put("/api/responsable",controller.dataResponsable).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.search = function(){
        api.get("/api/responsable").then(function(response){
            controller.dataSearch = JSON.parse(response);
            console.log(controller.dataSearch);
        });
    };
}]);