# MY-PDF Application

## Overview

MY-PDF is a web application that integrates AI-powered content generation with PDF creation capabilities. The application uses FastAPI as the backend framework and provides a web interface for users to generate and manipulate PDF documents using OpenAI's GPT-5 model. The system combines modern web technologies with AI to create a streamlined document generation experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: FastAPI with Python for high-performance API development
- **Template Engine**: Jinja2Templates for server-side HTML rendering
- **HTTP Client**: httpx for asynchronous external API calls
- **API Design**: RESTful endpoints with form handling capabilities

### Frontend Architecture
- **Template-based Rendering**: Server-side HTML generation using Jinja2
- **PDF Generation**: Client-side PDF creation using jsPDF library
- **Styling**: CSS with gradient backgrounds and responsive design
- **Language**: French language interface (lang="fr")

### AI Integration
- **Model**: GPT-5 (specified as the newest OpenAI model released August 7, 2025)
- **API Configuration**: Configurable OpenAI API key through environment variables
- **Message Handling**: Support for both user prompts and system messages
- **Error Handling**: Comprehensive error management for API failures

### Configuration Management
- **Environment Variables**: Secure API key storage using os.getenv
- **Timeout Handling**: 30-second timeout for external API calls
- **Temperature Control**: AI response creativity controlled at 0.7
- **Token Limits**: Maximum 2000 tokens per AI response

## External Dependencies

### AI Services
- **OpenAI API**: GPT-5 model integration for content generation
- **API Endpoint**: https://api.openai.com/v1/chat/completions
- **Authentication**: Bearer token authentication

### Frontend Libraries
- **jsPDF**: Client-side PDF generation library (version 2.5.1)
- **CDN Delivery**: CloudFlare CDN for reliable library delivery

### Python Packages
- **FastAPI**: Web framework for API development
- **httpx**: Asynchronous HTTP client for external API calls
- **Jinja2**: Template engine for HTML rendering

### Development Tools
- **Environment Configuration**: Support for local development with fallback API keys
- **Error Response Handling**: Structured error messages for debugging