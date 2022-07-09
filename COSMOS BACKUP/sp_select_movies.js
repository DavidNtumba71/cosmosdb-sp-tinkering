function sp_select_movies_before_year(release_date) {
    var collection = getContext().getCollection();

    var whereQuery = {
        query: "SELECT * FROM Movies m WHERE m.release_date <= @release_date",
        parameters: [{ name: "@release_date", value: year }],
      }; 

    var isAccepted = collection.queryDocuments(
        collection.getSelfLink(),
        whereQuery,
        function (err, feed, options) {
            if (err) throw err;
            if (!feed || !feed.length) {
                var response = getContext().getResponse();
                response.setBody('no docs found');
            }
            else{
                var response = getContext().getResponse();
                var body = { feed };
                response.setBody(JSON.stringify(body));
            }            
        });

    if (!isAccepted) throw new Error('The query was not accepted by the server.');
};