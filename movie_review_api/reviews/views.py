from rest_framework import generics, viewsets, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import login
from .models import Movie, Review
from .serializers import UserSerializer, RegisterSerializer, MovieSerializer, ReviewSerializer
from django.conf import settings
import requests
from django.db.models import Avg












class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_movies_view(request):
    user = request.user
    reviews = Review.objects.filter(user=user)
    reviewed_movies = [review.movie.id for review in reviews]
    recommendations = Movie.objects.exclude(id__in=reviewed_movies).annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')[:10]
    serializer = MovieSerializer(recommendations, many=True)
    return Response(serializer.data)

"""@api_view(['GET'])"""
"""@permission_classes([IsAuthenticated])"""
"""def recommend_movies_view(request):
    user = request.user
    user_id = user.id

    # Fetch all reviews
    reviews = Review.objects.all()
    
    # Convert reviews to a DataFrame
    reviews_df = pd.DataFrame(list(reviews.values('user_id', 'movie_id', 'rating')))
    
    # Prepare the data for surprise
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(reviews_df[['user_id', 'movie_id', 'rating']], reader)
    
    # Split the data into training and testing sets
    trainset, testset = train_test_split(data, test_size=0.25)
    
    # Use the SVD algorithm for collaborative filtering
    algo = SVD()
    algo.fit(trainset)
    
    # Get a list of all movie IDs
    all_movie_ids = Movie.objects.values_list('id', flat=True)
    
    # Get a list of movies the user has already reviewed
    reviewed_movie_ids = reviews_df[reviews_df['user_id'] == user_id]['movie_id'].tolist()
    
    # Predict ratings for movies the user hasn't reviewed yet
    predictions = []
    for movie_id in all_movie_ids:
        if movie_id not in reviewed_movie_ids:
            pred = algo.predict(user_id, movie_id)
            predictions.append((movie_id, pred.est))
    
    # Sort the predictions by estimated rating in descending order
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    # Get the top 10 movie IDs
    top_movie_ids = [pred[0] for pred in predictions[:10]]
    
    # Fetch the top 10 movie objects
    top_movies = Movie.objects.filter(id__in=top_movie_ids)
    
    # Serialize the movie data
    serializer = MovieSerializer(top_movies, many=True)
    
    return Response(serializer.data) """





def fetch_movies_from_tmdb():
    url = 'https://api.themoviedb.org/3/movie/popular'
    params = {'api_key': settings.TMDB_API_KEY}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        movies = response.json().get('results', [])
        for movie in movies:
            movie_id = movie['id']
            details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}'
            details_response = requests.get(details_url)
            
            if details_response.status_code == 200:
                details = details_response.json()
                
                Movie.objects.update_or_create(
                    title=details['title'],
                    defaults={
                        'description': details['overview'],
                        'release_date': details['release_date'],
                      
                    }
                )
            else:
                print(f"Failed to fetch movie details for movie ID {movie_id}: {details_response.status_code}")
    else:
        print(f"Failed to fetch movies: {response.status_code}")
