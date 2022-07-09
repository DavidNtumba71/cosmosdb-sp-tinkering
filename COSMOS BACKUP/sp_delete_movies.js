function DeleteMoviesOfGenre(genre) {
    var collection = getContext().getCollection();

    var deletedDocuements = 0;

    var query = {
        query: "SELECT * FROM Movies m where m.primary_genre = @primary_genre",
        parameters: [{ name: "@primary_genre", value: genre }],
    };

    function QueryMoviesOfGenre(collection) {
        return collection.queryDocuments(
            collection.getSelfLink(),
            query,
            (options = {}),
            (callback = QueryCallback)
        );
    }

    function QueryCallback(err, documents, responseOptions) {
        if (err) throw new Error("Error:" + err.message);
        if (documents.length == 0) throw "no document found.";
        ExecuteDeletions(documents, genre);
        return;
    }

    function ExecuteDeletions(documents) {
        documents.forEach(function (document, genre) {
            document.genre = genre;
            var accept = collection.deleteDocument(
                document._self,
                document,
                (callback = DeleteCallBack)
            );
            if(accept) deletedDocuements++;
            else throw "Unable to update document"; 
        });
    }

    function DeleteCallBack(err, deleteion) {
        if (err) throw new Error("Error:" + err.message);
        var output = {
            deletedDocuements : deletedDocuements,
            body : deleteion
        };
        getContext().getResponse().setBody(output);
    }
    var areDeleted = QueryMoviesOfGenre(collection,  genre);
    if (!areDeleted) throw "Unable to delete document(s)";
};