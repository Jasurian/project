// Add an event listener to the "Bold" button
document.getElementById('bold-button').addEventListener('click', function() {
    // Log a message to the console for debugging
    console.log("Bold button clicked");
    
    // Execute the "bold" command on the contenteditable element
    document.execCommand('bold', false, null);
});

// Add an event listener to the "Italic" button
document.getElementById('italic-button').addEventListener('click', function() {
    // Log a message to the console for debugging
    console.log("Italic button clicked");
    
    // Execute the "italic" command on the contenteditable element
    document.execCommand('italic', false, null);
});

// Add an event listener to the "Underline" button
document.getElementById('underline-button').addEventListener('click', function() {
    // Log a message to the console for debugging
    console.log("Underline button clicked");
    
    // Execute the "underline" command on the contenteditable element
    document.execCommand('underline', false, null);
});

// Add an event listener to the color picker input
document.getElementById('color-picker').addEventListener('input', function(event) {
    // Log a message to the console for debugging
    console.log("Color picker changed to: " + event.target.value);
    
    // Execute the "foreColor" command on the contenteditable element with the selected color
    document.execCommand('foreColor', false, event.target.value);
});

// Variable to store the current file name (initially empty)
let currentFileName = '';

// Add an event listener to the "Save" button
document.getElementById('save-button').addEventListener('click', function() {
    // Get the content of the editor
    const content = document.getElementById('editor').innerHTML;

    // If a file name is not set, prompt the user to enter a file name (with a default of "document.txt")
    if (!currentFileName) {
        currentFileName = prompt('Enter a file name:', 'document.txt');
    }

    // If a file name is provided (or already set)
    if (currentFileName) {
        // Create a Blob containing the content with a specified MIME type
        const blob = new Blob([content], { type: 'text/plain' });

        // Create a URL for the Blob
        const url = URL.createObjectURL(blob);

        // Create a hidden anchor element
        const a = document.createElement('a');

        // Set the anchor's URL and download attribute with the current file name
        a.href = url;
        a.download = currentFileName;

        // Programmatically trigger a click on the anchor element to initiate the download
        a.click();

        // Clean up the URL object to release resources
        URL.revokeObjectURL(url);
    }
});

// Add an event listener to the file input for opening documents
document.getElementById('file-input').addEventListener('change', function(event) {
    // Get the selected file from the input
    const file = event.target.files[0];
    
    // Check if a file was selected
    if (file) {
        // Create a FileReader to read the file's contents
        const reader = new FileReader();
        
        // Set up a callback for when the file is loaded
        reader.onload = function(e) {
            // Set the content of the editor to the file's content
            document.getElementById('editor').innerHTML = e.target.result;
        };
        
        // Read the file as text
        reader.readAsText(file);
    }
});

// Add an event listener to the "Save As" button
document.getElementById('save-as-button').addEventListener('click', function() {
    // Get the content of the editor
    const content = document.getElementById('editor').innerHTML;

    // Prompt the user to enter a file name
    const fileName = prompt('Enter a file name:', 'document.txt');

    // If a file name is provided
    if (fileName) {
        // Create a Blob containing the content with a specified MIME type
        const blob = new Blob([content], { type: 'text/plain' });

        // Create a URL for the Blob
        const url = URL.createObjectURL(blob);

        // Create a hidden anchor element
        const a = document.createElement('a');

        // Set the anchor's URL and download attribute with the provided file name
        a.href = url;
        a.download = fileName;

        // Programmatically trigger a click on the anchor element to initiate the download
        a.click();

        // Clean up the URL object to release resources
        URL.revokeObjectURL(url);
    }
});

// Add an event listener to the "Back to Dashboard" button
document.getElementById('back-button').addEventListener('click', function() {
    // Prompt the user to save the document before going back to the dashboard
    const confirmMessage = 'Do you want to save the document before going back to the dashboard?';
    if (confirm(confirmMessage)) {
        // Trigger the "Save" button click event
        document.getElementById('save-button').click();
    }

    // Redirect to the dashboard (replace this with your actual dashboard URL)
    window.location.href = 'dashboard.html';
});

// Variable to track whether changes have been made
let changesMade = false;

// Function to set the changesMade flag when content is modified
document.getElementById('editor').addEventListener('input', function () {
    changesMade = true;
});

// Function to display a confirmation dialog when navigating away
window.addEventListener('beforeunload', function (e) {
    if (changesMade) {
        // Prompt the user to confirm before leaving
        e.preventDefault();
        e.returnValue = '';
    }
});
