from django.db import models
from django.core.validators import MinValueValidator


class Bolim(models.Model):
    nom = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

class Mahsulot(models.Model):
    nom = models.CharField(max_length=255)
    narx1 = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    narx2 = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    rasm = models.ImageField(upload_to='mahsulotlar/', blank=True, null=True)
    bolim = models.ForeignKey(Bolim, on_delete=models.CASCADE, related_name='mahsulotlar')
    miqdor = models.PositiveIntegerField(default=0)
    olchov = models.CharField(max_length=10,
        choices=[('dona', 'Dona'), ('kg', 'KG'), ('ta', 'Ta')],
        default='dona')
    brend = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

class Kirim(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    miqdor = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    sana = models.DateField(auto_now_add=True)
    narx = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.sana}: {self.mahsulot.nom} - {self.miqdor} {self.mahsulot.olchov}"

    class Meta:
        verbose_name = "Kirim"
        verbose_name_plural = "Kirimlar"

class Xarajat(models.Model):
    miqdor = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    izoh = models.TextField()
    sana = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.sana}: {self.miqdor} so'm - {self.izoh}"

    class Meta:
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar"

class Sotuv(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    miqdor = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    jami_summa = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    sana = models.DateField(auto_now_add=True)
    izoh = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.sana}: {self.mahsulot.nom} - {self.miqdor} {self.mahsulot.olchov}"

    class Meta:
        verbose_name = "Sotuv"
        verbose_name_plural = "Sotuvlar"