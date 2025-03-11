from db import get_db
from dependencies.auth import check_task_ownership
from dependencies.cache import get_redis_client
from fastapi import APIRouter, Depends, HTTPException
from schemas.comment import (
    CommentCreate,
    CommentsResponse,
    CommentResponse,
    CommentUpdate,
)
from services.comments import CommentService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/{task_id}", response_model=CommentResponse)
async def create_comment(
    task_id: str,
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis_client),
    is_owner: bool = Depends(check_task_ownership),
):
    """
    Creates a new comment for the task.
    """
    return await CommentService.create_comment(db, redis, comment)


@router.get("/{task_id}", response_model=CommentsResponse)
async def get_comments_by_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis_client),
):
    """
    Receives all the comments for the task.
    """
    comments = await CommentService.get_comments_by_task(db, redis, task_id)
    return {"comments": comments}


@router.delete("/{task_id}/{comment_id}")
async def delete_comment(
    task_id: str,
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis_client),
):
    """
    Removes a comment for the task.
    """
    deleted = await CommentService.delete_comment(db, redis, comment_id, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return {"detail": "Комментарий удалён"}


@router.delete("/{task_id}")
async def delete_comments_by_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis_client),
):
    """
    Removes all comments for the task.
    """
    deleted_count = await CommentService.delete_comments_by_task(db, redis, task_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Комментарии не найдены")
    return {"detail": f"Удалено {deleted_count} комментариев"}


@router.put("/{task_id}/{comment_id}", response_model=CommentResponse)
async def update_comment(
    task_id: str,
    comment_id: int,
    comment: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis_client),
):
    """
    Updates a comment for the task.
    """
    updated_comment = await CommentService.update_comment(
        db, redis, comment_id, comment
    )
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return updated_comment
