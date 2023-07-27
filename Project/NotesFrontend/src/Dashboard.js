import React, { useState, useEffect } from 'react';
import AWS from 'aws-sdk';
import { useParams } from 'react-router-dom';

// import AWS from 'aws-sdk';


// AWS.config.update({
//   accessKeyId: 'ASIA6CX3XVJEUOB6UX5D',
//   secretAccessKey: '2LIuDvtpK0zur2M+/AHcGuFwCk1lHArt17uL5vwI',
//   region: 'us-east-1' // e.g., 'us-east-1'
// });

const Dashboard = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [courseDetails, setCourseDetails] = useState(null);
  const [lectureNo, setLectureName] = useState('');
  const s3 = new AWS.S3();
  const { courseID } = useParams();
  console.log(courseID)

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleFileUpload = () => {
    if (selectedFile && lectureNo) {
      const fileName = selectedFile.name;
      const fileData = selectedFile;
      const s3BucketName = 'b00932103-notes';

      const folderKey = `${courseID}/${fileName}`;
  
      const params = {
        Bucket: s3BucketName,
        Key: folderKey,
        Body: fileData
      };
  
      s3.upload(params, async (err, data) => {
        if (err) {
          console.error('Error uploading file to S3:', err);
        } else {
          const fileUrl = data.Location;
          console.log('File uploaded to S3 successfully:', data.Location);
  
          // Prepare the request body
          // const requestBody = {
          //   courseID: courseID,
          //   lectureNo: lectureNo,
          //   fileURL: fileUrl
          // };
  
          // try {
          //   const response = await fetch('https://lv1qrdjxz4.execute-api.us-east-1.amazonaws.com/prod/store-file', {
          //     method: 'POST',
          //     headers: {
          //       'Content-Type': 'application/json'
          //     },
          //     body: JSON.stringify(requestBody)
          //   });
  
          //   if (response.ok) {
          //     console.log('File information stored successfully');
          //     // Add any additional logic or UI updates for successful storage
          //   } else {
          //     console.error('Error storing file information');
          //     // Handle error case, display error message, or perform any necessary actions
          //   }
          // } catch (error) {
          //   console.error('Error storing file information:', error);
          //   // Handle error case, display error message, or perform any necessary actions
          // }
        }
      });
    }
  };
  
  useEffect(() => {
    const fetchCourseDetails = async () => {
      try {
        const url = `https://mqywz41q78.execute-api.us-east-1.amazonaws.com/prod/course?courseID=${courseID}`;
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
          accept=".pdf,.doc,.docx,.txt,.png"
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
