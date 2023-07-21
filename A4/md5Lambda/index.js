const axios = require('axios');
const crypto = require('crypto');

exports.handler = async (event, context) => {
  try {
    const { course_uri, action, value } = JSON.parse(event.body);

    // Perform MD5 hashing
    const hashedValue = crypto.createHash('md5').update(value).digest('hex');

    // Prepare the response
    const response = {
      banner: "<Your Banner ID>",
      result: hashedValue,
      arn: context.invokedFunctionArn,
      action: action,
      value: value
    };

    // Send the response to the course_uri using Axios
    const requestOptions = {
      method: 'post',
      url: course_uri,
      headers: {
        'Content-Type': 'application/json'
      },
      data: JSON.stringify(response)
    };

    const res = await axios(requestOptions);
    console.log('Response Status Code:', res.status);
    console.log('Response Body:', res.data);

    return {
      statusCode: 200,
      body: JSON.stringify(response)
    };

  } catch (error) {
    console.error('Error:', error.message);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
