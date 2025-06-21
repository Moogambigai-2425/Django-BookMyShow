from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages

def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movies = Movie.objects.filter(name__icontains=search_query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie).prefetch_related('seats')
    
    # Prepare a list of theaters with available seat counts
    theater_data = []
    for theater in theaters:
        available_seats_count = theater.seats.filter(is_booked=False).count()
        theater_data.append({
            'theater': theater,
            'available_seats_count': available_seats_count
        })
    
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theater_data': theater_data})

@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []
        
        if not selected_seats:
            messages.error(request, "No seat selected.")
            return render(request, "movies/seat_selection.html", {'theater': theater, "seats": seats})

        # Check for booked seats in one query
        booked_seats = Seat.objects.filter(id__in=selected_seats, is_booked=True)
        error_seats = [seat.seat_number for seat in booked_seats]

        if error_seats:
            messages.error(request, f"The following seats are already booked: {', '.join(error_seats)}")
            return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats})

        # Proceed with booking
        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)
            if not seat.is_booked:
                try:
                    Booking.objects.create(
                        user=request.user,
                        seat=seat,
                        movie=theater.movie,
                        theater=theater
                    )
                    seat.is_booked = True
                    seat.save()
                except IntegrityError:
                    error_seats.append(seat.seat_number)

        if error_seats:
            messages.error(request, f"The following seats could not be booked: {', '.join(error_seats)}")
        else:
            messages.success(request, "Seats booked successfully!")
            return redirect('profile')

    return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats})
