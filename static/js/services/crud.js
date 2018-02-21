angular.module('HV').service('Crud', ['$http', '$q', '$httpParamSerializer', function (api, respuestaServidor, serializador) {
    this.post = function (url,datos) {
        var datosPost = respuestaServidor.defer();
        api.post(url,datos).success(function (datos) {
            datosPost.resolve(datos);
        }).error(function (error) {
            datosPost.reject(error);
        });
        return datosPost.promise;
    };
    this.patch = function (url,datos) {
        var datosPatch = respuestaServidor.defer();
        api.patch(url,datos).success(function (datos) {
            datosPatch.resolve(datos);
        }).error(function (error) {
            datosPatch.reject(error);
        });
        return datosPatch.promise;
    };
    this.get = function (url) {
        var datosGet = respuestaServidor.defer();
        api.get(url).success(function (datos) {
            datosGet.resolve(datos);
        }).error(function (error) {
            datosGet.reject(error);
        });
        return datosGet.promise;
    };
    this.put = function (url,data) {
        var datosDelete = respuestaServidor.defer();
        api.put(url,data).success(function (datos) {
            datosDelete.resolve(datos);
        }).error(function (error) {
            datosDelete.reject(error);
        });
        return datosDelete.promise;
    };
    this.delete = function (url) {
        var datosDelete = respuestaServidor.defer();
        api.delete(url).success(function (datos) {
            datosDelete.resolve(datos);
        }).error(function (error) {
            datosDelete.reject(error);
        });
        return datosDelete.promise;
    };
}]);