import requests
import inspect
from model.model_loader import ModelLoader


class WSDFTLoader(ModelLoader):

    ws_url = 'https://www.sistemas.semob.df.gov.br'
    resources_to_sql = {
        'AREAS_INTEGRACAO': '/summary/of/areas',
        'LINHAS': '/summary/of/linhas',
        'PERCURSOS': '/summary/of/percursos',
        'PARADAS': '/summary/of/paradas',
        'PARADAS_PERCURSOS': '/summary/of/paradas_percursos',
        'PARADAS_AREAS_INTEGRACAO': '/summary/of/paradas_areas_integracao',
        'TERMINAIS': '/summary/of/terminais',
        'PERCURSOS_TERMINAIS': '/summary/of/percursos_terminais',
        'OPERADORES': '/summary/of/operadores',
        'PERCURSOS_OPERACOES': '/summary/of/percursos_operacoes'
    }

    def load_resource(self, resource):
        url = self.ws_url + self.resources_to_sql[resource.name]
        return self._parse(requests.get(url).json(), resource.resource_type)

    @staticmethod
    def _parse(result_list, resource_type):
        type_spec = inspect.getfullargspec(resource_type.__init__)
        args_dict = resource_type.__init__.__annotations__

        attrs = [args_dict[arg] for arg in type_spec.args[1:]]

        values_list = [[result[attr] for attr in attrs] for result in result_list]

        return [resource_type(*tuple(line)) for line in values_list]
