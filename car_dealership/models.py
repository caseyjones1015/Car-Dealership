from django.db import models


class CarBrand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.IntegerField()
    price = models.CharField(max_length=100, null=True, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    grade = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    optional = models.TextField(null=True, blank=True)
    available = models.BooleanField(default=True)
    seater = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.car_model.name + str(self.year)


class CarImage(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"Image for Car {self.car.id}"


class AdditionalCarImage(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    additional_image = models.ImageField(upload_to='additional_car_images/')

    def __str__(self):
        return f"Additional Image for Car {self.car.id}"


class FinancialDetails(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    legal_documents = models.ManyToManyField('LegalDocument', related_name='financial_details', blank=True)

    buy_co = models.CharField(max_length=100, null=True, blank=True)
    buy_amount = models.CharField(max_length=100, null=True, blank=True)
    buy_additional = models.CharField(max_length=100, null=True, blank=True)
    buy_total = models.CharField(max_length=100, null=True, blank=True)

    repair_co = models.CharField(max_length=100, null=True, blank=True)
    repair_amount = models.CharField(max_length=100, null=True, blank=True)
    repair_additional = models.CharField(max_length=100, null=True, blank=True)
    repair_total = models.CharField(max_length=100, null=True, blank=True)

    sold_co = models.CharField(max_length=100, null=True, blank=True)
    sold_amount = models.CharField(max_length=100, null=True, blank=True)
    sold_additional = models.CharField(max_length=100, null=True, blank=True)
    sold_total = models.CharField(max_length=100, null=True, blank=True)

    brokage_co = models.CharField(max_length=100, null=True, blank=True)
    brokage_amount = models.CharField(max_length=100, null=True, blank=True)
    brokage_additional = models.CharField(max_length=100, null=True, blank=True)
    brokage_total = models.CharField(max_length=100, null=True, blank=True)

    profit = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Financial details for {self.car}"


class LegalDocument(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    legal_document = models.ImageField(upload_to='legal_documents/')

    def __str__(self):
        return f"Legal Document for car {self.car.id}"
