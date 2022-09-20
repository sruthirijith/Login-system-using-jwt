
import uvicorn
from fastapi import FastAPI , Body , Depends
import models
from models import PostSchema
from models import PostSchema, UserSchema, UserLoginSchema
from jwt_handler import signJWT
from jwt_bearer import jwtBearer



posts = [
    {
        "id" :1,
        "title" : "penguine",
        "text":" ggdeguhduwehcfhehchehvhv"
    },
    {
       "id" :2,
        "title" : "tigers",
        "text":" ggdeguhduwehcfhehchehvhv" 
    },
    {
        "id" :3,
        "title" : "koals",
        "text":" ggdeguhduwehcfhehchehvhv"
    }
]

users = []

app = FastAPI()


#1 get for testing
@app.get("/",tags=["test"])
def greet():
    return{"Hello":"world"}


#2 get posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return{"data": posts}


#3 get single post {id}
@app.get("/post/{id}", tags=["posts"])
def get_one_post(id: int):
    if id > len(posts):
        return{
            "error":"post with this id doesnt exist"
        }
    for post in posts:
        if post["id"] == id:
            return{
                "data":post            }     


#4 post a blog post [A handler for creating a post]
@app.post("/posts",dependencies=[Depends(jwtBearer())] , tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return{
        "info":"Post Added"
    }     

#5 user signup [create a new user]
@app.post("/user/signup", tags=["user"])
def user_signup(user : UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data:  UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False

@app.post("/users/login", tags=["user"])
def user_login(user: UserLoginSchema = Body()):
    if check_user(user):
        return signJWT(user.email)
    else:
        return{
            "error":"Invalid login details"
        }    