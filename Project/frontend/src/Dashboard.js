import React, { useState, useEffect } from 'react';
import AWS from 'aws-sdk';
import { useParams } from 'react-router-dom';

const Dashboard = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [courseDetails, setCourseDetails] = useState(null);
  const [lectureNo, setLectureName] = useState('');
  const s3 = new AWS.S3({
    accessKeyId: 'ASIA6CX3XVJE5FKH7LWL',
    secretAccessKey: 'LvVl915FJx2LEvDD9CC5h01wK36cS5iqbD9BI5oB',
    sessionToken: 'FwoGZXIvYXdzEOj//////////wEaDAe5ufMwwpI5D22JHSLIAd1opuQdWtrHhOOgFD3izpDdZSFCfEd8PTcdgff/DR8vina5ZibuXMS+ZydELeYazrZswF7VeuPyKr+IHnYdzDFIXdm/sOCVna82wn0nFKEuRkHJRHN0ya9iBke9AaG6rKdCJCR+rYaffstZMrpWpbYptpqZUE5lSbsuX3K2n85JeJKI7v3Pk+S2Qb/EGpJBzw2p59jckKcLx/OxWUqdJHzi5EDqKeJxnFsk85gEsDe7bQ6xeMfxMu3cCGjbjV1YzsnIMAza4d1sKODGjaYGMi3T5TCfG2xBIaASngWtkoxeanHHZThRcI5hqwjYzQag+qErR/Z4Dzvq8G+rNS4=',
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
        const url = `https://tipv8u9h4m.execute-api.us-east-1.amazonaws.com/prod/course?courseID=${courseID}`;
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
