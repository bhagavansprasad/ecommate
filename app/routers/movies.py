from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Movie
from app.schemas import MovieCreate, MovieResponse, MovieSchema
# from app.security import decode_access_token, get_current_token
from pdbwhereami import whereami, whocalledme

router = APIRouter()

@router.post("/movies/", response_model=MovieResponse)
def create_movie(
    movie: MovieCreate, 
    db: Session = Depends(get_db), 
):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/movies", response_model=list[MovieSchema])
def list_all_movies(
    db: Session = Depends(get_db), 
):
    
    whereami()
    movies = db.query(Movie).all()
    return movies

@router.get("/movies/{movie_id}", response_model=MovieResponse)
def read_movie(request: Request, movie_id: int, 
    db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    print("token_in_server", token)
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int, 
    updated_movie: MovieCreate, 
    db: Session = Depends(get_db), 
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in updated_movie.dict().items():
        setattr(movie, key, value)
    db.commit()
    return movie

@router.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int, 
    db: Session = Depends(get_db), 
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfully"}
