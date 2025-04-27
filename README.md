# 🚀 AI-Powered E-commerce Content Generator for Social Media

## 🔍 Overview

This project is a sophisticated AI-powered system that automatically generates engaging marketing content for e-commerce products. It extracts product information from e-commerce websites, analyzes product images, and leverages large language models to create compelling marketing scripts tailored to specific audiences, tones, and languages.

## ✨ Key Features

- 🕸️ **Web Scraping**: Automatically extracts product details from e-commerce sites
- 🖼️ **Image Analysis**: Generates descriptions of product images using computer vision models
- ✍️ **Content Generation**: Creates marketing scripts tailored to specific audiences and tones
- 🌍 **Multi-language Support**: Generates content in both Spanish and English
- 👥 **User-friendly Interface**: Simple Streamlit UI for easy content generation

## 🏗️ Technical Architecture

The project follows a microservices architecture with two main components:

### 🔧 Backend Services

- **Web Scraping Engine**: Extracts product details using Selenium and BeautifulSoup
- **Image Analysis Service**: Generates descriptions from product images using vision models
- **Content Generation Engine**: Creates marketing scripts using LLMs through Groq API
- **FastAPI Server**: Provides RESTful API endpoints for the frontend

### 🖥️ Frontend Interface

- **Streamlit Application**: User-friendly interface for generating content
- **Input Configuration**: Options for target audience, tone, and language
- **Output Visualization**: Displays the generated content with download options

## 📊 Data Science Components

### 1. 🕷️ Web Scraping and Data Extraction

The system uses a robust scraping mechanism based on Selenium and BeautifulSoup to extract product information:

- Product name, price, and available sizes
- Product specifications and additional information
- High-resolution product images

The scraper is designed to handle the dynamic nature of modern e-commerce sites with intelligent fallback mechanisms.

### 2. 👁️ Computer Vision for Image Analysis

The project incorporates computer vision capabilities:

- Creates a grid of product images for comprehensive visual analysis
- Uses the `deepseek-r1-distill-llama-70b` vision model through Groq API
- Generates detailed product descriptions highlighting visual features

### 3. 🧠 Natural Language Processing with LLMs

The content generation pipeline leverages:

- Groq API integration with models like `gemma2-9b-it`
- Custom prompt engineering for initial content generation
- Content refinement based on audience, tone, and language parameters
- Structured output parsing with Pydantic models

## 🔄 Data Flow Pipeline

1. User submits product URL with desired audience, tone, and language parameters
2. Backend scrapes product details and metadata
3. Product images are processed and analyzed using computer vision
4. Initial content is generated based on product information
5. Content is refined based on specified audience and tone parameters
6. Final content is returned to the user through the Streamlit interface

## 🛠️ Technologies Used

- **Python 3.9**: Core programming language
- **FastAPI**: Backend API framework
- **Streamlit**: Frontend user interface
- **Langchain**: Framework for LLM orchestration
- **Groq API**: LLM integration for content generation
- **Selenium & BeautifulSoup**: Web scraping
- **PIL/Pillow**: Image processing
- **Docker & Docker Compose**: Containerization and orchestration
- **Pydantic**: Data validation and serialization

## 🚦 Getting Started

### 📋 Prerequisites

- Docker and Docker Compose
- Groq API key

### 📝 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-reel-content-generator.git
   cd ai-reel-content-generator
   ```

2. Create a `.env` file in the root directory with the following variables:
   ```
   GROQ_API_KEY="your_groq_api_key"
   MODEL_NAME="gemma2-9b-it"
   VISION_MODEL_NAME="deepseek-r1-distill-llama-70b"
   BACKEND_URL="http://backend:8004/content_generator"
   ```

3. Build and run the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: Open your browser and navigate to `http://localhost:8501`
   - Backend API: Available at `http://localhost:8004`

## 📱 Usage

1. Enter the URL of an e-commerce product
2. Select your target audience (e.g., "Young adults (25-35 years)")
3. Choose the desired tone (e.g., "Professional", "Casual", "Motivational")
4. Select the language (Spanish or English)
5. Click "Generate Script" to create your marketing content
6. Download the generated content as JSON

## 🔮 Future Improvements

- **Enhanced Image Analysis**: Implement product segmentation and attribute detection
- **Multi-platform Content**: Generate platform-specific content for Instagram, TikTok, etc.
- **Sentiment Analysis**: Incorporate customer review sentiment into content generation
- **A/B Testing Integration**: Automatically generate multiple variants for testing
- **Performance Optimization**: Implement caching and parallel processing for faster scraping
- **Expanded Language Support**: Add more languages beyond Spanish and English

## 🧩 Technical Implementation Challenges

- **Web Scraping Robustness**: Implementing fallback strategies for various e-commerce site structures
- **Image Processing Optimization**: Managing image sizes for API limits while maintaining quality
- **Prompt Engineering**: Crafting effective prompts for consistent and high-quality content
- **Error Handling**: Graceful recovery from API errors and timeouts
- **Containerization**: Ensuring proper dependency management across microservices

## 💡 Data Science Insights

- The project demonstrates effective integration of multiple AI domains (NLP, computer vision, web scraping)
- Prompt engineering is crucial for extracting high-quality content from LLMs
- Structured output parsing ensures consistent application behavior
- Docker containerization simplifies deployment and dependency management
- The microservices architecture allows for independent scaling of components

This project showcases practical applications of AI for e-commerce marketing, streamlining content creation processes while maintaining quality and relevance.
