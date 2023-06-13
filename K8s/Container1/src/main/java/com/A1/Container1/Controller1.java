package com.A1.Container1;

import org.json.JSONObject;
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
        JSONObject returnJson = new JSONObject();
        try{
            String fileName = null;
            JSONObject jsonObject = new JSONObject(response.toString());
            if(jsonObject.isNull("file") == false){
                fileName = jsonObject.getString("file").toString();
            }
            responseReceived = generateResponse(fileName, response);
        }
        catch(Exception e) {
            responseReceived = "{\"file\": null, \"error\": \"Invalid JSON input.\"}";
            System.out.println("Exception: " + e);
        }
        return responseReceived;
    }

    public String generateResponse(String fileName, String response){
        if(validFile(fileName)){
            try{
                String url = "http://container2:6001/endpoint";
                HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Content-Type","application/json");
                connection.setDoOutput(true);

                try (OutputStream outputStream = connection.getOutputStream()) {
                    byte[] requestBodyBytes = response.getBytes("UTF-8");
                    outputStream.write(requestBodyBytes);
                    outputStream.flush();
                }
                int responseCode = connection.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                    String line;
                    StringBuilder myResponse = new StringBuilder();
                    while ((line = reader.readLine()) != null) {
                        myResponse.append(line);
                    }
                    responseReceived = myResponse.toString();
                    reader.close();
                }
            }
            catch(Exception e){
                System.out.println("Exception: "+e);
            }
        }
        return responseReceived;
    }

    public Boolean validFile(String fileName){
        try{
            if(fileName==null){
                responseReceived = "{\"file\": null, \"error\": \"Invalid JSON input.\"}";
                return false;
            }
            String filePath = "/app/"+fileName;
            File file = new File(filePath);
            if(!file.exists()){
                responseReceived = "{\"file\": \"" + fileName + "\", \"error\": \"File not found.\"}";
                return false;
            }
        }
        catch (Exception e){
            responseReceived = "{\"file\": null, \"error\": \"Invalid JSON input.\"}";
            System.out.println("Exception: "+e);
        }
        return true;
    }
}
