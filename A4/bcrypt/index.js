const axios = require('axios');
const bcrypt = require('bcryptjs'); // Import bcryptjs instead of bcrypt

exports.handler = async (event, context) => {
  try {
    const { course_uri, action, value } = event;

    // Perform bcrypt hashing with a salt
    const saltRounds = 10; // You can adjust the number of rounds as needed
    const hashedValue = await bcrypt.hash(value, saltRounds);

    // Prepare the response
    const response = {
      banner: "B00932103",
      result: hashedValue,
      arn: context.invokedFunctionArn,
      action: action,
      value: value
    };

    // Send the response to the course_uri using axios
    const axiosResponse = await axios.post(course_uri, response); // Pass response directly as data
    console.log(`Response Status Code: ${axiosResponse.status}`);

    return {
      statusCode: 200,
      body: JSON.stringify(response)
    };

  } catch (error) {
    console.error(`Error: ${error.message}`);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
