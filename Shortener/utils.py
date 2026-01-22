
#turning the url primary key to short urlcode

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def base62_encode(num:int) ->str:
    out= []
    while num:
        num, rem =divmod(num,62)
        out.append(ALPHABET[rem])
    return "".join(reversed(out))

