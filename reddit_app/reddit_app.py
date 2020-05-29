# reddit_app.py

# Some sections of the code below were taken from the work
# of John Duke and Chris Hartig.

from _pickle import load
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from flask import Flask, request, jsonify
import requests


# Define create_app function
def create_app():
    app = Flask(__name__)

    # From example video.
    # Understanding flask.request
    # https://www.youtube.com/watch?v=hAEJajltHxc
    @app.route("/query")
    def query():
        language = request.args.get("language")
        region = request.args["region"]
        return """<h1>The language is {}</h1>
                  <h1>The region is {}</h1>""".format(language, region)


    @app.route("/predict.json", methods=["POST"])
    def predict():
        # Here the request context is creating a proxy of a
        # requests object with the get_json method applied.
        request_data = request.get_json(force=True)

        # The method used for title and content here is
        # functionally identical to the way that Flask
        # handles HTML forms Jinja passed inside, just
        # without the form.
        title = request_data["title"]
        content = request_data["content"]
        post = title + " " + content

        model = load(open("reddit_model_nc.pkl", "r+b"))

        predictions = pd.DataFrame(model.predict_proba([post])[0])
        predictions["subreddit"] = model.classes_
        predictions.columns = ["certainty", "subreddit"]
        predictions = predictions[["subreddit", "certainty"]]
        predictions = predictions.sort_values(by="certainty", ascending=False)
        predictions = predictions.reset_index()
        predictions = predictions.drop(columns=["index"])

        # Here we have limited the list of potential
        # subreddits to 3 in order to give the user only the
        # best selection of subreddit.
        potential_subreddits = []
        for i in range (0, 5):
            potential_subreddits.append(
                {"id" : i,
                 "subreddit" : predictions["subreddit"][i],
                 "probability" : f"{round(predictions.certainty[i] * 100, 2)}"}
            )
        return jsonify(potential_subreddits)


    @app.route("/test")
    def test():
        title = "Reddit Post"
        content = "This is a Reddit post."
        post = {"title" : title, "content" : content}

        url = "http://127.0.0.1:5000/predict.json"

        req = requests.post(url, json=post)
        return req.text

    @app.route("/")
    def base():
        strang = "Hello birthday handsome Joo Woon"
        return strang


if __name__ == "__main__":

    # my_app = create_app()

    # Here the argument "r+b" ensures that the model will
    # function regardless of which system is being used.
    model = load(open("reddit_model_nc.pkl", "r+b"))
    
    # Testing the model with a hypothetical Reddit post
    # to ensure that it will work in our function later.
    red_post = """
    Bizarre Foods

    While in Taiwan I had the opporotunity to try salted
    cicadas. They actually were not that bad. They tasted
    like a cross between a walnut, chicken, and potato
    chips. Unfortunately for my roommate, he was allergic.
    The poor sucker was up all night.
    
    Anyone else eat or drink anything bizarre lately?
    Anyone else have an allergic reaction to that bizarre
    food or beverage?
    """
    
    predictions = pd.DataFrame(model.predict_proba([red_post])[0])
    predictions["subreddit"] = model.classes_
    predictions.columns = ["certainty", "subreddit"]
    predictions = predictions[["subreddit", "certainty"]]
    predictions = predictions.sort_values(by="certainty", ascending=False)
    predictions = predictions.reset_index()
    predictions = predictions.drop(columns=["index"])

    print(predictions)
    print(predictions["subreddit"][0], predictions["certainty"][0])