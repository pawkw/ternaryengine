from ternaryengine.tryte import *
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

t1 = 'zzzzzzpnn'
t2 = 'zzzzzzpzn'

print(tAdd(t1, t2))