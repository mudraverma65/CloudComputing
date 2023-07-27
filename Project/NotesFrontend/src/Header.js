import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  const handleInstructorLogin = () => {
    // Add your logic here for instructor login
    console.log('Course Login clicked');
    navigate('/login');
  };

  return (
    <header className="navbar navbar-dark bg-dark">
      <div className="container">
        <a className="navbar-brand" href="/">Notes Distribution System</a>
        <button className="btn btn-primary" onClick={handleInstructorLogin}>
          Course Login
        </button>
      </div>
    </header>
  );
};

export default Header;
