from django.db import models
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView,CreateView, DeleteView, UpdateView
from usuarios.forms import UserForm,UserUpdateForm
from usuarios.models import Usuario
from django.utils.decorators import method_decorator
import re
from django.db.models import Q1a
# Create your models here.
class IndexView(ListarView):
    """
    * Vista basada en clase para la lista de usuarios*:
    + *template_name*: nombre del template que vamos a renderizar
    + *model*: modelo que vamos a listar.
    """
    template_name = 'usuario_list'
    model = Usuario

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    class CrearUsurio(CrearView):
        """
                *Vista Basada en Clase para crear usuarios*:
                    + *template_name*: nombre del template que vamos renderizar
                    + *form_class*: formulario para crear usuarios
                    + *success_url*: url en caso de exito
            """
        template_name = 'usuarios/crear.html'
        form_class = UserForm
        success_url = '/usuarios'

        # @user_passes_test(lambda user: user.is_superuser)
        @method_decorator(login_required)
        def dispatch(self, *args, **kwargs):
            return super(CrearUsuario, self).dispatch(*args, **kwargs)

        class UserMixin(object):
            """
                *Vista Basada en Clase para soporte de eliminacion de usuario*:
                    + *model*: modelo a ser eliminado
            """
            model = Usuario

        def get_context_data(self, **kwargs):
                kwargs.update({'object_name': 'Usuario'})
                return kwargs

        class EliminarUsuario(UserMixin, EliminarView):
            """
                *Vista Basada en Clase para eliminar usuarios*:
                    + *template_name*: nombre del template a ser rendirizado
                    + *success_url: url a ser redireccionada en caso de exito*
            """
            template_name = 'usuarios/eliminar.html'

            success_url = '/usuarios'

            @method_decorator(login_required)
            def dispatch(self, *args, **kwargs):
                return super(EliminarUsuario, self).dispatch(*args, **kwargs)

            class ModificarUsuario(ModificarView):
                """
                    *Vista Basada en Clase para modificar un usuario:*
                        +*template_name*: template a ser renderizado
                        +*model*: modelo que se va modificar
                        +*form_class*:Formulario para actualizar el usuario
                        +*success_url*: url a ser redireccionada en caso de exito
                """
                template_name = 'usuarios/modificar.html'
                model = Usuario
                form_class = UserUpdateForm
                success_url = '/usuarios/'

                @method_decorator(login_required)
                def dispatch(self, *args, **kwargs):
                    return super(EliminarUsuario, self).dispatch(*args, **kwargs)

                def normalize_query(query_string,
                                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                                    normspace=re.compile(r'\s{2,}').sub):
                    """
                    Splits the query string in invidual keywords, getting rid of unecessary spaces
                        and grouping quoted words together.
                        Example:
                        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
                        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
                    :param query_string: cadena completa de busqueda
                    :param findterms: expresion regular para encontrar las palabras
                    :param normspace: expresion regular para normalizar el espacio
                    :return: una lista de palabras separadas y normalizadas
                    """

                    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

                def get_query(query_string, search_fields):
                    """
                    :param query_string: Cadena que se va usar para la busqueda.
                    :param search_fields: Campos que se usan para comparar con la cadena de busqueda.
                    :return: Retorna una lista, que es una combinacion de objetos Q que cumplen con
                    la cadena de busqueda parcial o totalmente.
                    """
                    query = None  # Query to search for every search term
                    terms = normalize_query(query_string)
                    for term in terms:
                        or_query = None  # Query to search for a given term in each field
                        for field_name in search_fields:
                            q = Q(**{"%s__icontains" % field_name: term})
                            if or_query is None:
                                or_query = q
                            else:
                                or_query = or_query | q
                        if query is None:
                            query = or_query
                        else:
                            query = query & or_query
                    return query

                @login_required
                def buscar(request):
                    """
                    :param request: request HTTP
                    :return: retorna una lista de objetos que cumplan con el parametro de busqueda.
                    """
                    query_string = ''
                    found_entries = None
                    if ('busqueda' in request.GET) and request.GET['busqueda'].strip():
                        query_string = request.GET['busqueda']

                        entry_query = get_query(query_string, ['username', 'first_name', 'last_name'])

                        found_entries = Usuario.objects.filter(entry_query).order_by('username')
                    return render_to_response('usuarios/search_results.html',
                                              {'query_string': query_string, 'found_entries': found_entries},
                                              context_instance=RequestContext(request))
