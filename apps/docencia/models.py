import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

class Relator(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    relator_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

class Sucursal(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    create_at = models.DateTimeField(auto_now_add=True)
    sucursal_id = models.CharField(max_length=100, null=False, blank=False, unique=True)


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

class Modalidad(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

class Capa(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

class Competencia(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    create_at = models.DateTimeField(auto_now_add=True)

class Planificacion(models.Model):
    fecha_planificacion = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.CASCADE, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True)

class Curso(models.Model):
    ORIGEN = (
        ('W', 'Web'),
        ('T', 'Tablet'),
        ('E', 'Externo'),#cursos importados en excel
    )
    ESTADO = (
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('E', 'Eliminado'),
    )
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    tema = models.CharField(max_length=255, null=False, default='')
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE)
    capa  = models.ForeignKey(Capa, on_delete=models.CASCADE)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100, null=False, default='')
    hora = models.IntegerField(default=1)
    contenido = models.CharField(max_length=255, null=False, default='')
    planificacion = models.ForeignKey(Planificacion, on_delete=models.CASCADE, null=True)
    origen_creacion = models.CharField(max_length=1, choices=ORIGEN, default='W')
    estado = models.CharField(max_length=1, choices=ESTADO, default='A')
    # documentos # pendiente
    create_at = models.DateTimeField(auto_now_add=True)
    curso_id = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.cart_id

class CursoRelator(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    relator = models.ForeignKey(Relator, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['curso', 'relator']]

def set_curso_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Curso
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un curso_id
    if not instance.curso_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.curso_id = str(uuid.uuid4())

def set_sucursal_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Sucursal
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un sucursal_id
    if not instance.sucursal_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.sucursal_id = str(uuid.uuid4())

def set_relator_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Relator
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un relator_id
    if not instance.relator_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.relator_id = str(uuid.uuid4())

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

#Asigno al pre_save la función que actuará antes de guardar, e indico a que class corresponde
pre_save.connect(set_curso_id, sender=Curso)
pre_save.connect(set_sucursal_id, sender=Sucursal)
pre_save.connect(set_relator_id, sender=Relator)
pre_save.connect(set_cargo_id, sender=Cargo)
pre_save.connect(set_categoria_id, sender=Categoria)
pre_save.connect(set_centro_costo_id, sender=CentroCosto)