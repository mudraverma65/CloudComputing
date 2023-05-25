package com.A1.Container1;

import org.json.JSONObject;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

@RestController
public class Controller1 {

    String responseReceived = null;

    @PostMapping(path = "/calculate", consumes = "application/json")
    public String receiveJson(@RequestBody String response){
        try{
            System.out.println("Received Json: " +response);
            JSONObject jsonObject = new JSONObject(response.toString());
            String fileName = jsonObject.getString("file").toString();
            System.out.println("File: "+fileName);
            String product = jsonObject.getString("product").toString();
            System.out.println("Product: "+product);
            responseReceived = generateResponse(fileName, response);
        }
        catch(Exception e) {
            responseReceived = "Exception: " + e;
            System.out.println("Exception: " + e);
        }
        return responseReceived;
    }

    public String generateResponse(String fileName, String response){
        if(validFile(fileName)){
            try{
                String url = "http://localhost:6001/endpoint";
                HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Content-Type","application/json");
                connection.setDoOutput(true);

                try (OutputStream outputStream = connection.getOutputStream()) {
                    byte[] requestBodyBytes = response.getBytes("UTF-8");
                    outputStream.write(requestBodyBytes);
                    outputStream.flush();
                }
//                DataOutputStream outputStream = new DataOutputStream(connection.getOutputStream());
//                outputStream.writeBytes(response);
//                outputStream.flush();
//                outputStream.close();
                int responseCode = connection.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                    String line;
                    StringBuffer myResponse = new StringBuffer();
                    while ((line = reader.readLine()) != null) {
                        myResponse.append(line);
                    }
                    responseReceived = myResponse.toString();
                    reader.close();
                }
            }
            catch(Exception e){
                System.out.println("EEE: "+e);
            }
        }
        return responseReceived;
    }

    public Boolean validFile(String fileName){
        try{
            if(fileName==null){
                responseReceived = "{\"file\": \"" + fileName + "\", \"error\": \"Invalid JSON input\"}";
                System.out.println("Invalid JSON input");
                return false;
            }
//            String filePath = "/C1/"+fileName;
            String filePath = "Container1/"+fileName;
            System.out.println(filePath);
            File file = new File(filePath);
            if(!file.exists()){
                responseReceived = "{\"file\": \"" + fileName + "\", \"error\": \"File Not Found\"}";
                System.out.println("File Not Found");
                return false;
            }
        }
        catch (Exception e){
            System.out.println("Exception: "+e);
        }
        return true;
    }
    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }
}
