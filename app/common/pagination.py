from fastapi.responses import JSONResponse

def paginate_query(query, page: int, per_page: int, response_model, not_found_response, label: str = "items"):
    if page < 1:
        return JSONResponse(status_code=422, content={"message": "Page must be greater than or equal to 1", "status": 422})
    if per_page < 1:
        return JSONResponse(status_code=422, content={"message": "Limit must be greater than or equal to 1", "status": 422})
    total_items = query.count()
    total_pages = (total_items + per_page - 1) // per_page
    skip = (page - 1) * per_page
    items = query.offset(skip).limit(per_page).all()
    if not items:
        return JSONResponse(status_code=404, content=not_found_response.dict())
    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_items": total_items,
        label: [response_model.model_validate(u) for u in items]
    }
