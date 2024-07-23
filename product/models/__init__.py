from product.models.product import *
from product.models.category import *
from product.models.rating import *
from product.models.genre import *
from simple_history import register

register(Category)
register(Product)
register(Genre)
register(Rating)
