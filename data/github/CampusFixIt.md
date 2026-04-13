
# CampusFixIt

## Description


## Languages
JavaScript

## Topics


## Stars
0

## README
# Campus FixIt

## Overview
Campus FixIt is a React Native mobile application designed for reporting and tracking campus maintenance issues. It features a robust backend built with Node.js and Express, connected to a MongoDB database.

## Features
- **User Authentication**: Student and Admin login/registration using JWT.
- **Role-based Access**: 
  - Students can report issues with titles, descriptions, categories, and photos.
  - Admins can view all issues and update their status (Open -> In Progress -> Resolved).
- **Issue Tracking**: Real-time status updates and filtering.

## Tech Stack
- **Frontend**: React Native (Expo), React Navigation, Axios, Expo Image Picker.
- **Backend**: Node.js, Express, MongoDB (Mongoose), JSON Web Token (JWT).

## Setup Instructions

### Prerequisites
- Node.js installed
- MongoDB installed and running locally

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd campus-fixit/backend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   npm start
   ```
   The server runs on `http://localhost:5000`.

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd campus-fixit/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Update API URL (If testing on Emulator/Physical Device):
   - Open `src/utils/api.js`
   -  Replace `localhost` with your machine's local IP address (e.g., `192.168.1.X`) if using a physical device or Android Emulator (use `10.0.2.2`).
4. Start the Expo app:
   ```bash
   npx expo start
   ```

## API Endpoints
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/issues` - Create a new issue (Student only)
- `GET /api/issues` - Get all issues
- `PATCH /api/issues/:id` - Update issue status (Admin only)

## License
MIT
  # cap at 3000 chars per repo
