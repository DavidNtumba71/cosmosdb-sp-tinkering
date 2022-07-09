function insert_movie(movie) {
    var collection = getContext().getCollection();

    var isInserted = collection.createDocument(
        collection.getSelfLink(),
        movie, 
        function(err, insertedMovie){
            if (err) throw new Error('Error' + err.message);  
            context.getResponse().setBody(insertedMovie)  
        }
    );

    if (!isInserted) throw new Error('The query was not accepted by the server.');
};