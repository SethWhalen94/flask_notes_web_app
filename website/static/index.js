
function deleteNote(noteId) {
    /**
     * This function is a onClick function used to delete a note
     * makes POST request to the /delete-note endpoint
     * and then refreshes the page
     */
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId}),
    }).then((_result) => {
        window.location.href = "/";
    })
}