from fastapi import APIRouter
import services.HespressService as HespressService

router = APIRouter()


@router.get("/categorises", response_model=None)
async def get_hespress_categorises():
    return HespressService.get_all_categories()


@router.get("/get-category-id/{category_slug}", response_model=None)
async def get_articles_of_category(category_slug: str):
    return HespressService.get_category_id(category_slug)


@router.get("/articles/bref", response_model=None)
async def get_bref_articles_of_category(category_slug: str, page: int):
    articles = HespressService.get_articles_of_category(category_slug, page)
    return {
        "count": len(articles),
        "data": articles
    }


@router.get("/articles/{id_article}", response_model=None)
async def get_article(id_article: int):
    return HespressService.get_article(id_article)
