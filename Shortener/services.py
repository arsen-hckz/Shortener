from django.db import transaction
from django.db.utils import IntegrityError
from .models import ShortLink
from .utils import base62_encode
import uuid


class Code_Taken(Exception):
    pass


def create_short_link(*,long_url:str,custome_code:str| None = None) -> ShortLink:
    if custome_code:
            try:
                with transaction.atomic():
                    return ShortLink.objects.create(
                        code = custome_code,
                        long_url = long_url,
                        is_active = True
                          )
            except IntegrityError:
                raise IntegrityError
        
    link = ShortLink.objects.create(
                code = "tmp",
                long_url = long_url,
                is_active = True
     )
    temp_code = "tmp_" + uuid.uuid4().hex
    link.code = base62_encode(link.id)
    link.save(update_fields=["code"])
    return link
