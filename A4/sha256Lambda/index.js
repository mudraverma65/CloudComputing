const axios = require('axios');
const crypto = require('crypto');

exports.handler = async (event, context) => {
  try {
    const { course_uri, action, value } = JSON.parse(event.body);

    // Perform SHA-256 hashing
    const hashedValue = crypto.createHash('sha256').update(value).digest('hex');

    // Prepare the response
    const response = {
      banner: "<Your Banner ID>",
      result: hashedValue,
      arn: context.invokedFunctionArn,
      action: action,
      value: value
    };

    // Send the response to the course_uri using axios
    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      data: JSON.stringify(response)
    };

    const axiosResponse = await axios.post(course_uri, requestOptions);
    console.log(`Response Status Code: ${axiosResponse.status}`);
    console.log(axiosResponse.data);

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
