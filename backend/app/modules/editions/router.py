from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modules.editions.schemas import (
    EditionArticleAdd,
    EditionCreate,
    EditionResponse,
)

from app.modules.editions.service import (
    add_article_to_edition,
    create_edition,
    get_edition,
    get_editions,
    publish_edition,
    serialize_edition,
)


from app.modules.editions.service import (
    add_article_to_edition,
    create_edition,
    generate_edition_articles,
    get_edition,
    get_editions,
    publish_edition,
)


router = APIRouter(
    prefix="/editions",
    tags=["Editions"],
)


@router.post(
    "",
    response_model=EditionResponse,
)
def create_edition_endpoint(
    request: EditionCreate,
    db: Session = Depends(get_db),
):
    edition = create_edition(
        title=request.title,
        description=request.description,
        db=db,
    )

    return serialize_edition(
        get_edition(
            edition_id=edition.id,
            db=db,
        )
    )


@router.get(
    "",
    response_model=list[EditionResponse],
)
def list_editions(
    db: Session = Depends(get_db),
):
    editions = get_editions(db=db)

    return [
        serialize_edition(edition)
        for edition in editions
    ]


@router.get(
    "/{edition_id}",
    response_model=EditionResponse,
)
def retrieve_edition(
    edition_id: int,
    db: Session = Depends(get_db),
):
    edition = get_edition(
        edition_id=edition_id,
        db=db,
    )

    if edition is None:
        raise HTTPException(
            status_code=404,
            detail="Edition not found",
        )

    return serialize_edition(edition)


@router.post(
    "/{edition_id}/articles",
    response_model=EditionResponse,
)
def add_article(
    edition_id: int,
    request: EditionArticleAdd,
    db: Session = Depends(get_db),
):
    try:
        result = add_article_to_edition(
            edition_id=edition_id,
            article_id=request.article_id,
            db=db,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Edition or article not found",
        )

    edition = get_edition(
        edition_id=edition_id,
        db=db,
    )

    return serialize_edition(edition)


@router.patch(
    "/{edition_id}/publish",
    response_model=EditionResponse,
)
def publish(
    edition_id: int,
    db: Session = Depends(get_db),
):
    try:
        edition = publish_edition(
            edition_id=edition_id,
            db=db,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    if edition is None:
        raise HTTPException(
            status_code=404,
            detail="Edition not found",
        )

    return serialize_edition(edition)


@router.post(
    "/{edition_id}/generate",
    response_model=EditionResponse,
)
def generate_articles(
    edition_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    try:
        edition = generate_edition_articles(
            edition_id=edition_id,
            limit=limit,
            db=db,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    if edition is None:
        raise HTTPException(
            status_code=404,
            detail="Edition not found",
        )

    return edition