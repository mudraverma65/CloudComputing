import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const [courseID, setCourseID] = useState('');
  const [password, setPassword] = useState('');
  const [loginStatus, setLoginStatus] = useState('');
  const [isLoginSuccess, setIsLoginSuccess] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    // Add your logic here to handle the login process
    const url = `${process.env.REACT_APP_API_ENDPOINT}/login`;
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ courseID, password })
    };

    try {
      const response = await fetch(url, requestOptions);
      if (response.status === 200) {
        // Login successful
        setIsLoginSuccess(true);
        setLoginStatus('Login successful');
        navigate(`/course/${courseID}`);
      } else {
        // Login failed
        setIsLoginSuccess(false);
        setLoginStatus('Invalid credentials');
      }
    } catch (error) {
      console.log('Error:', error);
    }
  };

  return (
    <div className="container">
      <h1 className="mt-5 mb-4">Course Login</h1>
      <form onSubmit={handleLogin}>
        <div className="mb-3">
          <label htmlFor="courseID" className="form-label">Course ID</label>
          <input
            type="text"
            className="form-control"
            id="courseID"
            value={courseID}
            onChange={(e) => setCourseID(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Login</button>
      </form>
      {loginStatus && <p>{loginStatus}</p>}
      {isLoginSuccess && <p>Login successful. Redirecting...</p>}
    </div>
  );
};

export default LoginPage;
