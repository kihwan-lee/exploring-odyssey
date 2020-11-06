from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import City, Author, Article, Comment #Location,
from main_app.forms import Article_Form, Profile_Form, Comment_Form
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import psycopg2


#-----------------------------------------------------------------------------#
#                              A D M I N / A U T H                            #
#-----------------------------------------------------------------------------#
def signup(request):
    error_message=''

    if request.method == 'POST':
        user_form = UserCreationForm(data = {
            'username':request.POST['username'], 
            'password1': request.POST['password1'], 
            'password2': request.POST['password2']})
        # article_form = Article_Form(data = {'name': request.POST['name'], 'city': request.POST['city']})
        if user_form.is_valid():
            user = user_form.save()
            
            #new_form.user_id = user.id 

            login(request, user)
            return redirect('authors_index') 
        else:
            error_message='Invalid sign-up try again'
    else:
        user_form=UserCreationForm()

    context = {'user_form': user_form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def loginError (request):
    return render(request, 'home.html')

#-----------------------------------------------------------------------------#
#                                S T A T I C                                  #
#-----------------------------------------------------------------------------#
def home (request):
    login_form = AuthenticationForm()
    return render(request, 'home.html', {'form': login_form})

def about(request):
    return render(request, 'about.html')


#-----------------------------------------------------------------------------#
#                                C I T I E S                                  #
#-----------------------------------------------------------------------------#
def cities_index(request):
    cities = City.objects.all()
    # locations = Location.objects.all()
    # 'location': locations,

    context = {'cities': cities}

    return render(request, 'cities/index.html', context)

@login_required(login_url= 'loginError')
def city_detail(request, city_id):
    city = City.objects.get(id=city_id)
    cities = City.objects.all()

    return render(request, 'cities/detail.html', { 'city' : city })


# @login_required(login_url= 'signup')
# def location_search(request):
#     if request.method == 'GET':
#         selection = request.GET.get('id', None)
#         if selection:
#             selected_location = Location.objects.filter(pk=selection)
#             return selected_location
#         else:
#             return 


#-----------------------------------------------------------------------------#
#                                 A U T H O R S                               #
#-----------------------------------------------------------------------------#
@login_required(login_url= 'loginError')
def authors_index(request):
    articles = Article.objects.filter(author=request.user.id)
    author = Author.objects.filter(user=request.user)
    context = { 'articles' : articles, 'user' : request.user, 'author' : author }
    return render(request, 'authors/index.html', context)

@login_required(login_url= 'loginError')
def author_edit(request, user_id):
    error_message=''
    # authors = Author.objects.get(id=user_id)
    if request.method == 'POST':
        author_form = Profile_Form(request.POST, request.FILES, instance = request.user.author)
        if author_form.is_valid():
            author_form.save()
            return redirect('authors_index')
        else:
            error_message='Invalid sign-up try again'
    else: 
        author_form = Profile_Form(instance=request.user.author)
    
        context = {'author_form': author_form}

        return render(request, 'authors/edit.html', context)

#@login_required
#def edit_author(request, user_id):
    #if request.method == 'POST' :
    #add edit to profile functionality
        
#-----------------------------------------------------------------------------#
#                                A R T I C L E S                              #
#-----------------------------------------------------------------------------#
"""Show all articles."""
def articles_index(request):
    articles = Article.objects.order_by('created_on')
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)

"""Show a single article."""
@login_required(login_url= 'loginError')

