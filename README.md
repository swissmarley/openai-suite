# <p align="center">:rocket: OpenAI API Tools Suite :rocket:</p>

This web application utilizes Flask and the OpenAI API to offer a range of features including vision image analysis, image generation from text, audio to text transcription, and more. It's designed to showcase how Flask can be integrated with OpenAI's powerful models to create interactive and useful applications.

<img width="1209" alt="Main-Screen" src="https://github.com/swissmarley/openai-suite/assets/120587389/d2407b17-9239-49ed-b07c-a26cc775cddd">

## Features

- **ChatGPT**: Chat with different GPT-Models
- **Vision Image Analysis**: Analyze images and get insights.
- **Generate Image from Text**: Create images based on textual descriptions.
- **Generate Audio from Text**: Create spoken audio based on text input.
- **Audio to Text Transcription**: Convert audio files into text.
- **Image Inpainting**: Modify images by inpainting.

## Getting Started

To run this web application locally, you'll need Python installed on your system. Follow these steps:

**Clone the repository & Install required packages**

```bash
git clone https://github.com/swissmarley/openai-suite.git
cd openai-suite
pip install -r requirements.txt
```

**Set up environment variables**

Create or modify the **example.env** file to **.env** in the root directory of the project and add your OpenAI API key and any other configuration as needed:

```bash
OPENAI_API_KEY=your_openai_api_key_here
FLASK_SECRET_KEY=a_secret_key_for_session_management
```

**Run the application**

```bash
flask run
```

**Usage**

After starting the app, navigate to http://127.0.0.1:5000/ in your web browser. You'll be greeted with the main interface where you can choose the functionality you want to explore.

## Contributions

Contributions are welcome! If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
