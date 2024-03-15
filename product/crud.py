from sqlalchemy.orm import Session
from . import models, BaseModels
from datetime import datetime


def add_new_item(db: Session, user_name: str, item:BaseModels.Item):
    resp = db.query(models.Item).filter_by(item_name=item.item_name).first()
    if not resp:
        add_item = models.Item( item_name=item.item_name, 
                                item_description=item.item_description,
                                item_quantity=item.item_quantity,
                                item_price=item.item_price, 
                                category=item.category, 
                                manufacture_date= item.manufacture_date,
                                expiry_date= item.expiry_date, 
                                units=item.units,
                                last_updated_by=user_name,
                                discount=item.discount)
        db.add(add_item)
        db.commit()
        db.refresh(add_item)
        return False
    return True


def get_all_items(db: Session, user_name: str, category: str, p_min: float, p_max: float):
    query_data = filter_data(db, user_name, category, p_min, p_max)
    if query_data:
        for i in query_data:
            i.before_discount = i.item_price
            price = calculate_discounted_price(i.item_price,i.discount)
            i.after_discount = price
        return query_data

def get_all_offered_items(db: Session, user_name: str, category: str, p_min: float, p_max: float):
    query_data = filter_data_offer(db, user_name, category, p_min, p_max)
    if query_data:
        for i in query_data:
            i.before_discount = i.item_price
            price = calculate_discounted_price(i.item_price,i.discount)
            i.after_discount = price
        return query_data

def calculate_discounted_price(original_price, discount_percentage):
    discounted_price = original_price - (original_price * (discount_percentage / 100))
    return discounted_price



def add_new_category(db: Session, user_name: str, category_details:BaseModels.Category):
    existing_category = db.query(models.Category).filter_by(category_name=category_details.category_name).first()
    if existing_category:
        return existing_category, True
    add_category = models.Category( category_name= category_details.category_name,
                                    updated_by=user_name )
    db.add(add_category)
    db.commit()
    db.refresh(add_category)
    return add_category, False

def get_all_category(db: Session, user_name: str):
    return db.query(models.Category).all()
    # return db.query(models.Item.category).distinct().all()


def delate_item(db: Session, user_name: str, item_name: str):
    resp = db.query(models.Item).filter(models.Item.item_name == item_name).first()
    if not resp:
        return False
    db.query(models.Item).filter(models.Item.item_name == item_name).delete()
    db.commit()
    return resp



def filter_data_offer(db, user_name, category, p_min, p_max):
    if category == "None" and p_min == 0.0 and p_max == 0.0:
        query_data = db.query(models.Item).filter(models.Item.discount != 0).all()
    elif category != "None" and p_min == 0.0 and p_max == 0.0:
        query_data = db.query(models.Item).filter(models.Item.discount != 0, models.Item.category == category).all()

    elif category != "None" and p_min != 0.0 and p_max != 0.0:
        query_data = db.query(models.Item).filter(models.Item.discount != 0, models.Item.category == category, models.Item.item_price.between(p_min, p_max)).all()
    elif category == "None" and p_min != 0.0 and p_max != 0.0:
        query_data = db.query(models.Item).filter(models.Item.discount != 0, models.Item.item_price.between(p_min, p_max)).all()

    elif p_min == 0.0 and p_max != 0.0 and category != "None":
        query_data = db.query(models.Item).filter(models.Item.discount != 0, models.Item.category == category, models.Item.item_price <= p_max).all()
    elif p_min == 0.0 and p_max != 0.0 and category == "None":
        query_data = db.query(models.Item).filter(models.Item.discount != 0, models.Item.item_price <= p_max).all()

    elif p_min != 0.0 and p_max == 0.0 and category != "None":
        query_data = db.query(models.Item).filter(models.Item.discount != 0, models.Item.category == category, models.Item.item_price >= p_min).all()
    elif p_min != 0.0 and p_max == 0.0 and category == "None":
        query_data = db.query(models.Item).filter(models.Item.discount != 0, models.Item.item_price >= p_min).all()
    
    return query_data


def filter_data(db, user_name, category, p_min, p_max):
    if category == "None" and p_min == 0.0 and p_max == 0.0:
        query_data = db.query(models.Item).all()
    elif category != "None" and p_min == 0.0 and p_max == 0.0:
        query_data = db.query(models.Item).filter(models.Item.category == category).all()

    elif category != "None" and p_min != 0.0 and p_max != 0.0:
        query_data = db.query(models.Item).filter(models.Item.category == category, models.Item.item_price.between(p_min, p_max)).all()
    elif category == "None" and p_min != 0.0 and p_max != 0.0:
        query_data = db.query(models.Item).filter(models.Item.item_price.between(p_min, p_max)).all()

    elif p_min == 0.0 and p_max != 0.0 and category != "None":
        query_data = db.query(models.Item).filter(models.Item.category == category, models.Item.item_price <= p_max).all()
    elif p_min == 0.0 and p_max != 0.0 and category == "None":
        query_data = db.query(models.Item).filter(models.Item.item_price <= p_max).all()

    elif p_min != 0.0 and p_max == 0.0 and category != "None":
        query_data = db.query(models.Item).filter(models.Item.category == category, models.Item.item_price >= p_min).all()
    elif p_min != 0.0 and p_max == 0.0 and category == "None":
        query_data = db.query(models.Item).filter(models.Item.item_price >= p_min).all()
    
    return query_data