def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    comments = article.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = Comment_Form(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    
    else:
        comment_form = Comment_Form()

    context = {
        'article': article,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request, 'articles/detail.html', context)

"""Adds an Article"""
@login_required(login_url= 'loginError')
def article_add(request, city_id):
    city = City.objects.get(id = city_id)
    if request.method == 'POST':
        new_form = Article_Form(request.POST)
        if new_form.is_valid():
            new_article = new_form.save(commit=False)
            new_article.author_id = request.user.id
            new_article.city = city
            new_article.save()

            return redirect('city_detail', city_id)
    else: 
        new_form = Article_Form()
        context = {
            'new_form': new_form,
            'city': city
        }
        return render(request, 'articles/add.html', context)

"""Edit an Article"""
# We want to identify the article by its 'id'. 
# When a user presses a button to "Edit", this will trigger a POST).
# We want to get the selected Article object, render the form to our
# HTML template. If the user fulfills the form's requirements before
# submitting the form, it's saved and they'll be redirected.
@login_required(login_url= 'loginError')
def edit_article(request, article_id):
    sel_article = Article.objects.get(id=article_id)
    # Naming convention: "sel" => selected #
    if request.method == 'POST':
        art_form = Article_Form(request.POST, instance=sel_article)
        if art_form.is_valid():
            updated_article = art_form.save()
            return redirect('article_detail', updated_article.id)
    else:
        art_form = Article_Form(instance=sel_article)
        context = {
            'article': sel_article,
            'art_form': art_form
        }
        return render(request, 'articles/edit.html', context)

"""Delete an Article"""
# We want to identify the article by its 'id'. 
# When a user presses a button to "Delete", this will trigger a POST).
# We want to get the selected Article object and delete it
# then redirect them to the main cities_index
@login_required(login_url= 'loginError')
def delete_article(request, article_id):
    if request.method == 'POST':
        Article.objects.get(id=article_id).delete()

        return redirect('cities_index')


#-----------------------------------------------------------------------------#
#                                C O M M E N T S                              #
#-----------------------------------------------------------------------------#

def edit_comment(request, comment_id):
    """Edit an existing comment."""
    comment = Comment.objects.get(id=comment_id)
    article = comment.article

    if request.method != 'POST':
        # Initial request; pre-fill form with current comment.
        form = Comment_Form(instance=comment)
    else:
        # POST data submitted; process data.
        form = Comment_Form(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_detail', article_id=article.id)

    context = {'comment': comment, 'article': article, 'form': form}
    return render(request, 'comments/edit.html', context)

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    article = comment.article

    if request.method == 'POST':
        Comment.objects.get(id=comment_id).delete()

        return redirect('article_detail', article_id=article.id)


# Importing Location Data
# db = psycopg2.connect(dbname="location")
# cur = db.cursor()
# insert_statement = "INSERT INTO location (region_id, region_name, location, location_name, location_desc, english_proficiency, primary_lang, currency, ideal_season,  poi_1, poi_2, poi_3, url) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# values = [
#         (1,'Africa',1,'Botswana','Botswana is nothing short of enchanting! It’s home to incredible wildlife, breathtaking national parks, and intriguing local culture and history. It’s also one of the most popular destinations in Africa, especially for safaris!','t','Setswana','Pula','Fall','Explore the Okavango Delta','See Meerkats at Jacks Camp','Vist Chobe National Park', ''),
#         (1,'Africa',2,'Egypt','Between the Nile, the Red Sea, Alexandria, Cairo, and pyramids that date back to 2500 BC, Egypt offers so much history and culture.','t','Masri','EGP','Spring','Visit the Egyptian Museum','Pyramids of Giza','Explore Alexandria', ''),
#         (1,'Africa',3,'Kenya','Kenya is a country full of diverse landscapes and cultures, along with some unforgettable wildlife experiences. With endless plains that are full of wildlife, rolling hills, lush mountains, and a coastline that will leave you speechless, Kenya was made to explore!','t','Swahili','KES','Summer','Witness the Great Migration','Stay at Giraffe Manor','Helicopter over Mount Kenya at sunrise', ''),
#         (1,'Africa',4,'Mauritius','Mauritius is THE destination for a beach getaway offering palm-lined coastlines and water as clear as glass. This destination is for snorket fanatics and has a haven of dolphins and sea turtles. For land dwellers, hike a jungle trail to a waterfall, or just work on your tan.','t','English','MUR','Winter','Colored Earth of Chamarel','Hike Le Morne Brabant','Go Snorkeling or Diving', ''),
#         (1,'Africa',5,'Morocco','Morocco is a country that draws you in. From the colorful, heady markets filled with the rich scents of spices to the vibrant Atlas Mountains, there is just so much to see in this incredible North African country.','t','Arabic','Dirham','Spring','Walk the streets of Marrakech','Visit Chefchaouen','Desert Glamping', ''),
#         (1,'Africa',6,'South Africa','South Africa provides incredible opportunities for those who prefer the outdoor lifestyle. Additionally, this destination is packed with interesting people, hiking trails, horseback riding, plenty of beach space or getting lunch at a scenic restaurant.','t','Zulu','Rand','Summer','Explore Cape Town','Road Trip the Cape Peninsula','Road Trip Across the Garden Route', ''),
#         (2,'Asia',7,'Cambodia','Cambodia is a popular stop along the Southeast Asia backpacking route. The main attraction being the awe-inspiring ancient temples of Angkor Wat, located just outside of Siem Reap and known as the largest religious monument in the world.','f','Khmer','KHR','Winter','Temples of Angkor Wat','Bayon Temple','Kampot', ''),
#         (2,'Asia',8,'Indonesia','Indonesia offers over 17,800 islands including Bali, Komodo Island, Gili Islands, and more. Trek to the peak of the Kelimutu volcanic lake and scuba dive throughout the Gili Islands - Indonesia is a bucket list destination.','f','Indonesian','IDR','Summer','Raja Ampat Islands','Bali','Komodo Island', ''),
#         (2,'Asia',9,'Japan','From robot restaurants and Mario Karting in the streets to ancient temples and cat cafes, Japan blends its traditional and modern culture to provide tourists with an unforgettable experience. ','t','Japanese','JPY','Spring','Must see Mount Fuji','Eat at a Robot Restaurant','Explore the Osaka Castle', ''),
#         (2,'Asia',10,'The Maldives','Geographically surprising of 26 natural atolls, this island destination is known for providing the first accurate maritime charts of the Indian Ocean.','t','Dhivehi','MVR','Winter','Snorkel at the Banana Reef','Male Market for souvenir shopping','Baros Island to zen out', ''),
#         (2,'Asia',11,'Singapore','This thrilling city-state country is located off the tip of Malaysia. It boast a beautiful blend of culture including Malaysian, Indian, Chinese, Arab and English.','t','Mandarin','SGD','All Year','A 158-year-old tropical oasis, the Singapore Botanic Gardens are a must see','Head to Chinatown for the epic Mid-Autumn Festival','Visit the historic neighborhood Joo Chiat!', ''),
#         (2,'Asia',12,'Sri Lanka','Marco Polo visited Sri Lanka in the fourteenth centry and said it was "undoubtedly the finest island in the world," and to this day it is one of the most beautiful travel destinations in the world','t','Sinhala & Tamil','LKR','Winter','Visit Anuradhapura a UNESCO World Heritage cultural site','Climb to the top of Mihintale','Visit the stunning rock fortress Sigiriya', ''),
#         (2,'Asia',13,'Thailand','A must for many travelers, Thailand offers unique experiences whether you came to view the majestic temples or indulge in the amazing food.','t','Thai','THB','Winter','Chiang Mai Flower Festival','Bangkok','Sanctuary of Truth', ''),
#         (2,'Asia',14,'Vietnam','Gorgeous landscapes, tasty food, and vibrant energy, Vietnam will take your breath away while giving you a full sensory experience. ','f','Vietnamese','VND','All Year','Boat cruise Bai Tu Long Bay','Explore Saigon','Hanoi ', ''),
#         (2,'Asia',15,'South Korea','South Korea is a highly developed country with its iconic pop cultural influences and is home of one of the worlds fastest internet connection speeds!','t','Korean','won','Spring','Changdeokgung Palace','Busan','Seoraksan National Park', ''),
#         (3,'Caribbean',16,'The Caribbean','This is where tropical island dreams come true. Each of the comprising 30 island territories that make up The Caribbean offer very unique experiences to all travelers. ','t','Spanish','USD','Winter','Havana','Antigua','St Lucia', ''),
#         (3,'Caribbean',17,'Aruba','Aruba is like no other. Its unique melting pot set in the middle of the Caribbean will definitely capture your heart.','t','Papiamento','florin','Summer','Bubali Bird Sanctuary','Arikok National Park','Oranjestad', ''),
#         (3,'Caribbean',18,'The Bahamas','The Bahamas is true paradise sprinkled with 700 islands over 100000 square miles of ocean.','t','English','BSD','Winter','Nassau','Coral-reef diving in Sea of Abaco','Pig Beach', ''),
#         (3,'Caribbean',19,'British Virgin Islands','The white sandy beaches and the world class sailing, makes the BVI a popular travel destination.','t','English','USD','Fall','The Baths on Virgin Gorda','BVI Spring Regatta','Jost Van Dyke', ''),
#         (3,'Caribbean',20,'Cuba','A unique blend of African, Spanish, and Caribbean influences, Cuba has some of the best food in the world.','t','Spanish','CUP','Winter/Spring','Old Havana','Plaza Mayor','Museo Romantico', ''),
#         (3,'Caribbean',21,'The Dominican Republic','Bordered by Haiti and the Caribbean, this country is known for its year round golf courses and is home to the Caribbeans tallest mountain peak, Pico Duarte.','t','Spanish','DOP','Winter/Spring','Santo Domingo Zona Colonial','Playa Dorada','Whale Watching in Samana Bay', ''),
#         (4,'Central America',22,'Panama','The bridge between two continents, Panama is chalk full of history, wildlife, and adventure.','t','Spanish','PAB','Winter','Panama City','Bocas Del Toro Scuba Diving','San Blas Islands', ''),
#         (4,'Central America',23,'Honduras','The second largest country in Central America is home to reefs and rainforest but also has a history of being the murder capital of the world. ','t','Spanish','HNL','Winter/Spring','Raotan, Bay Islands','Copan Ruins','Museum of Mayan Sculpture', ''),
#         (4,'Central America',24,'Guatemala','From riding around on chicken buses to exploring the many historical sites, Guatamala is a true gem in Central America.','t','Spanish','GTQ','Winter','Antigua','Lake Atitlan','Tikal in the Peten', ''),
#         (4,'Central America',25,'Costa Rica','With jaw-dropping landscapes, friendly locals and jungle explorations, it is no wonder why touritsts flock to Costa Rica.','t','Spanish','CRC','Winter','Envision Festival','Puerto Viejo','Arenal Volcano', ''),
#         (4,'Central America',26,'Belize','Explore Mayan ruins and relax on picturesque beaches all in one trip! Belize has something for everyone!','t','English','BZD','Winter','Actun Tunichil Muknal','Caracol','St. John Cathedral', ''),
#         (5,'Europe',27,'Austria','Welcome to the home of Mozart and Wienerschnitzel. From the moment you arrive in Austria, you will be taken back by the feeling you have stepped into a winter wonderland. ','t','Austrian German','EUR','All Year','Krems','Melk','Vienna', ''),
#         (5,'Europe',28,'Belgium','Belgium is a destination for the history buffs and chocolate lovers in our life.','t','Dutch','EUR','All Year','Brussels','Bruges','Ghent', ''),
#         (5,'Europe',29,'Croatia','The sea-to-table cuisine and fantastic wine make Croatia a food lovers paradise.','t','Croatian','HRK','All Year','Plitvice National Park','Krka National Park','Istria', ''),
#         (5,'Europe',30,'Czech Republic','Visiting the Czech Republic is a great starting point for any Eastern European trip.','t','Czech','CZK','All Year','Prague','Kutna Hora','Karlovy Vary', ''),
#         (5,'Europe',31,'Denmark','Often touted as the happiest country - it is easy to see why. ','t','Danish','Krone','Spring/Summer/Fall','Bulbjerg Klint','Thy National Park','Rabjerg Mile', ''),
#         (5,'Europe',32,'England','Ohh the history and iconic sites in England are quite spectacular. Whether you are a history buff or a Harry Potter fan, everyone can nerd out in England. ','t','English','British Pound','All Year','London','Stonehenge','Buckingham Palace', ''),
#         (5,'Europe',33,'France','When it comes to traveling, Paris seams to be one of the most sought after destinations and for good reason too. But do not let it steal all the limelight! France in general has alot to offer.','t','French','EUR','All Year','Paris','Bordeaux','Corsica', ''),
#         (5,'Europe',34,'Germany','With its long history and exceptional food, Germany is consider the heart of Europe','t','German','EUR','All Year','Munich ','Berlin ','Frankfurt', ''),
#         (5,'Europe',35,'Greece','If you want to leasure amongst the olive trees with a glass of wine than Greece is the country for you!','t','Greek','EUR','Summer','Santorini','Athens','Thessoliniki', ''),
#         (5,'Europe',36,'Iceland','Want to live out of a van for a few weeks and travel around? Well come to Iceland and begin your adventure!','t','English','EUR','All Year','Blue Lagoon','Golden Circle','Reykjavik', ''),
#         (5,'Europe',37,'Ireland','You cant get any greener than Ireland. Talk about craggy coastlines and lush meadows as far as the eye can see! Any traveler looking for a beer and a frolic would be happy in Ireland. ','t','Gaelic','EUR','Spring/Summer/Fall','The Cliffs of Moher','Grafton Street, Dublin','Killarney National Park', ''),
#         (5,'Europe',38,'Italy','If your looking for a "Eat, Pray, Love" experience, Italy is your go too. ','t','Italian','EUR','All Year','Florence','Pompeii','Rome', ''),
#         (5,'Europe',39,'Malta','Malta has a laidback tropical vibe with picture perfect beaches and amazing diving.','t','Maltese','EUR','All Year','Gjantija Temple','Mdina','Valletta', ''),
#         (5,'Europe',40,'The Netherlands','A wonderland full of museums, quirky hotels, a buzzing food scene, and photogenic spots at every corner, The Netherlands is a country of style and adventure','t','Dutch','EUR','All Year','Amsterdam','Hull','RotterDam', ''),
#         (5,'Europe',41,'Poland','While parts of the country do still feel like a time warp, modern Poland also has a vibrant urbanity, enticing food and design culture, dynamic history, and kindhearted natives.','t','Polish','PLN','Spring/Fall','Wroclaw','Warsaw','Cracow', ''),
#         (5,'Europe',42,'Portugal','Portugal offers the pleasure of having white sandy beaches, beautiful cities, and rugged coastlines.','t','Portuguese','EUR','Spring/Fall','Aveiro','Lisbon','Porto', ''),
#         (5,'Europe',43,'Scotland','Scotland is known for its picturesque landscapes, jovial people, and booze!','t','Gaelic','EUR','Spring/Fall','Edinburgh','Glasgow','Inverness', ''),
#         (5,'Europe',44,'Spain','Spain is known for its festivals, beaches, and of course nigthlife!','t','Spanish','EUR','Summer/Fall','Barcelona','Canary Islands','Granada', ''),
#         (5,'Europe',45,'Sweden','Sweden is simply a jaw dropper. With its beautiful lakes, dense forests, and snow-capped mountains, it is a must for all travelers to experience!','t','Swedish','SEK','Summer','Gothenburg','Lilla Korno','Stockholm', ''),
#         (5,'Europe',46,'Switzerland','Chocolate and cheese. Sprinkle in some snow covered mountains and crystal clear lakes. Do I need to say anymore? ','t','Swiss German, Swiss French, Swiss Italian','CHF','Spring/Fall','The Matterhorn ','Jungfraujoch: The Top of Europe','Interlaken', ''),
#         (6,'The Middle East',47,'Egypt','With a rich history and an exotic culture, Egypt is full of unspoken treausures that the adventurous travel should experience. ','t','Arabic','EGP','Fall/Winter/Spring','Pyramids of Giza','Coptic Cairo','Egyptian Museum of Antiquities', ''),
#         (6,'The Middle East',48,'Jordan','Jordan is a diverse country with lots to explore and experience!','t','Arabic','JOD','Spring/Fall','Amman','Dead Sea','Petra', ''),
#         (6,'The Middle East',49,'Turkey','Visiting Turkey is one of the easiest, safest, and most fascinating ways to explore the Islamic culture.','t','Turkish','TRY','Spring/Summer/Fall','Istanbul','"Fairy chimneys"','Pamukkale', ''),
#         (6,'The Middle East',50,'United Arab Emirates','This city-state country has the perfect combination between modern/traditional and desert/sea.','t','Arabic','AED','Fall/Winter/Spring','Burj Khalifa','Sheikh Zayed Mosque','Hajar Mountains', ''),
#         (7,'North America',51,'Canada','Oh Canada! Your people and maple sugar always tends to leave travelers with a smile on their face.','t','French/English','CAD','Summer/Fall','Banff','Montreal','Whistler', ''),
#         (7,'North America',52,'Mexico','From lively music and vibrant colors, Mexico will keep you dancing through your stay.','t','Spanish','MXN','All Year','Oaxaca','Tulum','Cozumel', ''),
#         (7,'North America',53,'Puerto Rico','In Puerto Rico you may find yourself wandering the streets of Old San Juan or splashing around on the crystal clear beaches.','t','Spanish','USD','Spring','Bioluminescent Bay','San Juan','Flamenco Beach', ''),
#         (7,'North America',54,'New York City','From the Empire State Building to The Statue of Liberty to the endless brunch spots. NYC has it all.','t','English','USD','Spring/Summer/Fall','Central Park','Statue of Liberty','Empire State Building', ''),
#         (7,'North America',55,'Chicago','The Windy City has lots to see. From the Chicago Bean to the Sears Tower, this city has some magnificient architecture that will captivate any traveler.','t','English','USD','Spring/Summer/Fall','Navy Pier ','The Shed Aquarium','Sears Tower', ''),
#         (7,'North America',56,'Los Angeles','LA is a sprawling city that is home to sun-kissed beaches, laidback neighborhoods and fancy Tinseltown.','t','English','USD','All Year','Universal Studios Hollywood','Old Town Pasadena','Sunset Boulevard', ''),
#         (7,'North America',57,'San Francisco','San Fran means mild climate all year round. With temps always staying around 70 who wouldnt want to visit here?','t','English','USD','All Year','Golden Gate Bridge','Alcatraz','Expore Haight-Ashbury', ''),
#         (7,'North America',58,'Australia','Welcome downunder! Where kangaroos hop wildly and tourists rome freely.','t','English','USD','All Year','Art & Museums in Melbourne','Brisbane','Sydney', ''),
#         (7,'North America',59,'French Polynesia','With diverse marine life, French Polynesia boasts some of the most sought after diving in the world!','t','French','CFP','Summer','Bora Bora','Rangiroa','Tahiti', ''),
#         (7,'North America',60,'New Zealand','Backpacking New Zealand has changed my life. It was so easy to find work and good company here. Not to mention breath taking views!','t','English','NZD','All Year','Milford Sounds','Tauranga','Coromandel Peninsula', ''),
#         (8,'South America',61,'Bolivia','Bolivia is one-of-a-kind. Dubbed a country of extremes, Bolivia offers a rainbow of climates to the true explorer.','t','Spanish','BOB','Summer/Fall','La Paz','Death Road','Uyuni Salt Flats', ''),
#         (8,'South America',62,'Brazil','Brazil covers around half of South America. This makes it the largest country in South America. So its no surprise that it offers alot of diverse experiences and a rainbow of different geographicaly features. ','t','Portuguese','BRL','All Year','Rio de Janeiro','Fernando de Noronha','Foz de Iguacu falls', ''),
#         (8,'South America',63,'Colombia','Colombia. Not only is it the second most populated country in South America, but it is also home to a whopping 10% of the worlds biodiversity.','t','Spanish','COP','Winter','Bogota','Guadalupe','Tayrona Naitonal Park', ''),
#         (8,'South America',64,'Ecuador','Named after the equator that runs through it, this little Andean country it well known as one of the inspirations for Darwins theory of evolution. ','t','Spanish','USD','All Year','Galapagos Islands','Tungurahua Volcanoe','Quito', ''),
#         (8,'South America',65,'Peru','Peru is home to natural wonders such as the Amazon, Lake titicaca, and Rainbow Mountain.','t','Spanish','PEN','All Year','Inca Trail','Machu Picchu','Cusco', ''),
#         (8,'South America',66,'Chile','Chile is the richest nation in South America and leads Latin America in peace, income per capita, and democratic development.','t','Spanish','CLP','All Year','Santiago','Torres del Paine National Park','Easter Island', '')
#         ]

# cur.execute(insert_statement, values)

# db.commit()
# db.close()
