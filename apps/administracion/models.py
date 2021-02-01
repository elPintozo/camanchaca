import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from itertools import cycle
from apps.docencia.models import Sucursal, Curso
from apps.docencia.utils import nacionalidades
# Create your models here.

def validar_rut(rut):
    """
    Función que valida la veracidad del rut del Participante
    :param rut: puede ser ingresado con puntos y guión o sin uno de ellos
    :return: [False]: error en la interfaz | [True] da el visto bueno para la creación
    """
    rut = rut.upper()
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    aux = rut[:-1]
    dv = rut[-1:]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    if str(res) == dv:
        pass
    elif dv == "K" and res == 10:
        pass
    else:
        raise ValidationError(_('%(value)s No es un rut válido'), params={'value': rut}, )

class Empresa(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    empresa_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

class Area(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    area_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.area_id

class Clase(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    clase_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.clase_id

class Sindicato(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    sindicato_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sindicato_id

class Contrato(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    contrato_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contrato_id

class Cargo(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    cargo_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cargo_id

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    categoria_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categoria_id

class CentroCosto(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    centro_costo_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.centro_costo_id

class Horario(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    horario_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.horario_id

class Ine(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    ine_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ine_id

class Educacion(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    educacion_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    #sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.educacion_id

class Trabajador(models.Model):
    ESTADO = (
        ('A', 'Activo'),
        ('S', 'Suspendido'),
    )
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )

    nombres = models.CharField(max_length=255, null=False, default='')
    rut = models.CharField(max_length=12, null=False, validators=[validar_rut])
    estado = models.CharField(max_length=1, null=False, choices=ESTADO)
    sexo = models.CharField(max_length=1, choices=SEXO, default='1')
    fecha_nacimiento = models.DateField()
    email = models.EmailField(null=False)
    fecha_ingreso = models.DateField()
    fecha_termino = models.DateField()
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, null=True)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, null=True)
    sindicato = models.ForeignKey(Sindicato, on_delete=models.CASCADE, null=True)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, null=True)
    biometrico = models.CharField(max_length=255, null=False, default='')
    ine = models.ForeignKey(Ine, on_delete=models.CASCADE, null=True)
    educacion = models.ForeignKey(Educacion, on_delete=models.CASCADE, null=True)
    nacionalidad = models.CharField(max_length=10, default='46', choices=nacionalidades)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True)
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.CASCADE, null=True)
    trabajador_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rut

class CursoTrabajador(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['curso', 'trabajador']]

def set_cargo_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Cargo
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un cargo_id
    if not instance.cargo_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.cargo_id = str(uuid.uuid4())

def set_categoria_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Categoria
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un categoria_id
    if not instance.categoria_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.categoria_id = str(uuid.uuid4())

def set_centro_costo_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object CentroCosto
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un categoria_id
    if not instance.centro_costo_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.centro_costo_id = str(uuid.uuid4())

def set_empresa_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Empresa
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un empresa_id
    if not instance.empresa_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.empresa_id = str(uuid.uuid4())

def set_trabajador_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Trabajador
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un trabajador_id
    if not instance.trabajador_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.trabajador_id = str(uuid.uuid4())

def set_area_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Area
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un area_id
    if not instance.area_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.area_id = str(uuid.uuid4())

def set_contrato_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Contrato
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un contrato_id
    if not instance.contrato_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.contrato_id = str(uuid.uuid4())

def set_clase_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Clase
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un clase_id
    if not instance.clase_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.clase_id = str(uuid.uuid4())

def set_sindicato_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Sindicato
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un sindicato_id
    if not instance.sindicato_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.sindicato_id = str(uuid.uuid4())

def set_ine_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object INE
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un ine_id
    if not instance.ine_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.ine_id = str(uuid.uuid4())

def set_educacion_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Educacion
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un educacion_id
    if not instance.educacion_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.educacion_id = str(uuid.uuid4())

#Asigno al pre_save la función que actuará antes de guardar, e indico a que class corresponde
pre_save.connect(set_cargo_id, sender=Cargo)
pre_save.connect(set_categoria_id, sender=Categoria)
pre_save.connect(set_centro_costo_id, sender=CentroCosto)
pre_save.connect(set_empresa_id, sender=Empresa)
pre_save.connect(set_trabajador_id, sender=Trabajador)
pre_save.connect(set_area_id, sender=Area)
pre_save.connect(set_contrato_id, sender=Contrato)
pre_save.connect(set_clase_id, sender=Clase)
pre_save.connect(set_sindicato_id, sender=Sindicato)
pre_save.connect(set_ine_id, sender=Ine)
pre_save.connect(set_educacion_id, sender=Educacion)