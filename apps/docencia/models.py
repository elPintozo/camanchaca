import uuid
from django.db import models
from django.db.models.signals import pre_save

# Create your models here.
class Relator(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    create_at = models.DateTimeField(auto_now_add=True)
    relator_id = models.CharField(max_length=100, null=False, blank=False, unique=True)

class Sucursal(models.Model):
    nombre = models.CharField(max_length=255, null=False, default='')
    create_at = models.DateTimeField(auto_now_add=True)
    sucursal_id = models.CharField(max_length=100, null=False, blank=False, unique=True)

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

class Curso(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    tema = models.CharField(max_length=255, null=False, default='')
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE)
    capa  = models.ForeignKey(Capa, on_delete=models.CASCADE)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100, null=False, default='')
    hora = models.IntegerField(default=1)
    contenido = models.CharField(max_length=255, null=False, default='')
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

#Asigno al pre_save la función que actuará antes de guardar, e indico a que class corresponde
pre_save.connect(set_curso_id, sender=Curso)
pre_save.connect(set_sucursal_id, sender=Sucursal)
pre_save.connect(set_relator_id, sender=Relator)