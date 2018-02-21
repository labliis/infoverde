angular.module('HV').controller('Office', ['$scope','Crud',function (controller,api) {
    controller.dataOffice = {description : "",tiempoUso:"",tiempoFantasma:"",anio:"",id:0};//nombre de la otra foranea
    controller.cantidadPaginas = 0;
    controller.dataOfficeShow = [];

    controller.createOffice = function(){
        api.post("/api/office",controller.dataOffice).then(function(response){
            controller.clearField();
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.automaticUpdate = function(){
        api.patch("/api/office", controller.dataOffice).then(function(response){
            controller.search();
        });
    };
    controller.deleteOffice = function(data){
        api.delete("/api/office/"+data.ofi_serial).then(function(response){
            controller.search();//consulta de nuevo la bd
        });
    };
    controller.clearField = function(){
        controller.dataOffice = {description : "",tiempoUso:"",tiempoFantasma:"",anio:"",id:0};
        controller.updateFields = false;
    };

    controller.showFormUpdate = function(data){
        controller.dataOffice.description = data.ofi_dscrpcion;
        controller.dataOffice.tiempoUso = data.ofi_tmpo_uso;
        controller.dataOffice.tiempoFantasma = data.ofi_tmpo_fntsma;
        controller.dataOffice.anio = data.ofi_anio;
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
            controller.cantidadPaginas = Math.floor(controller.dataSearch.length/10);
            if(controller.dataSearch.length%10!=0){
                controller.cantidadPaginas++;
            }
            controller.pagination(1);
        });
    };
    controller.pagination = function(range){
        controller.dataOfficeShow = [];
        for(var i=range*10-10;i<range*10 && i<controller.dataSearch.length;i++){
            controller.dataOfficeShow.push(controller.dataSearch[i]);
        }
        controller.activar = "active";
    };
    controller.range = function(max) {
        var input = [];
        for (var i = 1; i <= max; i++)
            input.push(i);
        return input;
    };
}]);
