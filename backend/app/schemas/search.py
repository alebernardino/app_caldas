from pydantic import BaseModel


class ProviderSearchFilters(BaseModel):
    function_name: str | None = None
    min_rating: float | None = None
    only_five_star_concept: bool = False
    is_available: bool | None = None
