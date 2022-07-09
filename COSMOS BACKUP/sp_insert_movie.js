function insert_movie(movie) {
    var collection = getContext().getCollection();

    var item = JSON.parse(movie);
    
    function setPrimaryGenre(genres){
        if(genres == null){return "";}
        else {return genres.split("|")[0];}
    }   

    item.primary_genre = setPrimaryGenre(item.genres);    
    [item.RowID, item.id] = [item.id, item.original_title];

    var isInserted = collection.createDocument(
        collection.getSelfLink(),
        item, 
        function(err, insertedMovie){
            if (err) throw new Error('Error' + err.message);  
            getContext().getResponse().setBody([insertedMovie, item])  
        }
    );

    if (!isInserted) throw new Error('The query was not accepted by the server.');
};