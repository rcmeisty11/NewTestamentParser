document.addEventListener('DOMContentLoaded', function() {
    const bookDropdown = document.getElementById('book');

    // Fetch content when the page loads (default: Matthew)
    fetchBookContent(bookDropdown.value);

    // Fetch content when the dropdown changes
    bookDropdown.addEventListener('change', function() {
        fetchBookContent(this.value);
    });

    function fetchBookContent(book) {
        fetch(`/get_book_text?book=${book}`)
        .then(response => response.json())
        .then(data => {
            console.log('Received data:', data);
            let chapterContent = document.getElementById('chapter-content');
            chapterContent.innerHTML = '';  // Clear previous content

            // Process the chapters and verses
            Object.keys(data).forEach(chapter => {
                let accordionHtml = `
                <div class="accordion" id="accordionChapter${chapter}">
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="heading${chapter}">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${chapter}" aria-expanded="false" aria-controls="collapse${chapter}">
                                Chapter ${parseInt(chapter, 10)}
                            </button>
                        </h2>
                        <div id="collapse${chapter}" class="accordion-collapse collapse" aria-labelledby="heading${chapter}" data-bs-parent="#accordionChapter${chapter}">
                            <div class="accordion-body">`;

                // Sort and display verses
                Object.keys(data[chapter]).forEach(verse => {
                    let verseText = data[chapter][verse].map(word_data => {
                        return `<span class="word" data-morph="Part of Speech: ${word_data.part_of_speech}, Parsing Code: ${word_data.parsing_code}, Lexical Form (Lemma): ${word_data.lemma}">${word_data.text}</span>`;
                    }).join(' ');

                    accordionHtml += `
                    <div class="verse" style="display: flex; align-items: flex-start; margin-bottom: 10px;">
                        <div style="width: 50px; font-weight: bold; text-align: left; padding-right: 10px;">${parseInt(verse, 10)}</div>
                        <div style="text-align: left; padding-left:5px;">${verseText}</div>
                    </div>`;
                });

                accordionHtml += `
                            </div>
                        </div>
                    </div>
                </div>`;

                // Append this chapter's accordion to the content
                chapterContent.innerHTML += accordionHtml;
            });
        })
        .catch(error => {
            console.error('Error fetching book content:', error);
            document.getElementById('chapter-content').innerHTML = '<p>Error loading book content. Please try again later.</p>';
        });
    }
});
