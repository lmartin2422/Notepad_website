// takes a noteID that we just passed
// send a POST request to the delete note endpoint
//  then reload the window

function deleteNote(noteId) {
    fetch("/delete-note",{
        method: "POST",
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/";
});
}