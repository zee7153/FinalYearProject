from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class DateTimeAbstract(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class myuser(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField(unique=True)
    address = models.CharField(max_length=500)

    def __str__(self):
        template = '{0.name} {0.address}'
        return template.format(self)

class Order(DateTimeAbstract):
    user = models.ForeignKey(myuser, on_delete=models.CASCADE)
    order_id = models.IntegerField()
    order_status = models.CharField(max_length=100)

    def __str__(self):
        return self.order_status

class Company(models.Model):
    """
    Simply contains company details, referenced by Placement model
    """

    company_name = models.CharField(max_length=255,default='Add Company Name')
    company_address = models.CharField(max_length=255,default='Add Company address')
    company_description = models.TextField(default="There is currently no description available for this company.")
    # company_Price = models.DecimalField(max_digits=5,decimal_places=2)
    # company_Picture= models.URLField(blank=False,null=False)
    company_created = models.DateTimeField(auto_now_add=True)
    company_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class Placement(models.Model):
    """
    A placement allows investors to bid on company capital raise
    """

    placement_title = models.CharField(max_length=255,default='Add Bid-item Title')
    placement_slug = models.SlugField()
    placement_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price=models.IntegerField(default=0)
    total_pieces=models.IntegerField(default=0)
    picture=models.ImageField( upload_to="static", height_field=None, width_field=None, max_length=None,default='/home/zeeshan/My-FYP/static/ap1.jpeg')
    #pic = models.ImageField(upload_to='blah', default='path/to/my/default/image.jpg')

    #placement_created = models.DateTimeField(auto_now_add=True)
    #placement_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.placement_title


class Bid(models.Model):
    """
    The bid, synonmous with 'order'
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_status = models.BooleanField(default=False)

    bid_created = models.DateTimeField(auto_now_add=True)
    bid_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} -{}'.format(self.user, self.bid_status)


class PlacementBid(models.Model):
    """
    The junction table for placement and bid models/tables. Contains every instance of a bid for a placement
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE)
    bid  = models.ForeignKey(Bid, on_delete=models.CASCADE)
    offer = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    confirmed = models.BooleanField(default=False)
    
    placementbid_created = models.DateTimeField(auto_now_add=True)
    placementbid_modified = models.DateTimeField(auto_now=True)

    class Meta: 
        ordering = ['-placementbid_modified'] 

    def __str__(self):
        return '{} - {} - {}'.format(self.shares, self.offer, self.user)