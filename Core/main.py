from fastapi import FastAPI, HTTPException,Query,status,Path,Form,Body,File,UploadFile
from typing import Optional,Annotated
from fastapi.responses import JSONResponse
from typing import List
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔥 Application startup from lifespan")
    yield
    print("🛑 Application shutdown from lifespan")

app = FastAPI(lifespan=lifespan)

names_db = [
    {
        "id": 1,
        "name": "ali"
    },
    {
        "id": 2,
        "name": "maryam"
    },
    {
        "id": 3,
        "name": "arousha"
    },
    {
        "id": 4,
        "name": "ali"
    },
    {
        "id": 5,
        "name": "ali"
    }
]



@app.get("/")
def hello_world():
    print("/////")
    return JSONResponse(content={"message": "Hello World"},status_code=status.HTTP_200_OK)

@app.get("/names")
def retrive_names_list(q:Annotated[str|None,Query(alias="search",max_length=5,description="You can search any user in DB",example="ali")]=None):
    if q:
        return [item for item in names_db if item["name"]==q ]
    return names_db


@app.get("/items")
def get_items(
    q: Annotated[Optional[str], Query(alias="search", max_length=50, description="Search term", example="example")],
    page: Annotated[int, Query(ge=1, le=100, description="Page number")]=1,
    sort_by: Annotated[str|None, Query(regex="^[a-zA-Z0-9_]+$", description="Sort field")] = None):
    """
    Retrieve a list of items with optional search, pagination, and sorting.
    """
    # Your item retrieval logic here
    return {"q": q, "page": page, "sort_by": sort_by}

# @app.get("/names")
# def retrive_names_list(q:Optional[str]=None):
#     if q:
#         return [item for item in names_db if item["name"]==q ]
#     return names_db


# @app.get("/names")
# def retrive_names_list():
#     return names_db

@app.get("/names/{item_id}")
def retrive_name_id(item_id : int = Path(alias="object id",title="object id")):
    for item in names_db:
        if item['id'] == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found") 





@app.post("/names",status_code=status.HTTP_201_CREATED)
def add_new_user(name:str = Form()):
    id = len(names_db)+1
    new_item ={"id":id,"name":name}
    names_db.append(new_item)
    return new_item

@app.post("/upload")
def upload_image(file:bytes = File()):
    return JSONResponse(content={"file_size": len(file)},status_code=status.HTTP_201_CREATED)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    # اطلاعات فایل را می‌خوانیم
    content_file = await file.read()
    return JSONResponse(content={"filename": file.filename, "content_type": file.content_type, "file_size": len(content_file)},status_code=status.HTTP_201_CREATED)

@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile]):
    return [
        {"filename": file.filename, "content_type": file.content_type} 
        for file in files
    ]







@app.put("/names/{item_id}",status_code=status.HTTP_205_RESET_CONTENT)
def change_name_id(item_id : int,name :str = Body(default=None,embed=True),age:int = Body()):
    for item in names_db:
        if item['id'] == item_id:
            pre_name = item['name']
            item['name'] = name
            return {"message": f"{pre_name} with ID {item_id} updated successfully and its name has changed to {name}"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found") 




@app.delete("/names/{item_id}")
def delete_name_id(item_id : int):
    for item in names_db:
        if item['id'] == item_id:
            names_db.remove(item)
            return JSONResponse(content={"message": f"User with ID {item_id} deleted successfully"},status_code=status.HTTP_202_ACCEPTED)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")