from flask import Flask,request,jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

star_ratings = [[0,1399,1],[1400,1599,2],[1600,1799,3],[1800,1999,4],[2000,2199,5],[2200,2499,6],[2500,3000,7]]

def codechef(username):
    # user = input("USERNAME : ")
    # print("finding...")
    global star_ratings
    url = "https://codechef.com/users/{}".format(username)
    page = requests.post(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    rating = soup.find('div', class_='rating-number')
    RatingsRankings = soup.find('div', class_='rating-ranks')
    AllRank = RatingsRankings.find_all('strong')

    GlobalRank = AllRank[0].text
    CountryRank = AllRank[1].text
    Rating = rating.text

    STAR = 0  # star rating

    print("Global Rank: ", GlobalRank)
    print("Country Rank: ", CountryRank)
    print("Rating: ", Rating)

    if int(rating.text) > 3000:
        print("Stars: ", 7)
        STAR = "7"
    else:
        for i in star_ratings:
            if int(rating.text) in range(i[0], i[1]):
                print("Stars: ", i[2])
                STAR = i[2]

    data = {
        'global_rank': GlobalRank,
        'country_rank': CountryRank,
        'rating': Rating,
        'stars': STAR
    }

    return data

@app.route('/codechef/<username>',methods=['GET'])
def get_codechef(username):
	try:
		return jsonify(codechef(username))
	except:
		try:
			return jsonify(codechef(username))
		except:
			return jsonify({"ERROR":"INVL METHOD / WRONG PARAMETERS / USERNAME NOT FOUND"})

#ERROR HANDLING
#this is testing comment
#404
@app.errorhandler(404)
def pg404(e):
	dt = {
	"ERROR" : "404",
	"AVL" : "['/codechef']"
	}
	return jsonify(dt)

#500
@app.errorhandler(500)
def pg500(e):
	dt = {
	"ERROR" : "505",
	"AVL" : "['/codechef']"
	}
	return jsonify(dt)

if (__name__ == '__main__'):
    app.run(debug=True)