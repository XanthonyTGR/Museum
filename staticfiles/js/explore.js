// Sample JavaScript code to make AJAX requests
$(document).ready(function() {
    // Assume you have an element with class 'artifact-card' for each artifact
    $('.artifact-card').each(function() {
        var artifactId = $(this).data('artifact-id');

        // Get location
        $.get('/get_artifact_location/' + artifactId + '/', function(data) {
            $(this).find('.location-info').text('Location: ' + data.location);
        });

        // Get title
        $.get('/get_artifact_title/' + artifactId + '/', function(data) {
            $(this).find('.title-info').text('Title: ' + data.title);
        });
    });
});
