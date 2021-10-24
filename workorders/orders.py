import json
from collections import namedtuple
from collections import defaultdict
from types import SimpleNamespace

from data import *


files = [
    # 'basic.json',
    # 'furnace.json',
    # 'glassstock.json',
    # 'military.json',
    # 'rockstock.json',
    # 'smelting.json',
    'test.json',
]


OrderType = namedtuple('OrderType', ['job', 'item_subtype', 'item_category', 'reaction', 'material', 'material_category', 'meal_ingredients'])
# job	item_subtype	item_category	reaction	material	material_category	meal_ingredients

OrderVar = namedtuple('OrderVar', ['item_type', 'item_subtype', 'material', 'bearing', 'reaction_class', 'reaction_product', 'tool', 'flags'])
# item_type	item_subtype	material	bearing	reaction_class	reaction_product	tool	flags

class Condition(object):
    def __init__(self, condition_dict):
        # required
        self.condition = condition_dict.get('condition')
        self.value = condition_dict.get('value')

        # specifics
        self.item_type = condition_dict.get('item_type')
        self.item_subtype = condition_dict.get('item_subtype')
        self.material = condition_dict.get('material')
        self.bearing = condition_dict.get('bearing')
        self.reaction_class = condition_dict.get('reaction_class')
        self.reaction_product = condition_dict.get('reaction_product')
        self.tool = condition_dict.get('tool')
        self.flags = tuple(sorted(condition_dict.get('flags', [])))

        # not used in workorder.lua
        # self.reaction_id = condition_dict.get('reaction_id')
        # self.min_dimension = condition_dict.get('min_dimension')
        # self.contains = condition_dict.get('contains')


    def __repr__(self):
        # return str(self.__dict__)
        items = []
        self.item_type and items.append(f'item_type={self.item_type}')
        self.item_subtype and items.append(f'item_subtype={self.item_subtype}')
        self.material and items.append(f'material={self.material}')
        self.bearing and items.append(f'bearing={self.bearing}')
        self.reaction_class and items.append(f'reaction_class={self.reaction_class}')
        self.reaction_product and items.append(f'reaction_product={self.reaction_product}')
        self.tool and items.append(f'tool={self.tool}')
        self.flags and items.append(f'flags={self.flags}')

        return ' '.join([f'{self.condition}', f'{self.value}'] + items)

    @property
    def order_var(self):
        return OrderVar(self.item_type, self.item_subtype, self.material, self.bearing, self.reaction_class, self.reaction_product, self.tool, self.flags)

    def __str__(self):
        return str(self.key)


