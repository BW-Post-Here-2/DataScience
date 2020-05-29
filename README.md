# Predict Route:

``` python
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
```