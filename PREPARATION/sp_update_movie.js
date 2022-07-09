function UpdateMovieGenre(genre, id) {
  var collection = getContext().getCollection();
  var collectionLink = collection.getSelfLink();

  var whereQuery = {
    query: "SELECT * FROM Movies m where m.id = @id;",
    parameters: [{ name: "@id", value: id }],
  };
  function ExecuteWhereClause(collection, collectionLink) {
    return collection.queryDocuments(
      collectionLink,
      whereQuery,
      (options = {}),
      (callback = QueryCallback)
    );
  }
  function QueryCallback(err, documents, responseOptions) {
    if (err) throw new Error("Error:" + err.message);
    if (documents.length == 0) throw "no document found.";
    ApplyUpdate(documents, genre);
    return;
  }
  function ApplyUpdate(document, genre) {
    document.genre = genre;
    var accept = collection.replaceDocument(
      document._self,
      document,
      (callback = UpdateCallback)
    );
    if (!accept) throw "Unable to update document";
  }
  function UpdateCallback(err, replaceDocument) {
    if (err) throw new Error("Error:" + err.message);
    getContext().getResponse().setBody(replaceDocument);
  }
  var isUpdated = ExecuteWhereClause(collection, collectionLink);
  if (!isUpdated) throw "Unable to update document";
}