class Order(object):
    def __init__(self, order_dict):
        # job_type
        self.job = order_dict.get('job')
        self.item_subtype = order_dict.get('item_subtype')

        # reaction_name
        self.reaction = order_dict.get('reaction')

        # material_type: meal_ingredients or material
        self.material = order_dict.get('material')
        self.meal_ingredients = order_dict.get('meal_ingredients')

        # descriptive
        self.amount_left = order_dict.get('amount_left')
        self.amount_total = order_dict.get('amount_total')
        self.art = order_dict.get('art')
        self.frequency = order_dict.get('frequency')
        self.hist_figure = order_dict.get('hist_figure')
        self.id = order_dict.get('id')
        self.is_active = order_dict.get('is_active')
        self.is_validated = order_dict.get('is_validated')
        self.item_category = tuple(sorted(order_dict.get('item_category', [])))
        self.item_type = order_dict.get('item_type')
        self.material_category = tuple(sorted(order_dict.get('material_category', [])))
        self.max_workshops = order_dict.get('max_workshops')
        self.order_conditions = order_dict.get('order_conditions')
        self.workshop_id = order_dict.get('workshop_id')

        self.item_conditions = []
        for c in order_dict.get('item_conditions', []):
            self.item_conditions.append(Condition(c))

    @property
    def order_type(self):
        return OrderType(self.job, self.item_subtype, self.item_category, self.reaction, self.material, self.material_category, self.meal_ingredients)

    def orders_match(self, other):
        return self.order_type == other.order_type

    def __repr__(self):
        parts = []
        self.job and parts.append(f'{self.job}')
        self.item_subtype and parts.append(f'item_subtype={self.item_subtype}')
        self.reaction and parts.append(f'reaction={self.reaction}')
        self.material and parts.append(f'material={self.material}')
        self.meal_ingredients and parts.append(f'meal_ingredients={self.meal_ingredients}')
        self.amount_left and parts.append(f'amount_left={self.amount_left}')
        self.amount_total and parts.append(f'amount_total={self.amount_total}')
        self.art and parts.append(f'art={self.art}')
        self.frequency and parts.append(f'frequency={self.frequency}')
        self.hist_figure and parts.append(f'hist_figure={self.hist_figure}')
        self.id and parts.append(f'id={self.id}')
        self.is_active and parts.append(f'is_active={self.is_active}')
        self.is_validated and parts.append(f'is_validated={self.is_validated}')
        self.item_category and parts.append(f'item_category={self.item_category}')
        self.item_type and parts.append(f'item_type={self.item_type}')
        self.material_category and parts.append(f'material_category={self.material_category}')
        self.max_workshops and parts.append(f'max_workshops={self.max_workshops}')
        self.order_conditions and parts.append(f'order_conditions={self.order_conditions}')
        self.workshop_id and parts.append(f'workshop_id={self.workshop_id}')

        conditions = [str(c) for c in self.item_conditions]

        return ' '.join(parts) + '[' + ','.join(conditions) + ']'

    def __str__(self):
        parts = []
        # self.job and parts.append(f'{self.job}')
        # self.item_subtype and parts.append(f'item_subtype={self.item_subtype}')
        # self.item_category and parts.append(f'item_category={self.item_category}')
        # self.reaction and parts.append(f'reaction={self.reaction}')
        # self.material and parts.append(f'material={self.material}')
        # self.material_category and parts.append(f'material_category={self.material_category}')
        # self.meal_ingredients and parts.append(f'meal_ingredients={self.meal_ingredients}')
        parts.append(str(self.order_type))

        # remaining
        # self.amount_left and parts.append(f'amount_left={self.amount_left}')
        # self.amount_total and parts.append(f'amount_total={self.amount_total}')
        # self.art and parts.append(f'art={self.art}')
        # self.frequency and parts.append(f'frequency={self.frequency}')
        # self.hist_figure and parts.append(f'hist_figure={self.hist_figure}')
        # self.id and parts.append(f'id={self.id}')
        # self.is_active and parts.append(f'is_active={self.is_active}')
        # self.is_validated and parts.append(f'is_validated={self.is_validated}')
        # self.item_type and parts.append(f'item_type={self.item_type}')
        # self.max_workshops and parts.append(f'max_workshops={self.max_workshops}')
        # self.order_conditions and parts.append(f'order_conditions={self.order_conditions}')
        # self.workshop_id and parts.append(f'workshop_id={self.workshop_id}')

        conditions = ['\t' + str(c) for c in self.item_conditions]

        return ' '.join(parts) + ':\n' + '\n'.join(conditions)
        #{self.item_conditions}
        # optional
        #{self.material}
        #{self.item_subtype}
        #{self.reaction}
        #{self.material_category}
        #{self.meal_ingredients}


def read_orders():
    orders = []
    with open('second_half.json') as f:
        orders.extend(json.load(f))
    # for fn in files:
    #     with open('examples/orders/' + fn) as f:
    #         orders.extend(json.load(f))
    return orders


def tuple2row(t):
    parts = []
    for x in t:
        if isinstance(x, tuple):
            parts.append(','.join(x))
        elif not x:
            parts.append('')
        else:
            parts.append(str(x))
    return '\t'.join(parts)


def main():
    orders = read_orders()
    groups = defaultdict(int)
    done = set()
    for i, od in enumerate(orders):
        o = Order(od)
        cur = tuple2row(o.order_type)
        if o.order_type in done:
            continue
        done.add(o.order_type)
        for c in o.item_conditions:
            if c.condition == 'AtLeast':
                print('\t'.join([str(i), cur, 'INPUT', tuple2row(c.order_var)]))
            else:
                print('\t'.join([str(i), cur, 'OUTPUT', tuple2row(c.order_var)]))
        #     groups[c.key] += 1
    # for k, v in groups.items():
        # print(k, v)
    # for k, v in sorted(groups.items(), key=lambda t: len(t[1])):
    # # for k in groups.keys():
    #     if k <= 1:
    #         continue
    #     for x in v:
    #         print(x)


if __name__ == '__main__':
    main()
