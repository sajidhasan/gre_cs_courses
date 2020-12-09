from flask import *

app = Flask(__name__)
#app.config['DEBUG'] = True

PORT = 8877
HOST = '0.0.0.0'

courses = {
        "COMP1252": "MSc Project",
        "COMP1424": "Mobile Application Development",
        "COMP1427": "Cyber Security",
        "COMP1429": "Systems Modelling",
        "COMP1430": "Systems Design and Development",
        "COMP1431": "Audit and Security",
        "COMP1434": "Data Warehousing",
        "COMP1436": "User Experience Design",
        "COMP1470": "Systems Development Management and Governance",
        "COMP1471": "Enterprise Software Engineering Development"
}


@app.route('/')
def index():
    return render_template('index.html', courses = courses )

@app.route('/products')
def producst():
    return render_template('products.html')

#route for returning JSON data provided in the query string
#you get back the data you put in the query
@app.route('/query')
def query():
    if request.args:
        req = request.args
        res = {}
        for key, value in req.items():
            res[key] = value
            
        res = make_response(jsonify(res), 200)
        return res
    res = make_response(jsonify({"Error": "Empty query!"}), 404)
    return res


#get all the course code and course title in JSON format
@app.route("/courses")
def get_json():
    res = make_response(jsonify(courses), 200)
    return res

#get an specific course with code
@app.route('/courses/<code>')
def get_course_title(code):
    if code in courses:
        course_title = courses[code]
        res = make_response(jsonify({code: course_title}), 200)
        return res
    res = make_response(jsonify({"error": "course title not found"}), 404)
    return res

#add a course
@app.route('/courses/add', methods=['POST'])
def add_course():
    req = request.get_json()
    # if req in courses:
    #     res = make_response(jsonify({"error": "course already exists"}), 400)
    #     return res
    courses.update(req)
    res = make_response(jsonify({"message": "course added"}), 201)
    return res

#delete a course
@app.route('/courses/delete/<code>', methods=['DELETE'])
def delete_course(code):
    if code in courses:
        del courses[code]
        res = make_response(jsonify({"message": "course deleted"}), 200)
        return res
    res = make_response(jsonify({"message": "course does not exist"}), 404)
    return res    


if __name__ == "__main__":
    print("Server running on %s"%(PORT))
    app.run(host=HOST, port=PORT)