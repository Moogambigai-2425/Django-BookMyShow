from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from movies.models import Movie , Booking
from django.db.models import Count
from django.shortcuts import get_object_or_404

def home(request):
    movies= Movie.objects.all()
    return render(request,'home.html',{'movies':movies})
def register(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('profile')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('/')
    else:
        form=AuthenticationForm()
    return render(request,'users/login.html',{'form':form})

@login_required
def profile(request):
    bookings= Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'u_form': u_form,'bookings':bookings})

@login_required
def reset_password(request):
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'users/reset_password.html',{'form':form})

@login_required
def dashboard(request):
    recommendations = recommend_movies_based_on_booking_history(request.user)
    return render(request, 'users/dashboard.html', {'recommendations': recommendations})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'users/movie_detail.html', {'movie': movie})

def recommend_movies_based_on_booking_history(user):
    """
    Recommend movies to the user based on booking history and genre diversity.
    Logic:
    1. Find movies the user has booked.
    2. Identify genres of those movies.
    3. Recommend movies from the same genres.
    4. If no recommendations are found, fallback to popular movies across all genres.
    """
    # Step 1: Get movie ids and genres booked by current user
    user_booked_movies = Booking.objects.filter(user=user).select_related('movie')
    user_booked_movie_ids = user_booked_movies.values_list('movie_id', flat=True)
    user_genres = user_booked_movies.values_list('movie__genres', flat=True).distinct()

    if not user_booked_movie_ids:
        # If user has no bookings, recommend some popular movies
        return retrieve_popular_movies()
    
    # Step 2: Recommend movies from the same genres
    recommended_movies = Movie.objects.filter(
        genres__in=user_genres
    ).exclude(
        id__in=user_booked_movie_ids
    ).annotate(
        popularity=Count('booking')
    ).order_by('-popularity')

    if recommended_movies.exists():
        return recommended_movies

    # Step 3: Fallback to popular movies across all genres
    return retrieve_popular_movies()

def retrieve_popular_movies():
    """
    Retrieve popular movies based on total bookings across all genres.
    """
    return Movie.objects.annotate(
        booking_count=Count('booking')
    ).order_by('-booking_count')[:10]
