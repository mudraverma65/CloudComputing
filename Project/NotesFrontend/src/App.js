import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './LandingPage';
import LoginPage from './LoginPage';
import Header from './Header';
import Dashboard from './Dashboard';
import LandingPage1 from './old';
import './App.css';

const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/old" element={<LandingPage1 />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/course" element={<Dashboard/>} />
        <Route path="/course/:courseID" element={<Dashboard/>} />
      </Routes>
    </Router>
  );
};

export default App;
