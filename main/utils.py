
def get_pet_name(pet_name):
    if pet_name == 'Кошки':
        return 'для кошек'
    if pet_name == 'Собаки':
        return "для собак"
    if pet_name == 'Грызуны':
        return "для грызунов"
    if pet_name == 'Птицы':
        return "для птиц"
    if pet_name == 'Рыбки':
        return "для рыбок"


def get_total_weight(request):
    price = request.GET['price']
    weight = request.GET['weight']
    context = {
        'some_weight': weight,
        'some_price': price,
        }
    return context