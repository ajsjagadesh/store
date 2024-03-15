from fastapi import APIRouter, FastAPI, HTTPException, Header, Depends, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated

from .BaseModels import Item, Category, Offers, add_item
from .process import get_token

from . import crud

from connect import SessionLocal, engine
from sqlalchemy.orm import Session
from auth import Token, User, authenticate_user, create_access_token, get_current_active_user, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES





# Secret key to sign JWT token
# SECRET_KEY = "ajs-001-AB-001-1998-1997"


product = FastAPI()
router1 = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



        

@product.post("/item", response_model=add_item)
def add_new_item(current_user: Annotated[User, Depends(get_current_active_user)],   item_name: str = Form(...), item_description: str = Form(...),
                                                                                    item_price: float = Form(...), category: str = Form(...),
                                                                                    manufacture_date: datetime = Form(...),  expiry_date: datetime = Form(...),
                                                                                    units: int = Form(...), discount: float = Form(...),
                                                                                    item_quantity: str = Form(...), 
                                                                                    db: Session = Depends(get_db)):
    item = Item(item_name=item_name, item_description=item_description, 
                item_price=item_price, category=category,
                manufacture_date=manufacture_date, expiry_date=expiry_date,
                units=units, discount=discount, item_quantity=item_quantity)
    print(item)
    resp = crud.add_new_item(db, current_user.user_name, item)
    if resp:
        return {
            "message": "Item already in list, Trying to add duplicate item.",
            "item_name": item.item_name
        }
    return {
        "message": "Item added successfully",
        "item_name": item.item_name
    }
    

@product.get("/item")
def get_all_items(current_user: Annotated[User, Depends(get_current_active_user)], only_offer: bool = False, category: str = "None", p_min: float = 0.0, p_max: float = 0.0, db: Session = Depends(get_db)):
    if only_offer:
        offered_items = crud.get_all_offered_items(db, current_user.user_name, category, p_min, p_max)
        if offered_items:
            return {
                "items_count" : len(offered_items),
                "items_details" : [item.__dict__ for item in offered_items]
            }
        return {
                "items_count" : 0,
                "items_details" : ["No items found"]
            }

    all_items = crud.get_all_items(db, current_user.user_name, category, p_min, p_max)
    return {
        "items_count" : len(all_items),
        "items_details" : [item.__dict__ for item in all_items]
    }


@product.delete("/item")
def delete_item(current_user: Annotated[User, Depends(get_current_active_user)], item_name: str, db: Session = Depends(get_db)):
    resp = crud.delate_item(db, current_user.user_name, item_name)
    return {
        "message": "Item deleted successfully",
        "deleted_item": resp
        }


@product.post("/category")
def add_category(current_user: Annotated[User, Depends(get_current_active_user)], category_details : Category, db: Session = Depends(get_db)):
    resp, existing_category = crud.add_new_category(db, current_user.user_name, category_details)
    if existing_category:
        return {"message" : "Category already exist",
                "category_details" : resp.__dict__}
    return {
        "message": " Category added successfully",
        "category_details": resp.__dict__
    }
    

@product.get("/category")
def get_category(current_user: Annotated[User, Depends(get_current_active_user)] , db: Session = Depends(get_db)):
    all_category = crud.get_all_category(db, current_user.user_name)
    return {
        "category_count": len(all_category),
        "category_details": [category.__dict__ for category in all_category]
    }
   




from fastapi import FastAPI, Request, HTTPException, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from fastapi.responses import RedirectResponse
from typing import Optional  

# app = FastAPI()
templates = Jinja2Templates(directory="templates")

@product.get("/login_test", response_class=HTMLResponse)
async def test(request: Request):
    try:
        return templates.TemplateResponse("login_test.html", {"request": request})
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@product.get("/test", response_class=HTMLResponse)
async def test(request: Request, access_token: Optional[str] = Cookie(None)):
    print(access_token)
    if not access_token:
        return RedirectResponse(url="/v2/login_test")
     # access_token retrieved from headers
    # access_token = request.headers.get("Authorization")
    # print("Access Token from Headers:", access_token)
    try:
        return templates.TemplateResponse("test.html", {"request": request, "Name": "A Jagadish", "Test":1000})
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


product.include_router(router1)









# product = FastAPI()
# router1 = APIRouter()



# @product.post("/token")
# async def login_for_access_token( form_data: Annotated[OAuth2PasswordRequestForm, Depends()] ) -> Token:
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")


# @product.get("/users/me/", response_model=User)
# async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return current_user


# @product.get("/users/me/items/")
# async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return [{"item_id": "Foo", "owner": current_user.username}]

# product.include_router(router1)