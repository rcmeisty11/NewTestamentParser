from flask import Flask, jsonify, request, render_template
import os

app = Flask(__name__)

# Function to extract the book order number
def extract_book_order(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()  # Split the line by spaces
            if len(parts) >= 5:
                reference = parts[0]  # Book Order/Chapter/Verse (6 characters)
                book_order = int(reference[:2])  # Extract the first two digits for book order
                return book_order
    return None

# Function to parse the morphgnt text file
def parse_morphgnt_file(file_path):
    chapters = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()  # Split the line by spaces

            if len(parts) < 5:
                continue  # Skip malformed lines

            reference = parts[0]  # Book Order/Chapter/Verse (6 characters)
            chapter_num = int(reference[2:4])  # Extract the chapter number
            verse_num = int(reference[4:6])  # Extract the verse number
            part_of_speech = parts[1]  # Part of Speech (2 characters)
            parsing_code = parts[2]  # Morphological Parsing Code (8 characters)
            text_word = parts[3]  # The word that occurs in the text
            lemma = parts[-1]  # Lexical Form (lemma)

            # Ensure the chapter exists in the dictionary
            if chapter_num not in chapters:
                chapters[chapter_num] = {}

            # Ensure the verse exists in the chapter dictionary
            if verse_num not in chapters[chapter_num]:
                chapters[chapter_num][verse_num] = []

            # Store the parsed word in the correct chapter/verse
            word_data = {
                'part_of_speech': part_of_speech,
                'parsing_code': parsing_code,
                'text': text_word,
                'lemma': lemma
            }
            chapters[chapter_num][verse_num].append(word_data)

    return chapters

# Serve the main page
@app.route('/')
def index():
    text_files_dir = 'text_files'
    book_orders = {}

    # Loop through each file and extract the book order
    for file_name in os.listdir(text_files_dir):
        if file_name.endswith('.txt'):
            book_name = file_name.replace('.txt', '')
            file_path = os.path.join(text_files_dir, file_name)
            book_order = extract_book_order(file_path)

            if book_order is not None:
                book_orders[book_name] = book_order

    # Sort books by book order
    sorted_books = sorted(book_orders.items(), key=lambda x: x[1])

    return render_template('index.html', books=sorted_books)

# Serve book text from the files
@app.route('/get_book_text', methods=['GET'])
def get_book_text():
    book = request.args.get('book')
    file_path = f'text_files/{book}.txt'

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    chapters = parse_morphgnt_file(file_path)
    return jsonify(chapters)

@app.route('/how-to-use')
def how_to_use():
    return render_template('how_to_use.html')
    
if __name__ == '__main__':
    app.run(debug=True)
    
