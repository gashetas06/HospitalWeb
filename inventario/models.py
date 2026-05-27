from django.db import models

class Categoriainventario(models.Model):
    idcategoria = models.AutoField(db_column='idCategoria', primary_key=True)
    nombre = models.CharField(unique=True, max_length=100, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'CategoriaInventario'

class Inventario(models.Model):
    idinventario = models.AutoField(db_column='idInventario', primary_key=True)
    idcategoria = models.ForeignKey(Categoriainventario, models.DO_NOTHING, db_column='idCategoria')
    nombreproducto = models.CharField(db_column='nombreProducto', max_length=150, db_collation='Modern_Spanish_CI_AS')
    unidadmedida = models.CharField(db_column='unidadMedida', max_length=30, db_collation='Modern_Spanish_CI_AS')
    cantidaddisponible = models.IntegerField(db_column='cantidadDisponible')
    nivelcritico = models.IntegerField(db_column='nivelCritico')
    preciounitario = models.DecimalField(db_column='precioUnitario', max_digits=10, decimal_places=2, blank=True, null=True)
    proveedor = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    fechaultimaentrada = models.DateTimeField(db_column='fechaUltimaEntrada', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Inventario'

    def __str__(self):
        return self.nombreproducto