
# knowledge_vault-frontend

## Description


## Languages
JavaScript, TypeScript

## Topics


## Stars
0

## README
# Knowledge Vault - Mobile App

A modern, cross-platform mobile application built with React Native and Expo. Knowledge Vault serves as your AI-assisted "second brain," allowing you to capture ideas and find them using semantic search.

## Problem Statement
Users frequently encounter interesting information or have creative ideas that they document but later struggle to find because they cannot remember the exact keywords used. Knowledge Vault addresses this by integrating with an AI backend to provide meaning-based retrieval, making personal knowledge truly accessible.

## Tech Stack Used
- **Frontend Framework:** [React Native](https://reactnative.dev/) with [Expo](https://expo.dev/) (SDK 54)
- **Navigation:** [Expo Router](https://docs.expo.dev/router/introduction/) (File-based routing)
- **Styling:** Vanilla React Native Stylesheets with Lucide Icons
- **Networking:** [Axios](https://axios-http.com/)
- **State Management:** React Context API (AuthContext)
- **Animations:** React Native Reanimated

## Features Implemented
- **Secure Authentication:** Persistent login session management.
- **Dynamic Knowledge Feed:** View and manage your stored knowledge items.
- **AI-Powered Search:** Dedicated search tab for semantic, meaning-based queries.
- **Rich Editor:** Intuitive interface for adding and editing knowledge items with titles, content, and tags.
- **Native Experience:** Smooth navigation and haptic feedback.

## How to Run Locally

### Prerequisites
- Node.js (LTS version)
- Expo Go app on your mobile device (for testing on physical hardware)
- Backend service running (see [Backend README](../backend/README.md))

### Steps
1. **Navigate to frontend directory:**
   ```bash
   cd knowledge_vault-frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Configure API URL:**
   Update the `API_URL` in `app.json` to point to your backend's local IP address:
   ```json
   "extra": {
     "API_URL": "http://YOUR_LOCAL_IP:8000"
   }
   ```
4. **Start the development server:**
   ```bash
   npx expo start
   ```
5. **Open the app:**
   Scan the QR code with the Expo Go app (Android) or Camera app (iOS).

## Project Structure
- `/app`: Main application routes and screens (using Expo Router).
- `/components`: Reusable UI elements (cards, inputs, buttons).
- `/context`: Global state providers (Authentication).
- `/api`: API client configuration and network calls.
- `/constants`: Theme and styling constants.