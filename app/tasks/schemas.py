from pydantic import BaseModel



class SCreateTask(BaseModel):
    title: str
    completed: bool = False




class UpdateTaskFull(BaseModel):
    title: str
    completed: bool
    category: str

class UpdateTaskPartial(BaseModel):
    title: str | None = None
    completed: bool | None = None
    category: str | None = None



