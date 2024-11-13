from django.db import models

class Residente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nro_departamento = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Depto {self.nro_departamento}"

class GastoComun(models.Model):
    mes = models.CharField(max_length=20)
    año = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    estado_pago = models.BooleanField(default=False)

    def __str__(self):
        return f"Gasto {self.mes}/{self.año} - Depto {self.residente.nro_departamento} - {'Pagado' if self.estado_pago else 'Pendiente'}"