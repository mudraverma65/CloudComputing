import React, { useState, useEffect } from 'react';
import { Modal, Button } from 'react-bootstrap';

import 'bootstrap/dist/css/bootstrap.min.css';

const LandingPage = () => {
  const [showModal, setShowModal] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [email, setEmail] = useState('');
  const [courseList, setCourseList] = useState([]);
  const [registrationMessage, setRegistrationMessage] = useState('');

  useEffect(() => {
    const fetchCourseList = async () => {
      try {
        const response = await fetch('https://44qf0igih4.execute-api.us-east-1.amazonaws.com/test/course-list');
        const data = await response.json();
        setCourseList(data.body);
      } catch (error) {
        console.error('Error fetching course list:', error);
      }
    };

    fetchCourseList();
  }, []);

  const handleRegister = (courseId) => {
    setSelectedCourse(courseId);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedCourse(null);
    setEmail('');
    setRegistrationMessage('');
  };

  const handleRegisterCourse = async () => {
    try {
      const response = await fetch('https://44qf0igih4.execute-api.us-east-1.amazonaws.com/test/course-register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          emailID: email,
          courseID: selectedCourse
        })
      });
      if (response.ok) {
        const data = await response.json();
        setRegistrationMessage(data.message);
        console.log('Registration successful');
        // Add any additional logic or UI updates for successful registration
      } else {
        console.error('Registration failed');
        // Handle error case, display error message, or perform any necessary actions
      }
    } catch (error) {
      console.error('Error registering for the course:', error);
      // Handle error case, display error message, or perform any necessary actions
    }
    handleCloseModal();
  };

  return (
    <div className="container">
      <h1 className="mt-5 mb-4">Available Courses</h1>
      <div className="row">
        {courseList.map((course) => (
          <div key={course.courseID} className="col-md-4 mb-4">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">Course: {course.name}</h5>
                <p className="card-text">Instructor: {course.instructor}</p>
                <button className="btn btn-primary" onClick={() => handleRegister(course.courseID)}>
                  Register
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Register for Course</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Enter your email address to register for the course.</p>
          <input
            type="email"
            className="form-control"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleRegisterCourse}>
            Register
          </Button>
        </Modal.Footer>
      </Modal>

      {registrationMessage && (
        <div className="mt-3 alert alert-success" role="alert">
          {registrationMessage}
        </div>
      )}
    </div>
  );
};

export default LandingPage;
