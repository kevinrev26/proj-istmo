product_list = [
        {
            'id': 1,
            'name' : 'The Legend of Zelda: Echoes of wisdom',
            'price' : '45',
            'rating' : 5,
            'image' : 'https://ae-pic-a1.aliexpress-media.com/kf/S4d6a08820b8b4ba89fc364423f49301dM.jpg_960x960q75.jpg',
            'description' : 'Lorem ipsum',
        },
        {
            'id': 2,
            'name' : 'Dumb ways to die',
            'price' : '20.21',
            'rating' : 4,
            'image' : 'https://ae-pic-a1.aliexpress-media.com/kf/S324a5ecb269344828a7658f5893477e10.jpg_960x960q75.jpg',
            'description' : 'Lorem ipsum',
        },
        {
            'id': 3,
            'name' : 'Mildfred pain',
            'price' : '2.63',
            'rating' : 3.5,
            'image' : 'https://ae-pic-a1.aliexpress-media.com/kf/Se6cd32489eaf439995500907e3eca937g.jpg_960x960q75.jpg',
            'description' : 'Lorem ipsum',
        },
        {
            'id': 4,
            'name' : 'League of legends 50 pcs of stickers',
            'price' : '2.12',
            'rating' : 4.9,
            'image' : 'https://ae-pic-a1.aliexpress-media.com/kf/S79bfc7c08da94721839f07c01530b015S.jpg_960x960q75.jpg',
            'description' : 'Lorem ipsum',
        },
        {
            'id': 5,
            'name' : 'Spy x Family anime figure',
            'price' : '9.09',
            'rating' : 4.8,
            'image' : 'https://ae-pic-a1.aliexpress-media.com/kf/Sba64703d8f9240a6afed0ca48ea3b35bx.jpg_960x960q75.jpg',
            'description' : 'Lorem ipsum',
        },
        {
            'id' : 6,
            'name' : 'Xiomi Deli Metal Rollerball',
            'price' : '1.92',
            'rating' : 3,
            'image' : 'https://ae-pic-a1.aliexpress-media.com/kf/H4828a5c5d29445c48fbfa95ba70a7b6eF.jpg_960x960q75.jpg',
            'description' : 'Lorem ipsum',
        },
    ]

def get_products():
    '''This is a test and dummy list to simulate a list of products
    '''
    return product_list

def get_product_by_id(product_id):
    product = None
    for item in product_list:
        if item['id'] == product_id:
            product = item
            break

    return product