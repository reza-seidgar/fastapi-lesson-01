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

# ذخیره‌ی هزینه‌ها در حافظه
expenses: dict[int, dict] = {}

# شمارنده‌ی شناسه‌ها
next_expense_id: int = 1

@app.post("/expenses/")
def create_expense(
    description: Annotated[str, Body(max_length=100, description="description of the expense")],
    amount: Annotated[float, Body(description="amount of the expense")]
):
    global next_expense_id
    expense_id = next_expense_id
    next_expense_id += 1

  
    expenses[expense_id] = {
        "id": expense_id,
        "description": description,
        "amount": amount
    }

    return JSONResponse(content=expenses[expense_id],status_code=status.HTTP_201_CREATED)


@app.get("/expenses")
def get_all_expenses(
    q: Annotated[
        str | None,
        Query(
            alias="search",
            max_length=50,
            description="You can search expenses by description",
            example="Coffee"
        )
    ] = None):

    if q:
        filtered = [item for item in expenses.values() if q.lower() in item["description"].lower()]
        return JSONResponse(content=filtered, status_code=status.HTTP_200_OK)
        
    return JSONResponse(content=list(expenses.values()), status_code=status.HTTP_200_OK)

@app.get("/expenses/{item_id}")
def get_expense_id(item_id : int = Path(description="ID of the expense to get",ge=1)):
    expense = expenses.get(item_id)
    if expense:
        return JSONResponse(content=expense, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

@app.put("/expenses/{item_id}")
def update_expense(item_id : int = Path(description="ID of the expense to update"),
                    description: Annotated[Optional[str], Body(max_length=100, description="New description")] = None,
                    amount: Annotated[Optional[float], Body(description="New amount")] = None):
    expense = expenses.get(item_id)

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
    if description is not None:
        expense['description'] = description
    if amount is not None:
        expense['amount'] = amount

    return JSONResponse(content=expense, status_code=status.HTTP_200_OK)

@app.delete("/expenses/{item_id}")
def delete_expense_id(item_id : int = Path(description="ID of the expense to delete",ge=1)):
    expense = expenses.get(item_id)
    if expense:
        expenses.pop(item_id)
        return JSONResponse(content={"message": f"Expense with id {item_id} has been deleted"},status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
