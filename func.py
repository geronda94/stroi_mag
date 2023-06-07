from pg import products
from flask import session



def return_next(lst):
    if len(lst) >1:
        result = lst[-2]
        if 'static' not in result and 'favico' not in result:
            return result
        else: return '/'
    else:
        return '/'
    

def coll_to_int(coll):
    result = ''
    for i in coll:
        if i.isdigit():
            result = result+i
        else:
            continue
    if result != None and result != '':
        return int(result)
    else:
        return 1



def bag_construct(cart:dict):  
    total_price = 0
    total_weight = 0
    prod_id = [x[0] for x in cart.items()]
    product_list = products.in_cart(prod_id)
    loaders__calc = dict()



    bag_refactored= []
    for i in product_list:
        
        for key, value in cart.items():
            product_id = int(i.get('product_id'))
            cart_id = int(key)
            if product_id ==cart_id:
                sale = 0
                price = int(i.get('price'))
                price2 = i.get('price2')
                price3 = i.get('price3')
                condition1 = i.get('sale_for1')
                condition2 = i.get('sale_for2')
                coll = int(value)
                weight = float(i.get('weight'))
                
                sale = int(price)

                if (condition2 and price3):
                    if coll >= int(condition2):
                        sale = int(price3)
                    elif (condition1 and price2):
                        if coll >= int(condition1):
                            sale = int(price2)

                
                    

                total = int(sale)*int(coll)
                total_price+=total
                sum_weight = int(weight*int(coll))
                total_weight += sum_weight

                if sale == price:
                    sale = '-'

                bag_refactored.append({
                    'product_id':i.get('product_id'),
                    'product_name':i.get('product_name'),
                    'product_ava':i.get('ava_link'),
                    'coll':coll,
                    'weight':sum_weight,
                    'price':price,
                    'sale':sale,
                    'total':total,
                    'link':i.get('link')
                })

                if loaders__calc.get(weight):
                    loaders__calc[weight] += int(sum_weight/weight)
                else:  
                    loaders__calc[weight] = int(sum_weight/weight)
            else:
                continue
        
    if not session.get('delivery'):
        session['delivery'] = dict()

    session['bag_refactored'] = cart
    session['loaders_calc'] = loaders__calc
    session['delivery']['total_weight'] = total_weight
    session['delivery']['total_price'] = total_price

    return [bag_refactored, total_price, total_weight]