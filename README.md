# The Crate

A community-driven web app for archiving and streaming hip-hop mixtapes.

## Tech Stack

### Backend

- FastAPI
- Supabase (PostgreSQL + Storage)
- FFmpeg for audio processing

### Frontend

- React + Vite
- Chakra UI
- TypeScript

## Project Structure

```
.
├── backend/           # FastAPI application
├── frontend/          # React + Vite frontend
├── docker/            # Docker configuration files
└── docs/             # Project documentation
```

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 18+
- Python 3.11+
- FFmpeg

### Quick Start

1. Clone the repository:

```bash
git clone https://github.com/yourusername/the-crate.git
cd the-crate
```

2. Start the development environment:

```bash
docker-compose up
```

3. Access the applications:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Features

### MVP Features

- Admin-only upload functionality
- Album management (CRUD operations)
- High-quality audio streaming
- Album grid view
- Track listing and playback

## License

MIT
