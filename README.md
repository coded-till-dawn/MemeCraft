# ✨ MemeCraft

**MemeCraft** is a professional, AI-powered design tool that transforms your ideas into viral-ready memes in seconds. By leveraging state-of-the-art image generation technology, it allows users to create unique, high-quality templates from simple text descriptions.

## 🚀 Key Features

*   **Generative AI Templates**: Simply describe a scene (e.g., *"A futuristic city where everyone rides giant hamsters"*), and the engine generates a high-definition, original meme template.
*   **Advanced Text Editor**: comprehensive suite of styling tools including dynamic font sizing, custom colors, outline controls, and precise vertical padding.
*   **Modern Interface**: A sleek, dark-themed UI designed for a seamless creative workflow.
*   **High-Resolution Export**: Download your creations instantly in optimized JPEG format.

## 🛠️ Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd MemeCraft
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    *   Create a `.env` file in the root directory.
    *   Add your API token for the image generation service:
        ```env
        REPLICATE_API_TOKEN=your_token_here
        ```

4.  **Launch the Application**:
    ```bash
    streamlit run app.py
    ```

## 📂 Architecture

*   **`app.py`**: The core Streamlit application handling the UI and state management.
*   **`utils/ai_generator.py`**: Interface for the generative AI backend.
*   **`utils/meme_renderer.py`**: Custom graphics engine for high-quality text rendering and compositing.
*   **`static/`**: Static assets and resources.

## 📄 License

This project is open-source and available under the MIT License.
