from django.dispatch import receiver
from django.db.models.signals import post_save
from system.models import Inscripciones, Notificaciones
@receiver(post_save, sender = Inscripciones)
def send_notification(sender, instance, **kwargs):
    Notificaciones.objects.create(
        texto="Se ha inscrito al curso",
        inscripciones=instance,
        nombre_noti=instance.nombre_ins,
        apellidos_noti=instance.apellidos_ins,
        curso=instance.curso_id
        # Asigna el curso asociado a la inscripción
    )
    