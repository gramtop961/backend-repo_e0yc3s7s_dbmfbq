from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Post, Message, Product

app = FastAPI(title="Mauch Garten Hilzingen API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Mauch Garten Hilzingen API running"}


@app.get("/test")
async def test():
    try:
        # Attempt a ping by listing collections
        collections = await db().list_collection_names()
        return {
            "backend": "fastapi",
            "database": "mongodb",
            "database_url": "env://DATABASE_URL",
            "database_name": "env://DATABASE_NAME",
            "connection_status": "ok",
            "collections": collections,
        }
    except Exception as e:
        return {
            "backend": "fastapi",
            "database": "mongodb",
            "connection_status": f"error: {e}",
        }


# Basic endpoints for content used by the site

@app.get("/products", response_model=List[Product])
async def list_products(category: Optional[str] = None):
    filter_dict = {"category": category} if category else {}
    items = await get_documents("product", filter_dict, limit=100)
    return items


class ContactPayload(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str


@app.post("/contact")
async def submit_contact(payload: ContactPayload):
    saved = await create_document("message", payload.model_dump())
    return {"status": "received", "id": saved.get("_id")}


@app.get("/posts", response_model=List[Post])
async def list_posts(tag: Optional[str] = None):
    filter_dict = {"tags": tag} if tag else {}
    items = await get_documents("post", filter_dict, limit=50)
    return items
