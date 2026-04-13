
# CityNavigator

## Description


## Languages
TypeScript, CSS, JavaScript

## Topics


## Stars
0

## README
Deployed Link: https://city-navigator-pi.vercel.app/

Demo Video: https://drive.google.com/file/d/1padZ5S9XxEvvR2Ep6BMu56KkMd5C4ezU/view?usp=sharing

## 🎯 Project Goals

**Primary Objective**: Create an interactive web-based route-finding application that demonstrates real-world applications of graph algorithms through city navigation, showcasing the practical implementation of shortest path algorithms with visual feedback.

**Educational Goals**:

- Demonstrate graph theory concepts in a tangible, real-world context
- Compare algorithm performance and behavior differences
- Provide interactive visualization of algorithm execution
- Bridge theoretical computer science with practical applications


## 🚀 Key Features

### **Interactive Map Interface**

- **OpenStreetMap Integration**: Real map tiles with Leaflet.js
- **Dynamic Node Selection**: Click-to-select start/end points via dropdowns or map popups
- **Real-time Path Visualization**: Animated route display with directional arrows
- **Bidirectional Edge Display**: Visual representation of two-way streets


### **Dual Algorithm Implementation**

- **Dijkstra's Algorithm**: Guaranteed shortest path with uniform exploration
- **A* Algorithm**: Heuristic-guided pathfinding for faster convergence
- **Algorithm Switching**: Real-time comparison between approaches
- **Performance Metrics**: Step counting, distance calculation, and exploration tracking


### **Educational Visualization**

- **Node State Tracking**: Visual indicators for start, end, and explored nodes
- **Algorithm Statistics**: Complexity analysis, pros/cons comparison
- **Exploration Order**: Step-by-step visualization of node visitation
- **Path Reconstruction**: Clear route display with distance labels


### **Responsive Design**

- **Mobile-Friendly Interface**: Adaptive layout for all screen sizes
- **Interactive Controls**: Intuitive algorithm selection and route planning
- **Real-time Feedback**: Loading states and calculation progress


## 🛠️ Implementation Highlights

### **Frontend Architecture**

- **Next.js 15 + React**: Modern full-stack framework with App Router
- **TypeScript**: Type-safe development with custom interfaces
- **Tailwind CSS + shadcn/ui**: Consistent, responsive design system
- **Client-Side Rendering**: Proper hydration handling for map components


### **Graph Data Structure**

```typescript
interface GraphNode {
  id: string
  name: string
  lat: number
  lng: number
  type: "landmark" | "transport" | "education" | "commercial" | "medical" | "recreation"
}

interface GraphEdge {
  from: string
  to: string
  weight: number
  distance: number
  time: number
}
```

### **Algorithm Optimizations**

- **Early Termination**: Stops search immediately upon reaching target
- **Bidirectional Edge Handling**: Treats all roads as two-way unless specified
- **Efficient Data Structures**: Uses Sets and Maps for O(1) lookups
- **Memory Management**: Proper cleanup of map instances and event listeners


### **Real-World Mapping**

- **Coordinate System**: Latitude/longitude positioning
- **Distance Calculations**: Euclidean distance heuristics for A*
- **Visual Scaling**: Automatic map bounds fitting
- **Interactive Markers**: Custom styled nodes with type indicators


## 📚 Graph Concepts & Algorithms Implemented

### **Core Graph Theory Concepts**

- **Graph Representation**: Adjacency list structure with weighted edges
- **Bidirectional Graphs**: Two-way traversal for realistic city navigation
- **Weighted Edges**: Distance, time, and cost considerations
- **Graph Connectivity**: Path existence validation


### **Shortest Path Algorithms**

#### **1. Dijkstra's Algorithm**

- **Implementation**: Complete single-source shortest path
- **Data Structures**: Priority queue simulation with distance tracking
- **Complexity**: O((V + E) log V) time complexity
- **Features**:

- Guaranteed optimal solution
- Uniform exploration pattern
- Works with non-negative weights
- Early termination optimization





#### **2. A* (A-Star) Algorithm**

- **Implementation**: Heuristic-guided pathfinding
- **Heuristic Function**: Euclidean distance to target
- **Data Structures**: Open/closed sets with f-score tracking
- **Features**:

- Faster convergence than Dijkstra
- Goal-directed search
- Admissible heuristic ensures optimality
- Reduced node exploration





### **Graph Traversal Techniques**

- **Neighbor Discovery**: Bidirectional edge traversal
- **Path Reconstruction**: Backtracking through parent pointers
- **Visited Node Tracking**: Exploration order visualization
- **Distance Propagation**: Relaxation of edge weights


### **Algorithm Analysis & Comparison**

- **Performance Metrics**: Step counting and exploration tracking
- **Space Complexity**: Memory usage optimization
- **Time Complexity**: Big-O analysis display
- **Practical Trade-offs**: Speed vs. guarantee comparisons


### **Visualization Techniques**

- **Graph Rendering**: Node and edge visualization on map
- **Algorithm Animation**: Step-by-step exploration display
- **State Management**: Real-time algorithm state tracking
- **Interactive Feedback**: User-driven algorithm execution


## 🎓 Educational Value

This project demonstrates:

- **Real-world Applications**: How graph algorithms solve practical problems
- **Algorithm Comparison**: Trade-offs between different approaches
- **Visual Learning**: Interactive exploration of abstract concepts
- **Performance Analysis**: Understanding computational complexity
- **Data Structure Design**: Efficient graph representation