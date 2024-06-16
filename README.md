# WhatsApp Chat Analyzer

This repository contains a WhatsApp Chat Analyzer application built using Streamlit. The app allows users to upload their WhatsApp chat export files and generates insightful visualizations and statistics about the conversation. It provides various analyses such as message counts, word clouds, activity heatmaps, and more.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Overview

WhatsApp Chat Analyzer is a web application designed to analyze WhatsApp chat exports. With an easy-to-use interface, it provides users with valuable insights into their messaging habits and interactions. The application leverages the power of Streamlit to deliver an interactive and responsive user experience.

## Features

- Upload and parse WhatsApp chat export files.
- Generate overall chat statistics (total messages, total words, etc.).
- Visualize daily, weekly, and monthly activity patterns.
- Create word clouds for frequent words used in the chat.
- Identify most active participants in group chats.
- Display the distribution of messages over time.
- Plot message frequency heatmaps.

## Installation

To run the WhatsApp Chat Analyzer application locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/SkSay777/whatsapp-chat-analyzer.git
    cd whatsapp-chat-analyzer
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

## Usage

1. **Export your WhatsApp chat:**

    - Open the chat you want to analyze in WhatsApp.
    - Go to the chat settings and select "Export Chat".
    - Choose to export without media to keep the file size manageable.
    - Save the exported `.txt` file to your computer.

2. **Upload the chat file:**

    - Open the WhatsApp Chat Analyzer application in your browser.
    - Click on the "Browse files" button to upload your exported chat file.
    - The app will automatically process the file and display various analyses.

## Screenshots

### Home Page
![Home Page](screenshots/home_page.png)

### Chat Statistics
![Chat Statistics](screenshots/chat_statistics.png)

### Word Cloud
![Word Cloud](screenshots/word_cloud.png)

## Contributing

Contributions are welcome! If you have any ideas or improvements, please open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to reach out with any questions or suggestions! Enjoy analyzing your WhatsApp chats!
