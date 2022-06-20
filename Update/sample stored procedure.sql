CREATE PROCEDURE sproc_UpdateMovieGenre
    @Genre nvarchar(30),
    @id INT
AS
    UPDATE 
        [dbo].[MoviesBoxSet]
    SET 
        genres = @Genre
    WHERE 
        id = @id
GO;