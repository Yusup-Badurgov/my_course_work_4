# Константы:
# PWD_HASH_SALT -"соль" для хеширования
# PWD_HASH_ITERATIONS - число проходов при кодировании
# ALGORYTHM  - алгоритм
# SECRET - секретная строка ( Ой! :) )
# POSTS_PER_PAGE - число элементов на странице при пагинации

PWD_HASH_SALT = b'secret here'
PWD_HASH_ITERATIONS = 100_000
ALGORYTHM = 'HS256'
SECRET = 's3cR$eT'
POSTS_PER_PAGE = 12
