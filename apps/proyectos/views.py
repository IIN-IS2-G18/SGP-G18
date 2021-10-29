
from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404
from requests import request
from .models import Proyecto, Equipo, Sprint, UserStory, HistorialUS, RolProyecto, RolProyectoUsuarios
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.views.generic import DetailView
from . import forms
from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404


class ProyectoCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View creado específicamente para crear un proyecto.

    Utiliza un LoginRequiredMixin para asegurarnos de que solo puede ser accedida
    por usuarios que están logueados y hereda del CreateView.
    """
    permission_required = 'proyectos.crear_proyecto'
    raise_exception = True
    model = Proyecto
    fields = '__all__'

    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todos los equipos dentro del proyecto
        y las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(ProyectoCrear, self).get_context_data(**kwargs)
        context["equipos"] = Equipo.objects.all()
        context["estados"] = Proyecto.ESTADOS
        return context

    def get_success_url(self):
        """
        Override de la función original

        Se implementa un template personalizado en caso de que el proyecto fue creado/actualizado exitosamente
        :return: redireccionamiento hacia la página de éxito
        """
        return reverse('home')

    def form_valid(self, form):
        """
        En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
        :param form:
        :return: Redireccionamiento a la página de éxito
        """
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
        durante la creación del form.
        :param form:
        :return: Reload del form con errores.
        """
        context = {
            'form': form
        }
        print(form.errors)
        return super(ProyectoCrear, self).render_to_response(self.get_context_data(**context),)


class ProyectoEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    View creado para actualizar el proyecto en caso de ser necesario.
    
    Utiliza un LoginRequiredMixin para asegurarnos de que solo puede ser accedida
    por usuarios que están logueados y hereda del CreateView.
    
    """
    template_name = 'proyectos/proyecto_modificar.html'
    permission_required = 'proyectos.editar_proyecto'
    raise_exception = True
    model = Proyecto
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Override creado para incluir más datos a los datos del contexto y poder
        visualizarlos en el template correspondiente.
        :param kwargs:
        :return: contexto
        """
        context = super(ProyectoEditar, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        """
        :return: el path del template personalizado.
        """
        return reverse('home')

    def form_valid(self, form):
        """
                En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
                :param form:
                :return: Redireccionamiento a la página de éxito
                """
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
        durante la creación del form.
        :param form:
        :return: Reload del form con errores.
        """
        context = {
            'form': form
        }
        print(form.errors)
        return super(ProyectoEditar, self).render_to_response(self.get_context_data(**context))


class ProyectoBorrar(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    View implementado para eliminar un proyecto de la base de datos

    Requiere que el usuario esté logueado y hereda de DeleteView.

    El template es una página que solicita una confirmación para eliminar el proyecto.

    El url de éxito redirige a home.
    """
    template_name = 'proyectos/proyecto_eliminar.html'
    permission_required = 'proyectos.borrar_proyecto'
    raise_exception = True
    model = Proyecto
    success_url = '/'


class ProyectoDetalle(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyectos/proyecto_detalle.html'
    permission_required = 'proyectos.ver_proyecto'

    def get_context_data(self, **kwargs):
        context = super(ProyectoDetalle, self).get_context_data(**kwargs)
        id_proyecto = self.kwargs['pk']
        proyecto = Proyecto.objects.get(id=id_proyecto)
        equipo = Equipo.objects.filter(proyecto=id_proyecto)
        context["proyecto"] = proyecto
        context["equipo"] = equipo
        return context


class EquipoCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Equipo
    permission_required = 'proyectos.crear_equipo'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todos los equipos dentro del proyecto
        y las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(EquipoCrear, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        """
        Override de la función original

        Se implementa un template personalizado en caso de que el proyecto fue creado/actualizado exitosamente
        :return: redireccionamiento hacia la página de éxito
        """
        return reverse('home')

    def form_valid(self, form):
        """
        En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
        :param form:
        :return: Redireccionamiento a la página de éxito
        """
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
        durante la creación del form.
        :param form:
        :return: Reload del form con errores.
        """
        context = {
            'form': form
        }
        return super(EquipoCrear, self).render_to_response(self.get_context_data(**context),)


class EquipoModificar(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Equipo
    permission_required = ('proyectos.agregar_integrante', 'proyectos.eliminar_integrante')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todos los equipos dentro del proyecto
        y las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(EquipoModificar, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        """
        Override de la función original

        Se implementa un template personalizado en caso de que el proyecto fue creado/actualizado exitosamente
        :return: redireccionamiento hacia la página de éxito
        """
        return reverse('home')

    def form_valid(self, form):
        """
        En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
        :param form:
        :return: Redireccionamiento a la página de éxito
        """
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
        durante la creación del form.
        :param form:
        :return: Reload del form con errores.
        """
        context = {
            'form': form
        }
        return super(EquipoModificar, self).render_to_response(self.get_context_data(**context),)


class EquipoBorrar(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    View implementado para eliminar un proyecto de la base de datos

    Requiere que el usuario esté logueado y hereda de DeleteView.

    El template es una página que solicita una confirmación para eliminar el proyecto.

    El url de éxito redirige a home.
    """
    template_name = 'proyectos/equipo_eliminar.html'
    permission_required = 'proyectos.eliminar_equipo'
    raise_exception = True
    model = Equipo
    success_url = '/'



class SprintCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # Se especifica el models para crear view
    permission_required = 'sprint.crear_sprint'
    raise_exception = True
    model = Sprint
    # Se especifican los fields a ser desplegados
    fields = [
            "numero_sprint",
            "fecha_inicio",
            "fecha_fin",
            "duracion",
            "proyecto",
            "estado",
    ]

    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todas las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(SprintCrear, self).get_context_data(**kwargs)
        context["estados"] = Proyecto.ESTADOS
        context["proyecto"] = self.kwargs['pkproy']
        return context

    def get_success_url(self):
        """
        Override de la función original

        Se implementa un template personalizado en caso de que el proyecto fue creado/actualizado exitosamente
        :return: redireccionamiento hacia la página de éxito
        """
        URL = self.request.GET.get('next')
        return URL

    def form_valid(self, form):
        """
            En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
            :param form:
            :return: Redireccionamiento a la página de éxito
        """
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
        durante la creación del form.
        :param form:
        :return: Reload del form con errores.
        """
        print(form.errors)
        context = {
            'form': form
        }
        return super(SprintCrear, self).render_to_response(self.get_context_data(**context),)


class SprintModificar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
        template_name = 'proyectos/sprint_modificar.html'
        permission_required = 'sprint.editar_sprint'
        raise_exception = True
        model = Sprint
        fields = [
            "numero_sprint",
            "fecha_inicio",
            "fecha_fin",
            "duracion",
            "proyecto",
            "estado",
        ]
        # Se puede especificar url exitoso
        # Url para redireccionar despues del exito
        # modificando detalles
        success_url = "/"

        def get_context_data(self, **kwargs):
            """
            Override creado para incluir más datos a los datos del contexto y poder
            visualizarlos en el template correspondiente.
            :param kwargs:
            :return: contexto
            """
            context = super(SprintModificar, self).get_context_data(**kwargs)
            return context

        def get_success_url(self):
            """
            :return: el path del template personalizado.
            """
            return reverse('home')

        def form_valid(self, form):
            """
                    En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
                    :param form:
                    :return: Redireccionamiento a la página de éxito
                    """
            form.save()
            return HttpResponseRedirect(self.get_success_url())

        def form_invalid(self, form):
            """
            Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
            durante la creación del form.
            :param form:
            :return: Reload del form con errores.
            """
            context = {
                'form': form
            }
            print(form.errors)
            return super(SprintModificar, self).render_to_response(self.get_context_data(**context))


class SprintEliminar(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'proyectos/sprint_eliminar.html'
    permission_required = 'sprint.borrar_sprint'
    raise_exception = True
    model = Sprint
    success_url = "/"


class UserStoryCrear(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
        permission_required = 'userstory.crear_us'
        raise_exception = True
        # Se especifica el models para crear view
        template_name = 'proyectos/userstory_form.html'
        model = UserStory
        # Se especifican los fields a ser desplegados
        fields = [
            "nombre",
            "descripcion",
            "prioridad",
            # "estado",
            # "proyecto",
            # "sprint",
        ]

        def get_context_data(self, **kwargs):
            """

            Override de la función original, agregamos el query de todas las opciones para los estados.

            El contexto puede ser accedido directamente en el template de proyecto_form.html
            Agregamos al context para poder colocarlos como opciones en la lista desplegable.

            :param kwargs:
            :return: contexto
            """
            context = super(UserStoryCrear, self).get_context_data(**kwargs)
            context["prioridades"] = UserStory.PRIORIDADES
            return context

        def form_invalid(self, form):
            """
            Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
            durante la creación del form.
            :param form:
            :return: Reload del form con errores.
            """
            context = {
                'form': form
            }
            print(form.errors)
            return super(UserStoryCrear, self).render_to_response(self.get_context_data(**context))


class UserStoryModificar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
        permission_required = 'userstory.modificar_us'
        raise_exception = True
        template_name = 'userstory/userstory_modificar.html'
        model = UserStory
        fields = [
            "nombre",
            "descripcion",
            "prioridad",
            "estado",
            "proyecto",
            "sprint",
        ]


class UserStoryEliminar(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
        permission_required = 'userstory.borrar_us'
        raise_exception = True
        template_name = 'proyectos/userstory_eliminar.html'
        model = UserStory
        success_url = "/"


class RolProyectoCrear(CreateView, LoginRequiredMixin):
    model = RolProyecto
    template_name = 'proyectos/roles/rolproyecto_form.html'
    fields = [
        "nombre",
        "permisos"
    ]
    '''
        def dispatch(self, request, *args, **kwargs):
            get_object_or_404(Proyecto, pk=kwargs['pk'])
            return super().dispatch(request, *args, **kwargs)
    '''
    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todas las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(RolProyectoCrear, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        """
        Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
        durante la creación del form.
        :param form:
        :return: Reload del form con errores.
        """
        context = {
            'form': form
        }
        print(form.errors)
        return super(RolProyectoCrear, self).render_to_response(self.get_context_data(**context))

    def get_success_url(self):
        """
        :return: el path del template personalizado.
        """
        return reverse('home')

    def form_valid(self, form):
        """
        En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
        :param form:
        :return: Redireccionamiento a la página de éxito
        """
        #form.instance.proyecto = Proyecto.objects.get(id=self.kwargs["pk"])
        form.save()

        return HttpResponseRedirect(self.get_success_url())


class AgregarUsuariosRolView(LoginRequiredMixin, CreateView):
        model = RolProyectoUsuarios
        template_name = 'proyectos/roles/agregar_usuarios_rol.html'
        fields = "__all__"
        def dispatch(self, request, *args, **kwargs):
            get_object_or_404(Proyecto, pk=kwargs['pk'])
            return super().dispatch(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            """

            Override de la función original, agregamos el query de todas las opciones para los estados.

            El contexto puede ser accedido directamente en el template de proyecto_form.html
            Agregamos al context para poder colocarlos como opciones en la lista desplegable.

            :param kwargs:
            :return: contexto
            """
            context = super(AgregarUsuariosRolView, self).get_context_data(**kwargs)
            proyecto = get_object_or_404(Proyecto, pk=self.kwargs["pk"])
            context["roles"] = RolProyecto.objects.all()
            context["miembros"] = proyecto.equipo.usuarios.all()
            context["proyecto"] = proyecto
            return context

        def get_success_url(self):
            """
            Override de la función original

            Se implementa un template personalizado en caso de que el proyecto fue creado/actualizado exitosamente
            :return: redireccionamiento hacia la página de éxito
            """
            return reverse('home')

        def form_valid(self, form):
            """
            En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
            :param form:
            :return: Redireccionamiento a la página de éxito
            """

            usuario = form.cleaned_data["usuarios"]
            RolProyectoUsuarios.objects.filter(usuarios=usuario, rol=form.cleaned_data["rol"]).delete()
            usuario.user_permissions.set(usuario.user_permissions.all() | form.cleaned_data["rol"].permisos.all())
            form.save()
            usuario.save()
            return HttpResponseRedirect(self.get_success_url())

        def form_invalid(self, form):
            """
            Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
            durante la creación del form.
            :param form:
            :return: Reload del form con errores.
            """
            context = {
                'form': form
            }
            print(form.errors)
            return super(AgregarUsuariosRolView, self).render_to_response(self.get_context_data(**context), )


class AgregarUsuariosRolView(LoginRequiredMixin, CreateView):
    model = RolProyectoUsuarios
    template_name = 'proyectos/roles/agregar_usuarios_rol.html'
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Proyecto, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todas las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(AgregarUsuariosRolView, self).get_context_data(**kwargs)
        proyecto = get_object_or_404(Proyecto, pk=self.kwargs["pk"])
        context["roles"] = RolProyecto.objects.all()
        context["miembros"] = proyecto.equipo.usuarios.all()
        context["proyecto"] = proyecto
        return context

    def get_success_url(self):
        """
        Override de la función original

        Se implementa un template personalizado en caso de que el proyecto fue creado/actualizado exitosamente
        :return: redireccionamiento hacia la página de éxito
        """
        return reverse('home')

    def form_valid(self, form):
        """
        En caso de que el form sea válido, este es guardado y se crea el objeto en la base de datos.
        :param form:
        :return: Redireccionamiento a la página de éxito
        """

        usuario = form.cleaned_data["usuarios"]
        RolProyectoUsuarios.objects.filter(usuarios=usuario, rol=form.cleaned_data["rol"]).delete()
        usuario.user_permissions.set(usuario.user_permissions.all() | form.cleaned_data["rol"].permisos.all())
        form.save()
        usuario.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Se recarga la página del form y se muestra en pantalla los errores que puedieron haber cometido
        durante la creación del form.
        :param form:
        :return: Reload del form con errores.
        """
        context = {
            'form': form
        }
        print(form.errors)
        return super(AgregarUsuariosRolView, self).render_to_response(self.get_context_data(**context), )


class AgregarUsuariosRolBorrar(LoginRequiredMixin, DeleteView):
    template_name = 'proyectos/roles/agregar_usuarios_rol_eliminar.html'
    success_url = "/"
    model = RolProyectoUsuarios

    def get_context_data(self, **kwargs):
        """

        Override de la función original, agregamos el query de todas las opciones para los estados.

        El contexto puede ser accedido directamente en el template de proyecto_form.html
        Agregamos al context para poder colocarlos como opciones en la lista desplegable.

        :param kwargs:
        :return: contexto
        """
        context = super(AgregarUsuariosRolBorrar, self).get_context_data(**kwargs)
        context["rol"] = self.object.rol
        context["usuario"] = self.object.usuarios
        context["object"] = self.object
        return context

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        ids = RolProyectoUsuarios.objects.filter(usuarios=self.object.usuarios).exclude(pk=self.object.id).values_list(
            'rol', flat=True)
        roles = RolProyecto.objects.filter(id__in=ids)
        permissions = []
        for rol in roles:
            permisos = rol.permisos.all()
            for permiso in permisos:
                permissions.append(permiso)
        usuario = self.object.usuarios
        usuario.user_permissions.set(permissions)
        usuario.save()
        return super(AgregarUsuariosRolBorrar, self).delete(*args, **kwargs)