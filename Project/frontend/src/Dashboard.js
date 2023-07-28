import React, { useState, useEffect } from 'react';
import AWS from 'aws-sdk';
import { useParams } from 'react-router-dom';

const Dashboard = () => {
  const [uploadStatus, setUploadStatus] = useState(null); // To store upload status messages
  const [selectedFile, setSelectedFile] = useState(null);
  const [courseDetails, setCourseDetails] = useState(null);
  const [lectureNo, setLectureName] = useState('');
  const s3 = new AWS.S3({
    accessKeyId: 'ASIA6CX3XVJEVBGBRVXH',
    secretAccessKey: '5fRjt56W5W1txbkveFXv+t9EUY16t7bATzB6rSPW',
    sessionToken: 'FwoGZXIvYXdzEPT//////////wEaDChyD1TYgG6hI0qrnCLIAeVtkC87VMQC+wnpbEO8FcmZKQY/qSyR24Gc7qaDIV5TeELNsSLZmRBoVdw64MoR+gN3mI5p80dp1dMBJdqR/SeU3Xc1kDpIjyu9zUV4q4UyJmlVmhG3lM/P1CM7GzKgusxSp5GZSSf6vrGUMUtzSUpwgQlRijCo9UM19EeyIXGKbP5Ly28xXxVUcKAYlmJSGa8lRM8zkPwyKM+0rzFAaX4ZWFdKaJsQ1UpJwadobvUfDy5/HoI8TIm2T3k/tEc5F29PRVYr5OYMKPaSkKYGMi07ZWytGLZ/vEn/pZUElxn61aXtc9lh6Z/ok964rMm7iYAsGxmbEUFY3gcPuoo=',
    region: 'us-east-1' // e.g., 'us-east-1'
  });
  const { courseID } = useParams();
  console.log(courseID)

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleFileUpload = () => {
    if (selectedFile && lectureNo) {
      const fileName = selectedFile.name;
      const fileData = selectedFile;
      const s3BucketName = 'b00932103-notes-system';

      const folderKey = `${courseID}/${fileName}`;
  
      const params = {
        Bucket: s3BucketName,
        Key: folderKey,
        Body: fileData
      };
  
      s3.upload(params, (err, data) => {
        if (err) {
          console.error('Error uploading file to S3:', err);
          setUploadStatus('Error uploading file to S3'); // Set error message
        } else {
          console.log('File uploaded to S3 successfully:', data.Location);
          setUploadStatus('File uploaded successfully'); // Set success message
        }
      });
    }
  };
  
  useEffect(() => {
    const fetchCourseDetails = async () => {
      try {
        const url = `https://opv3f1heqe.execute-api.us-east-1.amazonaws.com/prod/course?courseID=${courseID}`;
        const response = await fetch(url);
        const data = await response.json();
        setCourseDetails(data.body);
      } catch (error) {
        console.error('Error fetching course details:', error);
      }
    };

    fetchCourseDetails();
  }, [courseID]);

  return (
    <div className="container">
      <h1 className="mt-5 mb-4">{courseDetails && courseDetails.name}</h1>
      {courseDetails && (
        <div>
          <h5>Course ID: {courseDetails.courseID}</h5>
          <h5>Instructor: {courseDetails.instructor}</h5>
        </div>
      )}

      {/* Upload Status Messages */}
      {uploadStatus && (
        <div className={`alert ${uploadStatus.includes('Error') ? 'alert-danger' : 'alert-success'}`}>
          {uploadStatus}
        </div>
      )}

      <div className="mb-3">
        <label htmlFor="lecture" className="form-label">Lecture Name</label>
        <input
          type="text"
          className="form-control"
          id="lecture"
          value={lectureNo}
          onChange={(e) => setLectureName(e.target.value)}
        />
      </div>

      <div className="mb-3">
        <label htmlFor="file" className="form-label">Upload File</label>
        <input
          type="file"
          className="form-control"
          id="file"
          accept=".pdf,.txt,.png,.jpeg,.jpg"
          onChange={handleFileChange}
        />
      </div>

      <button
        className="btn btn-primary"
        onClick={handleFileUpload}
        disabled={!selectedFile}
      >
        Upload
      </button>
    </div>
  );
};

export default Dashboard;
