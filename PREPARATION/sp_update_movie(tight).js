function UpdateMovieGenre(genre, id) {
  var collection = getContext().getCollection();
  var collectionLink = collection.getSelfLink();

  var whereQuery = {
    query: "SELECT * FROM Movies m where m.id = @id",
    parameters: [{ name: "@id", value: id }],
  };
  var accept = collection.queryDocuments(
    collectionLink,
    whereQuery,
    (options = {}),
    (callback = function (err, documents, responseOptions) {
      if (err) throw new Error("Error:" + err.message);
      if (documents.length == 0) throw "no document found.";

      document.genre = genre;

      var accept = collection.replaceDocument(
        document._self,
        document,
        (callback = function (err, document) {
          if (err) throw new Error("Error:" + err.message);
          getContext().getResponse().setBody(replaceDocument);
        })
      );

      if (!accept) throw "Unable to update document";
    })
  );
  if (!accept) throw "Unable to update document";
}